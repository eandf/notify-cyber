// this react component renders the search box, source selection dropdown,
// and rss button

"use client";

import { CheckboxList, Dropdown, SearchBox } from "@/src/components";
import { RSSIcon } from "@/src/components/svg";
import SettingsContext, { Settings } from "@/src/providers/SettingsContext";
import styles from "@/src/styles/Filterbar.module.css";
import Link from "next/link";
import { useContext, useEffect, useState } from "react";

interface Item {
  name: string;
  id: string;
}

export default function Filterbar({ sources }: { sources: Item[] }) {
  const { settings, updateSelectedSources, updateSearchString } =
    useContext(SettingsContext);

  const [activeDropdownId, setActiveDropdownId] = useState<number>(-1);
  const [previousSettings, setPreviousSettings] = useState<Settings>();

  useEffect(() => {
    if (activeDropdownId !== -1) return;

    const settingsUpdated =
      JSON.stringify(settings) !== JSON.stringify(previousSettings);

    if (settingsUpdated) {
      setPreviousSettings(settings);
    }
  }, [activeDropdownId, settings, previousSettings]);

  return (
    <div className={styles.filtercontainer}>
      <div className={styles.searchbar}>
        <SearchBox onSubmit={updateSearchString} />
      </div>

      <Dropdown
        id={0}
        activeDropdownId={activeDropdownId}
        setActiveDropdownId={setActiveDropdownId}
        label="Sources"
        content={
          <CheckboxList
            items={sources}
            selectedItems={settings.selectedSources}
            setSelectedItems={updateSelectedSources}
          />
        }
      />
      <Link
        className={styles.rssbutton}
        href={`/rss?${new URLSearchParams({
          sources: settings.selectedSources,
        })}`}
      >
        <RSSIcon
          style={{
            width: "100%",
            height: "100%",
            fill: "#ffa500",
            paddingRight: "2px",
          }}
        />
      </Link>
    </div>
  );
}
