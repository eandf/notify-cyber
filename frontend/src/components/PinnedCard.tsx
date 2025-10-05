// this react component renders the pinned card that appears at the
// top of the list of articles

// if you want to edit the content of the pinned card, you will need to edit
// this component direclty

"use client"; // make sure this component is only rendered on the client

import { CloseIcon } from "@/src/components/svg";
import formatEpochAsDate from "@/src/lib/formatEpochAsDate";
import styles from "@/src/styles/PinnedCard.module.css";
import Link from "next/link";
import { useEffect, useState } from "react";

export default function PinnedCard({
  setShow,
}: {
  setShow: (b: boolean) => void;
}) {
  const [isMounted, setIsMounted] = useState<boolean>(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  return isMounted ? (
    <div className={styles.pin_container} key={-1}>
      <span className={styles.pin_title}>
        <Link href="/about">Welcome to Notify Cyber!</Link>
        <button
          className={styles.pin_button}
          onClick={() => {
            setShow(false);
          }}
        >
          <CloseIcon style={{ fontSize: "2em", fill: "white" }} />
        </button>
      </span>
      <span className={styles.pin_date}>
        {formatEpochAsDate(1736278033, navigator.language)}
      </span>
      <p>
      Discover the latest cybersecurity news from the past 7 days, gathered from various sources, all in one place! Join our{" "}
        <a href="https://forms.gle/qcJsgfu8BZJJvSAQ8" target="_blank" rel="noopener noreferrer">
          waitlist
        </a> for possible future updates/features!
      </p>
    </div>
  ) : null;
}