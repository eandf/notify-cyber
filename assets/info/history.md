# History Of Notify-Cyber

## Events

- In December 2019, Mehmet became really paranoid about cyber security after discovering how the hardware/software that people use everyday is being exploited everyday by criminals who want to hurt others.
- In 2021, Mehmet started looking into ways to automate getting information about the latest cyber security news. He thought, by keeping yourself up to date about the latest cyber security news, is the best way most people can protect themselves from hackers/criminals.
- On around February 11, 2022, Mehmet and Dylan started a project called thn-discord-bot (TDB) which can be viewed here: https://github.com/MehmetMHY/thn-discord-bot
  - This was basically an earlier version of notify-cyber. It was a Discord bot that would get the latest cyber security news from "The Hacker News" and post them on a Discord server. There was a channel for all the news then 4 "filter" channels. These filter channels were for "Google", "Microsoft", "Apple", and "Linux". They would contain news related to their names.
  - While this project was running, there were around 10 to 20 people in the Discord server. But most people had the server muted and most of these people were classmates and/or friends.
  - In May 2022, the service was shut down and the Discord server was deleted. The code was then made open source on GitHub.
  - The main things learned with this project were the following:
    - Discord sucks at measuring engagement.
    - A good amount of people did not use Discord as their main notification platform.
    - A lot of people muted the channel and most people did not think the filter channels were that useful.
    - People wanted to make their own filters, not just be limited to 4 options.
- On April 21, 2022, this repo was made: https://github.com/MehmetMHY/thn-api
  - This repo contained the "The Hacker News" web scraper that was developed for the Discord bot. It was made in the hopes that it would help some people out (if needed).
- On around January 20, 2023 notify-cyber (NC) was created. It was initially developed for a Hackathon hosted by Courier on the Devpost platform. As the Hackathon went on, Mehmet and Dylan dropped the Hackathon because they confirmed that Courier's API is NOT ideal/designed-for what notify-cyber is trying to do.
- On around February 17, 2023, Mehmet and Dylan brought this project back to life and decided to make this into a product rather than just a project for a Hackathon.
- The main logo for Notify-Cyber started development on 3-10-2023. The exact date the logo was "completed" is not known but it's estimated that the logo was completed around 3-13-2023 and was modified here and there until 4-27-2023. The logo was created through these methods:
  - The "draft" for the logo was generated through OpenAI's DALL-E-2 with the following prompt:
    ```
    A picture of a bird carrying a news paper
    ```
  - The logo was then lightly edited and cleaned up by Mehmet on MacOS using Preview, Google Drawing, and Screenshot.
- On 06/11/2023 (June 11, 2023), Dylan officially left the Notify-Cyber project. Dylan did all of the frontend code for Notify-Cyber up to this point.

## Technical Events

- On 6-13-2023, Notify-Cyber was down for an unknown amount of time (most likely a few hours) because Vercel was running into region issues on the cloud side due to an AWS issue. The issue was resolved by changing Notify-Cyber's server's region and redeploying the app in Vercel. You can view Vercel's report here: https://www.vercel-status.com/incidents/cqkdqrzqkspm
- On 6-22-2023, I (Mehmet) deleted some very old 2013 CVE data from the Postgres database. These rows were never meant to be in the database, they were added by mistake. In doing this, the collector's get_all_data() function broke. This resulted in the collector NOT knowing what articles it already added, resulting in over 16,000 duplicated rows being added to the database. The DB row count went from around 32,000 to around 48,000. This was an issue because duplicated data is not great for the feed and there is a 500MB limit for the free plan for Supabase, so every hour this issue will generate over 16,000 new rows in the database since the CVE updating system in the Collector is not optimized. Thankfully this issue only ran live for a little over 1 hour, so only (over) 16,000 duplicated rows was created. The issue was resolved after I did some testing and came up with a better version of get_all_data() which more reliably allowed collector to know what articles it already added to the db. With the fix being added, I then used ChatGPT to make me a SQL query to get ALL duplicated data in the Postgres DB. I exported the output of that command as a csv file, then made a python script that safely extracted all the duplicated data's row ID(s). After getting all the duplicates row ID(s), the python script then made a custom SQL DELETE query. I ran this delete query in the database, through Supabase, which removed all the duplicated data. After all of this, I then updated the collector code in the Raspberry Pi and started the collector up again. From there, the site went live again.
  - This event resulted in a 4 to 6 hours down time. This was due to the fact that it occurred in the middle of the day while I was working and while I was dealing with some Tesla service stuff.

## Milestones and Optimizations

- On November 19, 2024, the waitlist signup count reached over 160. Total views as of April 26, 2024: Visitors: 14,169; Page Views: 38,133. Additionally, NC's monthly costs were reduced from $38.85 to $3.10 per month—a 12.5x reduction, saving $35.75 per month or $429.00 per year. The main cost saver was switching from hosting the collector in the cloud through Linode to hosting it on my personal Raspberry Pi.
- On October 4, 2025, total visitors reached 17,132 (page views not recorded). The waitlist signup count was exactly 160 as of October 2025.
