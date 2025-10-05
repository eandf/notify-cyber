// function to get the id of the most recently scraped article

"use server"; // make sure this only runs on the server

import logger from "@/src/backend/logger";
import util from "@/src/backend/utils";

// this must be async since it runs on the server
export async function getLatestID(): Promise<number> {
  let result;
  try {
    result = await util.getLatestID();
  } catch (error) {
    if (error instanceof Error) {
      throw error;
    }
  }

  logger.info(`the endpoint latest/ is sending the following query: ${result}`);

  return result;
}
