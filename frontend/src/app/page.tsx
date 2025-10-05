// this react component renders the home page

"use client"; // make sure this only renders on the clien

import getConfig from "@/src/backend/getConfig";
import { ArticleList, Filterbar, Navbar } from "@/src/components";
import { SettingsProvider } from "@/src/providers/SettingsContext";
import styles from "@/src/styles/HomePage.module.css";
import { useEffect, useState } from "react";
import { use100vh } from "react-div-100vh";

export default function HomePage() {
  const [validSources, setValidSources] = useState<
    {
      name: string;
      id: string;
    }[]
  >([]);
  const viewportHeight = use100vh();
  const height = viewportHeight ? viewportHeight : "100vh";

  useEffect(() => {
    getConfig().then((config) => {
      setValidSources(config.valid_sources);
    });
  }, []);

  return (
    <div className={styles.container} style={{ height: height }}>
      <Navbar />
      {/* id is set so skip navignation link in navbar works properly*/}
      <main className={styles.main} id="main-content">
        <SettingsProvider>
          <Filterbar sources={validSources} />
          <ArticleList />
        </SettingsProvider>
      </main>
    </div>
  );
}
