const crypto = require("crypto");
const fs = require("fs");
const path = require("path");
const readline = require("readline");

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

function generateHash() {
  return crypto.randomBytes(32).toString("hex");
}

rl.question("How many hashes do you want to generate? ", (answer) => {
  const count = parseInt(answer, 10);

  if (isNaN(count) || count <= 0) {
    console.log("Please enter a valid positive number.");
    rl.close();
    return;
  }

  const hashes = [];
  for (let i = 0; i < count; i++) {
    hashes.push(generateHash());
  }

  const outputPath = path.join(__dirname, "api", "hash.json");
  fs.writeFileSync(outputPath, JSON.stringify(hashes, null, 4));

  console.log(`✓ Generated ${count} hashes and saved to ${outputPath}`);
  rl.close();
});
