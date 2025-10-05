// this react component renders a simple search box with a magnifying glass
// icon to the left

// the component takes a function as input and calls that function when the
// the search box is non-empty, focused, and the enter key is pressed.

import { SearchIcon } from "@/src/components/svg";
import styles from "@/src/styles/SearchBox.module.css";
import { FormEvent, KeyboardEvent, useState } from "react";

interface SearchBoxProps {
  onSubmit: (input: string | null) => void;
}

export default function SearchBox({ onSubmit }: SearchBoxProps) {
  const [input, setInput] = useState<string>("");

  const inputOnChange = (event: FormEvent<HTMLInputElement>) => {
    const { target } = event;
    if (!target) return;
    const newValue = (target as HTMLInputElement).value;
    setInput(newValue);
    if (newValue === "") {
      onSubmit(null);
    }
  };

  const inputOnKeyDown = (event: KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Enter" && input !== "") {
      onSubmit(input);
    }
  };

  return (
    <div className={styles.container}>
      <SearchIcon className={styles.icon} />
      <input
        className={styles.input}
        type="text"
        value={input}
        onChange={inputOnChange}
        onKeyDown={inputOnKeyDown}
      />
    </div>
  );
}
