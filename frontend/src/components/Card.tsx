// this react component renders a simple card
// the card can hold any arbitrary react component inside of itself

import styles from "@/src/styles/Card.module.css";
import { ReactNode } from "react";

export default function Card({ children }: { children: ReactNode }) {
  return <div className={styles.container}>{children}</div>;
}
