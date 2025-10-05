/**
 * Basic Logger Library
 * 4-28-2023
 */

import moment from "moment";

function currentTimestamp(timezoneOffset: number | null = null): string {
  const format = "MM-DD-YYYY HH:mm:ss z";
  let timestamp = moment();

  if (timezoneOffset !== null) {
    timestamp = timestamp.utc().add(timezoneOffset, "hours");
  }

  let timestampStr: string = timestamp.format(format);

  return timestampStr;
}

function log(sev: number | null, msg: string) {
  // severity values are based off of Python's logger function(s)
  let sevStr = "";
  if (sev == 1) {
    sevStr = "DEBUG";
  } else if (sev == 2) {
    sevStr = "INFO";
  } else if (sev == 3) {
    sevStr = "WARNING";
  } else if (sev == 4) {
    sevStr = "ERROR";
  } else if (sev == 5) {
    sevStr = "CRITICAL";
  } else {
    sevStr = "NOTSET";
  }

  // all timestamps will be UTC
  let timestamp = currentTimestamp(0);
  let epoch = Date.now();

  let logMsg = `${timestamp} (${epoch} ms) [${sevStr}] ${msg}`;

  // only log/print to STDOUT
  console.log(logMsg);

  return;
}

function notset(msg: string) {
  log(null, msg);
  return;
}

function debug(msg: string) {
  log(1, msg);
  return;
}

function info(msg: string) {
  log(2, msg);
  return;
}

function warning(msg: string) {
  log(3, msg);
  return;
}

function error(msg: string) {
  log(4, msg);
  return;
}

function critical(msg: string) {
  log(5, msg);
}

// quick function to test all the log option functions
function test() {
  let testMsg: string = "Test log message...";
  notset(testMsg);
  debug(testMsg);
  info(testMsg);
  warning(testMsg);
  error(testMsg);
  critical(testMsg);
  return;
}

const logger = {
  notset: notset,
  debug: debug,
  info: info,
  warning: warning,
  error: error,
  critical: critical,
};

export default logger;
