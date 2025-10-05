// this react component renders the list of articles with infinite scrolling
// parts of this code based on: https://www.youtube.com/watch?v=JWlOcDus_rs&t=1526s

"use client"; // make sure this component is only rendered on the client

import { Article, LoadingSpinner, PinnedCard } from "@/src/components";
import { useLocalStorage, usePaginatedDatabaseData } from "@/src/hooks";
import SettingsContext from "@/src/providers/SettingsContext";
import styles from "@/src/styles/ArticleList.module.css";
import crypto from "crypto";
import { useCallback, useContext, useEffect, useRef, useState } from "react";
import ReactDomServer from "react-dom/server";
import SimpleBar from "simplebar-react";
import "simplebar-react/dist/simplebar.min.css";

export default function ArticleList() {
  const [paginationCursor, setPaginationCursor] = useState(0);
  const { settings } = useContext(SettingsContext);

  const { isLoading, isError, error, results, hasNextPage } =
    usePaginatedDatabaseData(paginationCursor, settings);

  const intersectionObserver = useRef<IntersectionObserver | null>(null);

  const lastArticleRef = useCallback(
    (article: any) => {
      if (isLoading) return;
      if (intersectionObserver.current)
        intersectionObserver.current.disconnect();

      intersectionObserver.current = new IntersectionObserver((articles) => {
        if (articles[0].isIntersecting && hasNextPage) {
          setPaginationCursor(results[results.length - 1].id);
        }
      });

      if (article) intersectionObserver.current.observe(article);
    },
    [isLoading, hasNextPage, results]
  );

  const [isMounted, setIsMounted] = useState<boolean>(false);

  // the hash of the pinned article is used as the validation string
  // so that the value of showPin will be invalidated if any part of
  // the pinned article changes
  const [showPin, setShowPin] = useLocalStorage<boolean>(
    "showPin",
    true,
    [true, false],
    crypto
      .createHash("sha256")
      .update(
        ReactDomServer.renderToString(
          <PinnedCard key="-1" setShow={(b: boolean) => {}} />
        )
      )
      .digest("hex")
  );

  useEffect(() => {
    setIsMounted(true);
    setPaginationCursor(0);
  }, []);

  useEffect(() => {
    setPaginationCursor(0);
  }, [settings]);

  if (isError) return <div>Error: {error.message}</div>;

  const content = results.map((article, index) => {
    if (results.length === index + 1) {
      return (
        <Article ref={lastArticleRef} key={article.id} article={article} />
      );
    }
    return <Article key={article.id} article={article} />;
  });

  if (isMounted && showPin) {
    content.unshift(<PinnedCard key="-1" setShow={setShowPin} />);
  }

  return (
    <SimpleBar style={{ width: "100%", height: "100%" }}>
      <div className={styles.article_container}>
        <div className={styles.gradient}></div>
        {isLoading && (
          <div className={styles.spinner_container}>
            <LoadingSpinner />
          </div>
        )}

        {(showPin && content.length === 1) ||
        (!showPin && content.length === 0) ? (
          <div className={styles.no_res_msg}>No Results</div>
        ) : (
          content
        )}
      </div>
    </SimpleBar>
  );
}
