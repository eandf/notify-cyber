// SettingsProvider creates a context containing state variables related to the user's search and filtering settings. These variables are accessible to all children of SettingsProvider
// see: https://react.dev/learn/passing-data-deeply-with-context

"use client";

import { useLocalStorage } from "@/src/hooks";
import { createContext, useState } from "react";

export interface Settings {
  selectedSources: string[];
  keywords: string[];
  searchString: string | null;
}

const SettingsContext = createContext<any>({});

export function SettingsProvider({ children }: { children: any }) {
  // TODO: this shouldn't be hard coded, use src/backend/getConfig
  const [selectedSources, setSelectedSources] = useLocalStorage<string[]>(
    "selectedSources",
    ["caisa", "isg", "thn", "dr"],
    ["caisa", "dr", "thn", "isg", "cve"]
  );

  const [otherSettings, setOtherSettings] = useState<
    Omit<Settings, "selectedSources">
  >({
    keywords: [],
    searchString: null,
  });

  const settings = {
    selectedSources,
    ...otherSettings,
  };

  const setSettings = (newSettings: Settings) => {
    setSelectedSources(newSettings.selectedSources);
    setOtherSettings({
      keywords: newSettings.keywords,
      searchString: newSettings.searchString,
    });
  };

  const updateSelectedSources = (source: string, selected: boolean) => {
    setSelectedSources((prev: string[]) => {
      if (selected) {
        return [...prev, source];
      } else {
        return prev.filter((selectedItem: string) => selectedItem !== source);
      }
    });
  };

  const updateKeywords = (keyword: string) => {
    let newKeywords: string[];
    if (!otherSettings.keywords.includes(keyword)) {
      newKeywords = [...otherSettings.keywords, keyword];
    } else {
      newKeywords = otherSettings.keywords.filter(
        (kw: string) => kw !== keyword
      );
    }

    setOtherSettings((prevSettings) => ({
      ...prevSettings,
      ["keywords"]: newKeywords,
    }));
  };

  const updateSearchString = (searchString: string) => {
    setOtherSettings((prevSettings) => ({
      ...prevSettings,
      ["searchString"]: searchString,
    }));
  };

  return (
    <SettingsContext.Provider
      value={{
        settings,
        setSettings,
        updateSelectedSources,
        updateKeywords,
        updateSearchString,
      }}
    >
      {children}
    </SettingsContext.Provider>
  );
}

export default SettingsContext;
