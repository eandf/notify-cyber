// this react component renders the navbar that appears at the top of the page
// note that the Next.js <Link /> component is used instead of <a> tags
// this allows Next.js to preload links

import appConfig from "@/app.config";
import { useOutsideClickListener } from "@/src/hooks";
import styles from "@/src/styles/Navbar.module.css";
import Image from "next/image";
import Link from "next/link";
import { useRef, useState } from "react";

export default function Navbar() {
  // these variables are for expanding / collapsing the navbar on mobile devices
  const [isExpanded, setIsExpanded] = useState<boolean>(false);
  const buttonRef = useRef<HTMLButtonElement | null>(null);
  const ref = useOutsideClickListener<HTMLUListElement>(() => {
    setIsExpanded(false);
  }, [buttonRef]);

  return (
    <header className={styles.header}>
      {/* link to skip navbar when using keyboard to interact with the page */}
      <a
        href="#main-content"
        id="skip-navigation"
        className={styles.skip_navigation_link}
      >
        Skip Navigation
      </a>
      <nav className={styles.nav} aria-label="Main Navigation">
        <Link href="/" className={styles.logo_link}>
          <div className={styles.img_container}>
            <Image
              src="/nc_logo.svg"
              alt="The Notify Cyber logo, an cartoon image of a bird's head surrounded a circular black border"
              fill={true}
              style={{ objectFit: "contain" }}
            />
          </div>
          <h1 className={styles.logo_text_container}>
            <span>Notify</span>
            <span>Cyber</span>
          </h1>
        </Link>
        <ul
          ref={ref}
          className={`${styles.ul} ${isExpanded ? styles.show : ""}`}
        >
          <li>
            <Link href="/about">About</Link>
          </li>
        </ul>
        <button
          ref={buttonRef}
          className={`${styles.nav_toggle} ${
            isExpanded ? styles.nav_toggle_show : ""
          }`}
          onClick={() => {
            setIsExpanded((prev) => !prev);
          }}
        >
          <div></div> {/* DO NOT REMOVE this div becomes the hamburger icon*/}
        </button>
      </nav>
    </header>
  );
}
