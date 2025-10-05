// this react component renders a loading spinner
// most of the work actuall creating the spinner is in the css

import styles from "@/src/styles/LoadingSpinner.module.css";

export default function LoadingSpinner() {
  return <span className={styles.spinner}></span>;
}
