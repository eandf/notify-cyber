// this is a custom React hook that fetches paginated data from the database
// this is used for the infinite scrolling on the home page
// based on this video: https://www.youtube.com/watch?v=JWlOcDus_rs&t=1526s

import appConfig from "@/app.config";
import getEvents from "@/src/backend/getEvents";
import { Settings } from "@/src/providers/SettingsContext";
import { useEffect, useState } from "react";

export default function usePaginatedDatabaseData(
  cursor = 0,
  settings: Settings
) {
  const [results, setResults] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isError, setIsError] = useState(false);
  const [error, setError] = useState<any>({});
  const [hasNextPage, setHasNextPage] = useState(false);

  useEffect(() => {
    setResults([]);
  }, [settings]);

  useEffect(() => {
    setIsLoading(true);
    setIsError(false);
    setError({});

    const controller = new AbortController();
    const { signal } = controller;

    const payload = {
      sources: settings.selectedSources,
      filter: settings.keywords,
      after: Math.floor(
        Date.now() / 1000 - appConfig.numDaysBack * 24 * 60 * 60
      ),
    };

    getEvents(
      appConfig.databasePageSize,
      cursor,
      payload,
      settings.searchString || ""
    )
      .then((events) => {
        setResults((prev) => {
          try {
            // this is probably not good, but sometimes the hook double fetches
            // and this was the easiest way to prevent that from causing issues
            const newData = events.filter(
              (d: any) => !prev.some((p) => p.id === d.id)
            );
            return [...prev, ...newData];
          } catch(err) {
            console.log(`error filtering: ${err}`)
            return prev
          }
        });
        setHasNextPage(Boolean(events.length));
        setIsLoading(false);
      })
      .catch((e) => {
        setIsLoading(false);
        if (signal.aborted) {
          return;
        }
        setIsError(true);
        setError({ message: e.message });
        console.log(e.response.data);
      });

    return () => {
      controller.abort();
    };
  }, [cursor, settings]);

  return { isLoading, isError, error, results, hasNextPage };
}
