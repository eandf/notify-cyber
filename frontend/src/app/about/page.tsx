// this react component renders the about page.
// if you want to modify the content of the about page, you will need to
// directly modify this component

"use client"; // make sure this only renders on the client

import { Card, Navbar } from "@/src/components";
import { MediumIcon, TwitterIcon } from "@/src/components/svg";
import styles from "@/src/styles/AboutPage.module.css";
import Image from "next/image";
import Link from "next/link";
import { use100vh } from "react-div-100vh";

export default function MorePage() {
  const viewportHeight = use100vh();
  const height = viewportHeight ? viewportHeight : "100vh";

  return (
    <div className={styles.container} style={{ height: height }}>
      <Navbar />
      {/* id is set so skip navignation link in navbar works properly*/}
      <main className={styles.main} id="main-content">
        <div className={styles.img_container}>
          <Image
            src="/logo_transparent.png"
            alt="Notify Cyber Logo"
            fill={true}
            style={{ objectFit: "contain" }}
          ></Image>
        </div>
        <Card>
          <div className={styles.card_content}>
            <div className={styles.title}>About</div>
            <p className={styles.abouttext}>
              Notify Cyber is a platform designed to enhance public awareness about cybersecurity threats by aggregating news from multiple reputable sources into a single, easily accessible feed. It aims to provide users with up-to-date and comprehensive coverage of cybersecurity news and vulnerabilities, enabling both individuals and organizations to stay informed. The platform&apos;s design allows users to scroll through articles chronologically, from the latest to older entries, making it simple to monitor current cybersecurity events as well as refer back to historical data when needed. This effort aims to address the often-overlooked aspect of cybersecurity awareness, encouraging proactive engagement with digital security issues. Learn more about Notify-Cyber&apos;s origins with our <Link href="https://mehmetmhy.com/blogs/why-we-built-nc/">blog post</Link>. And if you are interested, join our <Link href={process.env.NEXT_PUBLIC_WAITLIST_URL}>waitlist</Link> for possible future features!
            </p>
          </div>
        </Card>
        <Card>
          <div className={styles.card_content}>
            <span className={styles.title}>Check us Out!</span>
            <div className={styles.link_container}>
              <a href="https://twitter.com/notify_cyber" target="_blank">
                <TwitterIcon className={styles.icon} />
              </a>
              <a href="https://medium.com/@notify-cyber" target="_blank">
                <MediumIcon className={styles.icon} />
              </a>
            </div>
          </div>
        </Card>
      </main>
    </div>
  );
}
