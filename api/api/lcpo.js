const fs = require("fs");
const crypto = require("crypto");
const uuid = require("uuid");

const hashes = require("./hash.json");

function readFile(path) {
  return fs
    .readFileSync(path, "utf8")
    .split("\n")
    .filter((line) => line.trim());
}

function writeFile(path, data) {
  fs.writeFileSync(path, data.join("\n"), "utf8");
}

function readJson(path) {
  return JSON.parse(fs.readFileSync(path, "utf8"));
}

function writeJson(path, data) {
  fs.writeFileSync(path, JSON.stringify(data, null, 4), "utf8");
}

function hashKey(key) {
  return crypto.createHash("sha256").update(key).digest("hex");
}

function createChecksum(apiKey) {
  let total = 0;
  let add = true;
  for (let i = 0; i < apiKey.length; i++) {
    if (!isNaN(apiKey[i])) {
      let num = parseInt(apiKey[i]);
      if (add) {
        total += num;
        add = false;
      } else {
        total -= num;
        add = true;
      }
    }
  }
  let value = Math.abs(total).toString().padStart(4, "0").substring(0, 4);
  let firstChar = apiKey[0];
  let lastChar = apiKey.replace(/-/g, "")[apiKey.replace(/-/g, "").length - 1];
  return `${firstChar}${lastChar}${value}`;
}

function generateKey() {
  const rawKey = `${uuid.v4()}-${crypto.randomBytes(8).toString("hex")}`;
  const checksum = createChecksum(rawKey);
  const key = `${rawKey}-${checksum}`;
  const hashedKey = hashKey(key);
  return {
    key,
    hash: hashedKey,
  };
}

function initialKeyVerification(apiKey) {
  const expectedLength = 76;
  const dashPositions = [8, 13, 18, 23, 36, 69];
  if (
    apiKey.length !== expectedLength ||
    dashPositions.some((pos) => apiKey[pos] !== "-")
  ) {
    return false;
  }
  const expectedChecksum = createChecksum(apiKey.substring(0, 70));
  const actualChecksum = apiKey.substring(70);
  return expectedChecksum === actualChecksum;
}

// NOTE: run this function to generate local hash storage for auth
// NOTE: you MOST run this function atleast once!
// NOTE: after the first run, run it carefully
function createHashKeyFiles() {
  const keys = [];
  for (let i = 0; i < 10; i++) {
    keys.push(generateKey());
  }
  const hashes = keys.map((key) => key.hash);
  writeJson("keys.json", keys);
  writeJson("hash.json", hashes);
}

function basicValidator(token) {
  token = token.replace("Bearer ", "");

  if (initialKeyVerification(token)) {
    return false;
  }

  let hashToken = hashKey(token);
  for (let hash of hashes) {
    if (hashToken === hash) {
      return true;
    }
  }

  return false;
}

function convertToObjURL(url) {
  let arr = String(url).split("&").slice(1);

  let result = {};
  arr.forEach((item) => {
    let [key, value] = item.split("=");
    if (key === "limit") {
      let num = parseInt(value, 10);
      if (!isNaN(num) && num.toString() === value) {
        result[key] = num;
      }
    } else if (key === "select") {
      if (value.includes(",")) {
        result[key] = value.split(",").map((s) => s.trim());
      } else {
        result[key] = [value.trim()];
      }
    }
  });

  return result;
}

module.exports = {
  basicValidator,
  readFile,
  writeFile,
  readJson,
  writeJson,
  hashKey,
  generateKey,
  initialKeyVerification,
  createHashKeyFiles,
  convertToObjURL,
};
