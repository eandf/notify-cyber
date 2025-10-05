// utility functions for interacting with the database

import config from "@/src/backend/config";
import logger from "@/src/backend/logger";
import { createClient } from "@supabase/supabase-js";

const validSourceIDs = config.valid_sources.map((source) => source.id);
const maxArrayStrSize = config.max_array_str_size;
const validInputKeys = config.valid_input_keys;
const PROJECT_URL = process.env.SUPABASE_URL || "";
const PROJECT_KEY = process.env.SUPABASE_SECRET_KEY || "";
const MAIN_TABLE = process.env.SUPABASE_MAIN_TABLE || "";

const supabase = createClient(PROJECT_URL, PROJECT_KEY);

interface Payload {
  after: number;
  sources: string[];
  filter: string[];
}

/**
 * Checks if a given string contains only characters from a predefined list of allowed Unicode characters.
 *
 * The function uses a regular expression to test if the input string matches a pattern of allowed characters,
 * including letters A-Z (uppercase and lowercase), numbers 0-9, underscore (_), trademark symbol (™), registered
 * trademark symbol (®), copyright symbol (©), plus sign (+), ampersand (&), dash (-), and various parentheses.
 * This function exists to help prevent SQL Injection Attack(s).
 *
 * @param {string} str - The input string to check for valid characters.
 * @returns {boolean} True if the input string contains only valid characters, false otherwise.
 */
function hasValidChars(str: string): boolean {
  const regex = /^[A-Za-z0-9_™®©+&\/\-\(\)\[\]\{\} ]+$/;
  return regex.test(str);
}

/**
 * Validates a payload object to ensure that it meets certain criteria - Made by ChatGPT (partly)
 *
 * Checks the object properties and values, and validates the "filter" property characters using `hasValidChars()`.
 * Ensures the "after" property is greater than a minimum accepted time, and that the "sources" property contains only
 * valid values as defined by the "validSources" object. Also validates that the payload object contains only valid
 * keys, and that the length of the "filter" property does not exceed a maximum size.
 *
 * @param {object} payload - The payload object to be validated.
 * @param {number} dayOffset - The number of days to offset the minimum accepted time (default is 3).
 * @returns {object|null} An object with an "error" property if the payload fails any tests, or null if it passes all tests.
 */
interface ValidatePayloadOuput {
  error: string | null;
}

function validatePayload(payload: Payload, dayOffset: number) {
  const output: ValidatePayloadOuput = { error: null };

  if (!payload.hasOwnProperty("after") || typeof payload.after !== "number") {
    output.error = "Invalid 'after' property: must be a number";
    return output;
  }

  if (!payload.hasOwnProperty("sources") || !Array.isArray(payload.sources)) {
    output.error = "Invalid 'sources' property: must be an array";
    return output;
  }

  for (const source of payload.sources) {
    if (!validSourceIDs.includes(source)) {
      output.error = `Invalid source '${source}': must be one of ${validSourceIDs}`;
      return output;
    }
  }

  if (!payload.hasOwnProperty("filter") || !Array.isArray(payload.filter)) {
    output.error = "Invalid 'filter' property: must be an array";
    return output;
  }

  for (let i = 0; i < payload.filter.length; i++) {
    if (typeof payload.filter[i] !== "string") {
      output.error = `Invalid filter item at index ${i}: must be a string`;
      return output;
    }
    if (!hasValidChars(payload.filter[i])) {
      output.error = `Invalid filter item at index ${i}: contains invalid characters`;
      return output;
    }
  }

  const minCurrentTime =
    Math.floor(Date.now() / 1000) - dayOffset * 24 * 60 * 60;
  if (payload.hasOwnProperty("after") && payload.after <= minCurrentTime) {
    output.error =
      "Invalid 'after' property: must be greater than the minimum accepted time";
    logger.error(
      `bad 'after' time provided: ${payload.after} [ NOT >= ] ${minCurrentTime}`
    );
    return output;
  }

  for (const input of Object.keys(payload)) {
    if (!validInputKeys.includes(input)) {
      output.error = `Invalid property: '${input}' is not a valid input key`;
      return output;
    }
  }

  if (payload.filter.join("").length > maxArrayStrSize) {
    output.error = `Invalid 'filter' property: maximum allowed length exceeded (${maxArrayStrSize} characters)`;
    return output;
  }

  return output;
}

/**
 * Builds and executes an SQL query based on the input payload, limit, and last_id.
 *
 * The function constructs a query to fetch data from the main table in the database, applying
 * filters and conditions based on the input parameters. It returns the data as an array of
 * objects. In case of any errors, the function logs the error and returns 'undefined'.
 *
 * @param {Object} payload - The input object containing query conditions.
 * @param {string[]} payload.sources - Array of data sources to filter results.
 * @param {string} payload.after - The minimum 'recorded' date for fetched records.
 * @param {string[]} payload.filter - Array of strings to filter results by title (case insensitive).
 * @param {number} limit - The maximum number of records to return.
 * @param {number} last_id - The starting record ID for pagination.
 * @returns {Promise<Object[]|undefined>} A Promise that resolves to an array of objects containing the fetched data,
 *                                        or 'undefined' if an error occurs.
 */
async function buildSQLQuery(payload: Payload, limit: number, last_id: number) {
  try {
    const { sources, after, filter } = payload;

    let query = supabase
      .from(MAIN_TABLE)
      .select("id, source, url, title, date, recorded, details")
      .in("source", sources)
      .gte("recorded", after)
      .order("id", { ascending: false })
      .limit(limit);

    if (last_id > 0) {
      query.lt("id", last_id);
    }

    if (filter.length > 0) {
      filter.forEach((element) => {
        query.or(`title.ilike.%${element}%, details.ilike.%${element}%`);
      });
    }

    const { data, error } = await query;

    if (error) {
      logger.error(`Error while fetching data: ${JSON.stringify(error)}`);
      return undefined;
    }

    return data;
  } catch (err) {
    logger.error(`Unexpected error occurred in filter query function: ${err}`);
    return undefined;
  }
}

/**
 * Fetches the latest ID from the main table in the database.
 *
 * The function sends a query to the database to select the 'id' column, ordering the results in descending order,
 * and limiting the results to just one record. This way, it retrieves the highest ID value available.
 * In case of any errors, the function logs the error and returns -1.
 *
 * @returns {Promise<number>} A Promise that resolves to the latest ID as a Number, or -1 if an error occurs.
 */
async function getLatestID() {
  console.log("MAIN_TABLE:", MAIN_TABLE);
  let query = supabase
    .from(MAIN_TABLE)
    .select("id")
    .order("id", { ascending: false })
    .limit(1);

  const { data, error } = await query;
  if (error) {
    logger.error(`Error while fetching data id: ${JSON.stringify(error)}`);
    throw error;
  }
  return data[0].id;
}

const util = {
  validatePayload: validatePayload,
  hasValidChars: hasValidChars,
  buildSQLQuery: buildSQLQuery,
  getLatestID: getLatestID,
};

export default util;
