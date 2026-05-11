require("dotenv").config();
const express = require("express");
const { createClient } = require("@supabase/supabase-js");
const axios = require("axios");
const path = require("path");

const stopwords = require("./stopwords-en.json");

const lcpo = require("./lcpo");

const app = express();
app.use(express.json());

const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_KEY = process.env.SUPABASE_SECRET_KEY;
const MAIN_TABLE = process.env.MAIN_TABLE || "cybernews";
const ROOT_URL = "https://notifycyber.com/";

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

async function siteStatus(url) {
  try {
    const response = await axios.get(url);
    return response.status === 200;
  } catch (error) {
    console.error(`Error checking site status for ${url}: ${error.message}`);
    return false;
  }
}

function formatEpoch(epochSeconds) {
  const utcTime = new Date(epochSeconds * 1000);
  return utcTime.toISOString();
}

async function getLatestRecorded() {
  let { data, error } = await supabase
    .from(MAIN_TABLE)
    .select("recorded")
    .order("id", {
      ascending: false,
    })
    .limit(1);

  if (error) {
    console.error("Error fetching latest recorded:", error);
    return null;
  }
  return data[0].recorded;
}

async function getWeeksLastNews() {
  const sevenDaysAgo = Math.floor(Date.now() / 1000) - 7 * 24 * 60 * 60;
  let { data, error } = await supabase
    .from(MAIN_TABLE)
    .select("id, source, url, title, recorded, details")
    .gte("recorded", sevenDaysAgo);
  return {
    data: data,
    error: error,
  };
}

async function searchNewsByKeywords(keywords) {
  const MAX_KEYWORDS_LENGTH = 10;
  const MIN_KEYWORD_CHAR_LENGTH = 2;

  if (Array.isArray(keywords) === false) {
    throw new Error(`keywords most be an array of strings`);
  }

  if (keywords.length === 0) {
    throw new Error(`no keywords were provided`);
  }

  if (keywords.length > MAX_KEYWORDS_LENGTH) {
    throw new Error(`exceeded keyboards limit`);
  }

  for (let word of keywords) {
    // keyword most be AT-LEAST one character long
    if (word.length < MIN_KEYWORD_CHAR_LENGTH) {
      throw new Error(`${word} is too short of a keyword`);
    }

    // keyword most NOT be a stop-word
    if (stopwords.includes(word)) {
      throw new Error(`${word} is a stop word`);
    }
  }

  const pattern = keywords.map((keyword) => `%${keyword}%`);
  let { data, error } = await supabase
    .from(MAIN_TABLE)
    .select("id, source, url, title, recorded, details")
    .or(
      pattern
        .map(
          (keyword) =>
            `url.ilike.${keyword},title.ilike.${keyword},details.ilike.${keyword}`,
        )
        .join(","),
    )
    .order("id", {
      ascending: false,
    });

  if (error) {
    throw new Error(`${error}`);
  }

  return data;
}

//////////////////////////////////////////////////////////////////////////////////////////////////

app.get("/search", async (req, res) => {
  const authorization = req.headers.authorization;
  if (!authorization) {
    return res.status(401).json({
      error: "'authorization' is missing from the header",
    });
  }

  if (!lcpo.basicValidator(authorization)) {
    return res.status(401).json({
      error: "token is invalid",
    });
  }

  console.log(`Request made to /search endpoint from ${req.ip}`);

  let response = {};
  try {
    const keywords = Object.keys(req.query)
      .join(",")
      .split(",")
      .filter(Boolean);
    response = await searchNewsByKeywords(keywords);
  } catch (err) {
    response = {
      error: `${err}`,
    };
  }

  res.json(response);
});

app.get("/past_week", async (req, res) => {
  const authorization = req.headers.authorization;
  if (!authorization) {
    return res.status(401).json({
      error: "'authorization' is missing from the header",
    });
  }

  if (!lcpo.basicValidator(authorization)) {
    return res.status(401).json({
      error: "token is invalid",
    });
  }

  console.log(`Request made to /past_week endpoint from ${req.ip}`);

  const response = await getWeeksLastNews();

  if (response.error) {
    return res.status(500).json({
      error: error.message,
    });
  }

  res.json(response.data);
});

app.get("/status", async (req, res) => {
  const authorization = req.headers.authorization;
  if (!authorization) {
    return res.status(401).json({
      error: "'authorization' is missing from the header",
    });
  }

  if (!lcpo.basicValidator(authorization)) {
    return res.status(401).json({
      error: "token is invalid",
    });
  }

  console.log(`Request made to /status endpoint from ${req.ip}`);

  const websiteStatus = await siteStatus(ROOT_URL);
  const latestRecordedEpoch = await getLatestRecorded();
  const latestRecordedTime = latestRecordedEpoch
    ? formatEpoch(latestRecordedEpoch)
    : null;

  res.json({
    root_url: ROOT_URL,
    website_status: websiteStatus,
    latest_record: {
      epoch: latestRecordedEpoch,
      formatted_time: latestRecordedTime,
    },
  });
});

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "home.html"));
});

// main function calls for running the root server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
