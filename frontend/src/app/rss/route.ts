// this is the rss feed implementation
// since this file is called "route", it doesn't correspond to an actual page
// see https://nextjs.org/docs/getting-started/project-structure#app-routing-conventions

import appConfig from "@/app.config";
import getEvents from "@/src/backend/getEvents";
import { NextRequest } from "next/server";
import RSS from "rss";

// handle get requests to /rss
export async function GET(request: NextRequest) {
  const querySources = request.nextUrl.searchParams.get("sources");
  let sources: string[];
  if (querySources) {
    sources = querySources.split(",");
  } else {
    // TODO: should not be hard coded, get using src/backend/getConfig
    sources = ["caisa", "dr", "thn", "isg", "cve"];
  }

  const events = await getEvents(
    appConfig.rssFeedItemLimit,
    0,
    {
      sources: sources,
      filter: [],
      after: Math.floor(Date.now() / 1000 - 7 * 24 * 60 * 60),
    },
    ""
  );

  const feed = new RSS({
    title: "Notify Cyber",
    description: "",
    site_url: appConfig.deploymentURL,
    feed_url: `${appConfig.deploymentURL}/feed`,
    language: "en",
    pubDate: new Date(),
  });

  events.map((event: any) => {
    feed.item({
      title: event.title,
      url: event.url,
      date: new Date(event.recorded * 1000),
      description: event.details,
    });
  });

  return new Response(feed.xml(), {
    headers: {
      "content-type": "application/atom+xml; charset=utf-8",
    },
  });
}
