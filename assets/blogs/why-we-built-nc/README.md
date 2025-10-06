# Why We Built Notify Cyber

**May 29, 2023** • **_Mehmet Yilmaz_**

<p align="center">
  <img width="1000" src="./thumbnail.png">
</p>

[Notify-Cyber](https://notifycyber.com/) (NC) is a website that aggregates cybersecurity news from multiple sources, summarizes those articles, and lists them all in a simple news feed, providing a fast reading experience for staying up to date in the cybersecurity landscape. NC was co-developed by Mehmet Yilmaz (me), who handled the backend development, and Dylan Eck, who took charge of the frontend implementation. This article, originally posted on Medium on May 29, 2023, provides insights into Notify-Cyber and the motivations behind its creation. The original article, titled [From Unaware to Prepared: Navigating the Cybersecurity Landscape with Notify-Cyber](https://medium.com/@notify-cyber/from-unaware-to-prepared-navigating-the-cybersecurity-landscape-with-notify-cyber-37d804f8ef96), was written by me, Mehmet Yilmaz, and posted under [@notify-cyber](https://medium.com/@notify-cyber). I never liked the original title because it is too long, so I shortened it for this blog re-upload to: **_Why We Built Notify-Cyber_**

## Abstract

- Critical cybersecurity threats often go unnoticed by the general public until they become catastrophic, highlighting a gap in awareness.
- As generative AI tools like ChatGPT emerge, staying informed about cybersecurity news and vulnerabilities becomes increasingly crucial.
- Notify-Cyber is a service that aims to keep the general public more aware of cybersecurity threats by aggregating the latest cybersecurity news from various sources into one news feed. Notify-Cyber can be accessed here: https://notifycyber.com/
- Notify-Cyber plans to launch a personalized email alert service which will provide timely notifications about relevant cybersecurity vulnerabilities. The waitlist can be joined at: https://notifycyber.com/join

## Article

In today’s digital world, cybersecurity is more important than ever. We rely on our devices for everything from work to entertainment, making us constantly vulnerable to cyber threats. Unfortunately, many people only pay attention to cybersecurity issues when they become catastrophic, such as large data breaches or high-profile ransomware attacks. This lack of awareness leaves individuals susceptible to subtle yet equally dangerous threats.

One such widely unnoticed threat was the "IndexedDB API information leak" vulnerability in Apple’s Safari browser. The vulnerability was discovered and reported by fraud protection software company FingerprintJS in November 2021 and only affected the Safari web browser. In this vulnerability, when a user visits a website that takes advantage of this vulnerability, the website gains the ability to access the user’s browsing history across various tabs and/or windows. This ultimately could allow the website to uniquely and precisely identify a user based on their activity on other websites, like their Google account [[1]](https://fingerprint.com/blog/indexeddb-api-browser-vulnerability-safari-15/). The vulnerability was later patched by Apple in January 2022 [[2]](https://safarileaks.com/).

<div style="text-align: left;">
  <a href="https://www.youtube.com/watch?v=Z7dPeGpCl8s">
    Fingerprint - How IndexedDB in Safari 15 leaks your browsing activity (in real time)
  </a>
</div>

<p align="left"><em>YouTube video by Fingerprint demonstrating the IndexedDB vulnerability</em></p>

During the intervening period, we noticed that many Safari users remained unaware of this vulnerability. Although the issue was eventually covered by various news sources, including The Verge, The Hacker News, Macworld, TechCrunch, The Register, Screen Rant, and SiliconANGLE. To us, it still didn’t receive adequate attention by the general public.

Upon discovering this vulnerability in January 2022, we discussed it with our family, friends, and peers, only to realize that most of them were unaware of it until we brought it up. Subsequently, upon learning about the vulnerability, they promptly switched to a different browser until we confirmed that the issue was resolved.

This event highlighted the general lack of knowledge among people regarding cybersecurity events and vulnerabilities. However, it also demonstrated the widespread concern and continued importance placed on security and privacy, despite limited awareness in this area. It is crucial that individuals take responsibility for their own digital security and stay informed about the latest cyber threats and vulnerabilities.

With the emergence of generative AI tools like ChatGPT, staying informed about cybersecurity news and vulnerabilities becomes increasingly important. These tools have the potential to rapidly detect vulnerabilities, leading to the potential of an accelerated rise in exploits like the exploit we discussed earlier [[3]](https://www.youtube.com/watch?v=xoVJKj8lcNQ). Therefore, staying updated on cybersecurity news and emerging threats is now more critical than ever before.

<div style="text-align: left;">
  <a href="https://www.youtube.com/watch?v=xoVJKj8lcNQ">
    <b>YouTube - The Social Dilemma (2020) - Official Trailer</b>
  </a>
</div>

<p align="left"><em>At timestamps 00:23:00-00:23:31 and 00:23:31-00:35:48, Tristan Harris and Aza Raskin demonstrate the potential risks AI technologies can pose in the realm of cybersecurity.</em></p>

To protect yourself, it is essential to stay informed about cybersecurity events related to the software you use on a daily basis. This is where our platform, Notify-Cyber (https://notifycyber.com/), comes in. Notify-Cyber is an all-in-one cybersecurity news platform that simplifies staying informed about cybersecurity events. Notify Cyber aggregates the latest cybersecurity news from various sources all into one news feed. Making it easy to get a general overview of the current cybersecurity news scape.

When you visit Notify-Cyber (https://notifycyber.com/), you are presented with a news feed containing the latest cybersecurity news aggregated from the past 7 days. Each news posting includes a summary for quick reading. Additionally, there is a search bar to help you find specific postings by keywords.

<p align="center">
  <img width="1000" src="./demo.gif">
  <em>Simple demo of Notify Cyber</em>
</p>

The ultimate goal of Notify-Cyber is to keep you aware and updated about vulnerabilities that affect software and hardware that you care about. Currently, Notify-Cyber serves as an aggregation of the latest cybersecurity news from multiple sources. Our plan is to expand the capabilities of Notify-Cyber by introducing an email service that sends users timely notifications about vulnerabilities they care about. This service will not be a newsletter but more like personal alerts. Emails will only be sent exclusively upon the discovery of relevant cybersecurity events pertaining to each individual. So depending on the user’s preferences, they might receive daily emails or just one email every few months. If you are interested in using such a service, you can join our waitlist here: https://notifycyber.com/join.

We urge everyone to keep themselves aware of the current cybersecurity landscape, recognizing the pivotal role each of us plays in our own digital safety. Always remember, your cybersecurity begins with you. We invite you all to check out Notify Cyber: https://notifycyber.com/

```
This article was written by the Notify-Cyber team with the help
of ChatGPT (GPT-3.5). The final draft was proofread, fact checked,
and edited by the Notify-Cyber team.
```

## Citations

- [1] M. Bajanik, "Exploiting IndexedDB API Information Leaks in Safari 15," Fingerprint Blog RSS, https://fingerprint.com/blog/indexeddb-api-browser-vulnerability-safari-15/ (accessed May 29, 2023).
- [2] "Safari 15 indexeddb leaks," Safari 15 IndexedDB Leaks, https://safarileaks.com/ (accessed May 29, 2023).
- [3] Center for Humane Technology, "The A.I. Dilemma — March 9, 2023," YouTube, https://www.youtube.com/watch?v=xoVJKj8lcNQ (accessed May 29, 2023). Timestamps 00:23:00-00:23:31 and 00:23:31-00:35:48
