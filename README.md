<h1 align="center">Notify Cyber</h1>

<div align="center">
  <img src="./assets/images/background2.png" alt="Notify Cyber Logo" width="1000"/>
</div>

## Table of Contents

- [Overview](#overview)
- [Project Vision](#project-vision)
- [Dataset](#dataset)
- [Core Components](#core-components)
  - [Frontend](#frontend)
  - [Collector](#collector)
  - [Database](#database)
  - [API](#api)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
- [Project Status](#project-status)
- [License](#license)

## Overview

Notify Cyber was a dynamic cybersecurity news aggregation platform created by **Mehmet Yilmaz** and **Dylan Eck** in **February 2023**. It operated from **June 1, 2023** to **October 5, 2025** where it successfully provided timely and relevant security news to **over 17,000 visitors**. The project gained initial visibility through a popular Reddit post and created numerous opportunities for its developers. This repository now hosts a static, open source version of the original website, preserving its design and functionality as a snapshot in time.

## Project Vision

The vision behind Notify Cyber was to create a centralized and personalized platform for cybersecurity news. We aimed to simplify how professionals and enthusiasts stay informed about the latest digital threats and vulnerabilities. By aggregating information from trusted sources and offering powerful filtering capabilities, the platform allowed users to receive a newsfeed tailored to the hardware and software they care about most, complete with email notifications and a robust search engine. For a deeper dive into the motivation and story behind Notify Cyber's creation, read the [original launch blog post](./assets/blogs/why-we-built-nc/README.md).

## Dataset

The entire database of cybersecurity news articles collected throughout Notify Cyber's operation is available in two locations: [./docs/db.json](./docs/db.json) contains the dataset used for the static site, while [./assets/backups/backup_nc_1759690168.json.zip](./assets/backups/backup_nc_1759690168.json.zip) contains the complete, unfiltered database backup.

## Architecture Overview

Notify Cyber was built as a distributed system leveraging free-tier cloud services and local infrastructure. Here's how everything worked together:

**Domain & Hosting**: The domain was originally registered through Google Domains (now SquareSpace Domains). The entire frontend and all serverless functions were hosted on Vercel's free plan, which also provided web analytics for tracking site usage.

**Database**: A single PostgreSQL table hosted on Supabase's free tier served as the central data repository. This simple yet effective design stored all aggregated cybersecurity news articles with their metadata.

**Collector Infrastructure**: The collector ran 1-2 times daily to update the database. It was primarily hosted on a personal Raspberry Pi 3B+ at home, with failover to a Linode instance during travel. The collector operated as a Docker container on Debian-based Linux, using various scraping tools including requests, BeautifulSoup, cloudscraper, and newspaper3k. Notably, no browser-rendering scraping was required—all content was successfully extracted without JavaScript rendering.

**Data Sources & Processing**: Initially, the system cloned the entire [CVEProject/cvelist repository](https://github.com/CVEProject/cvelist) to parse thousands of JSON-formatted CVE records. However, this approach proved computationally intensive and was eventually replaced with more efficient request + BeautifulSoup methods. Article summarization evolved through three OpenAI models: starting with gpt-3.5-turbo, upgrading to gpt-3.5-turbo-16k for longer content, and finally settling on gpt-4o-mini for optimal cost and performance.

**Data Pipeline**: The collector would fetch raw article data, clean and normalize it, generate AI-powered summaries via OpenAI's API, and push the processed content directly to the Supabase database.

**API Purpose**: The Express-based API wasn't essential for Notify Cyber's core functionality. It was deployed primarily to enable other projects, such as [TARS](https://github.com/MehmetMHY/TARS), to easily consume the cybersecurity news database.

## Core Components

The Notify Cyber ecosystem consists of several key components working together to deliver a seamless user experience.

### Frontend

The user interface is a modern web application built with Next.js and React. It provides a clean, intuitive, and responsive design for browsing news articles. Key aspects of the frontend include an infinitely scrollable article list, robust search and filtering options, and a dedicated about page. The frontend was designed for easy deployment on **Vercel**.

### Collector

The collector is a Python based service responsible for populating our database. It systematically scrapes various cybersecurity news sources from the internet, processes the collected data for consistency, and structures it for storage. The collector is designed to run within a Docker container, ensuring a consistent and isolated environment for its operations. It can be deployed on cloud instances like **Linode** or on local hardware such as a **Raspberry Pi**.

### Database

A PostgreSQL database serves as the central repository for all aggregated news content. The primary table, `cybernews`, stores essential information for each article, including its source, URL, title, and publication date. The database schema is straightforward and optimized for efficient querying. A collection of SQL tools is available for database maintenance and analysis. This database in production was hosted on **Supabase**.

### API

Before continuing, please note that while this API was used for other projects, it is not required for Notify Cyber's core functionality. It is a lightweight Express-based API that provides endpoints for the frontend to interact with the database via Supabase. It supports fetching articles with pagination, retrieving configuration data, and intelligent search with stopword filtering. The API is designed to run as a serverless function on **Vercel**.

## Features

- **Centralized News Aggregation**: Fetches news from major cybersecurity sources into a single feed.
- **Advanced Search and Filtering**: Allows users to search for specific topics and filter articles by source.
- **Infinite Scroll**: Delivers a smooth and continuous browsing experience without pagination.
- **Retired Snapshot**: Preserves the original site design and a snapshot of the news data.
- **Open Source**: The entire codebase is available for the community to explore and learn from.

## Technology Stack

- **Frontend**: Next.js, React, TypeScript, CSS Modules
- **Backend Collector**: Python, Docker
- **Database**: PostgreSQL
- **API**: Node.js, Express.js
- **Deployment**: Vercel (Frontend & API), Linode (Collector)

## Getting Started

To get the full Notify Cyber platform running, you should set up the components in the following order. Each component has its own detailed setup instructions in its respective README file.

1.  **[Database](./database/README.md):** Begin by setting up the PostgreSQL database. This is the core data store for the application.

2.  **[API](./api/README.md):** Set up the API service to enable communication between the frontend and database.

3.  **[Frontend](./frontend/README.md):** Next, set up the Next.js frontend. This will provide the user interface for viewing the data.

4.  **[Collector](./collector/README.md):** Once the database, API, and frontend are ready, set up the collector to populate the database with news articles.

## Project Status

Notify Cyber was officially retired on **October 5, 2025**. The decision was made because the project could not achieve sufficient monetization to cover its ongoing maintenance and operational costs. This repository provides a static and open sourced version of the platform as a tribute to its legacy and a resource for the community. The domain will remain active to ensure continued access to this snapshot.

## License

This project is licensed under the **Apache License 2.0**. See the [LICENSE](LICENSE) file for details.
