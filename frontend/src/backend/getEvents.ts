// function to get scraped events from the database

"use server"; // make sure this only runs on the server

import config from "@/src/backend/config";
import logger from "@/src/backend/logger";
import util from "@/src/backend/utils";
import stopwords from "stopwords-en";

// for some reason "microsoft" is included in stopwords-en, not sure why
const filteredStopwords = stopwords.filter(
  (stopword) => stopword !== "microsoft"
);

// this must be async since it runs on the server
export default async function getEvents(
  limit: number,
  last_id: number,
  payload: any,
  search_string: string
): Promise<any> {
  if (search_string) {
    payload.filter = search_string
      .split(" ")
      .map((word) => word.toLowerCase())
      .filter((word) => !filteredStopwords.includes(word));
  }

  logger.info(`payload sent: ${JSON.stringify(payload)}`);

  let validOutput = util.validatePayload(payload, config.max_days_back);
  if (validOutput.error != null) {
    logger.error(
      `submitted payload is invalid: ${JSON.stringify(validOutput)}`
    );
    return { "msg": `submitted payload is invalid: ${JSON.stringify(validOutput)}`, "status": 400 }
  }

  const result = await util.buildSQLQuery(payload, limit, last_id);
  if (result === undefined) {
    return { "error": "error fetching data from database", "status": 500 }
  }

  return result;
}
