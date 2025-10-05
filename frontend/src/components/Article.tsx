// this react component renders a single article

import React, { ForwardedRef } from "react";

import apiConfig from "@/src/backend/config";
import { Card } from "@/src/components";
import formatEpochAsDate from "@/src/lib/formatEpochAsDate";
import styles from "@/src/styles/Article.module.css";

export interface ArticleProps {
  article: {
    source: string;
    title: string;
    date: string;
    details: string;
    recorded: number;
    url: string;
  };
}

const Article = (
  { article }: ArticleProps,
  ref: ForwardedRef<HTMLDivElement>
): JSX.Element => {
  const articleBody = (
    <Card>
      <h2 className={styles.title}>
        <a href={article.url}>{article.title}</a>
      </h2>
      <span className={styles.subtitle}>
        {`${formatEpochAsDate(article.recorded, navigator.language)} - ${
          apiConfig.valid_sources.find((source) => source.id == article.source)
            ?.name
        }`}
      </span>
      {article.details !== "None" && <p>{article.details}</p>}
    </Card>
  );

  return ref ? <div ref={ref}>{articleBody}</div> : <div>{articleBody}</div>;
};

export default React.forwardRef(Article);
