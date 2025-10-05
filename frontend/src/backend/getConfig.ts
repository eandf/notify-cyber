// function to get info about the database configuration

"use server"; // make sure this only runs on the server

import config from "@/src/backend/config";
import logger from "@/src/backend/logger";

// this must be async since it runs on the server
export default async function getConfig() {
  const apiPublicConfig = {
    valid_sources: config.valid_sources,
    max_array_str_size: config.max_array_str_size,
  };
  logger.info(
    `the endpoint config/ is returning the following config: ${JSON.stringify(
      apiPublicConfig
    )}`
  );

  return apiPublicConfig;
}
