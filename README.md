<h1 align="center">Notify Cyber</h1>

<div align="center">
  <img src="./assets/images/background2.png" alt="Notify Cyber Logo" width="1000"/>
</div>

## Table of Contents

- [Overview](#overview)
- [Project Vision](#project-vision)
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

Notify Cyber was a dynamic cybersecurity news aggregation platform created by **Mehmet Yilmaz** and **Dylan Eck** in **May 2023**. It operated from **June 1, 2023** to **October 31, 2025** where it successfully provided timely and relevant security news to over 17,000 visitors. The project gained initial visibility through a popular Reddit post and created numerous opportunities for its developers. This repository now hosts a static, open source version of the original website, preserving its design and functionality as a snapshot in time.

## Project Vision

The vision behind Notify Cyber was to create a centralized and personalized platform for cybersecurity news. We aimed to simplify how professionals and enthusiasts stay informed about the latest digital threats and vulnerabilities. By aggregating information from trusted sources and offering powerful filtering capabilities, the platform allowed users to receive a newsfeed tailored to the hardware and software they care about most, complete with email notifications and a robust search engine.

## Core Components

The Notify Cyber ecosystem consists of several key components working together to deliver a seamless user experience.

### Frontend

The user interface is a modern web application built with Next.js and React. It provides a clean, intuitive, and responsive design for browsing news articles. Key aspects of the frontend include an infinitely scrollable article list, robust search and filtering options, and a dedicated about page. The frontend was designed for easy deployment on Vercel.

### Collector

The collector is a Python based service responsible for populating our database. It systematically scrapes various cybersecurity news sources from the internet, processes the collected data for consistency, and structures it for storage. The collector is designed to run within a Docker container, ensuring a consistent and isolated environment for its operations. It can be deployed on cloud instances like Linode or on local hardware such as a Raspberry Pi.

### Database

A PostgreSQL database serves as the central repository for all aggregated news content. The primary table, `cybernews`, stores essential information for each article, including its source, URL, title, and publication date. The database schema is straightforward and optimized for efficient querying. A collection of SQL tools is available for database maintenance and analysis.

### API

A lightweight Express based API provides the necessary endpoints for the frontend to interact with the database through Supabase. It handles requests for fetching articles with pagination, retrieving configuration data, and supporting search functionality with intelligent stopword filtering. The API is designed to run as a serverless function on Vercel.

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

1.  **Database**: Begin by setting up the PostgreSQL database. This is the core data store for the application.
    - [Database Setup Instructions](./database/README.md)

2.  **API**: Set up the API service to enable communication between the frontend and database.
    - [API Setup Instructions](./api/README.md)

3.  **Frontend**: Next, set up the Next.js frontend. This will provide the user interface for viewing the data.
    - [Frontend Setup Instructions](./frontend/README.md)

4.  **Collector**: Once the database, API, and frontend are ready, set up the collector to populate the database with news articles.
    - [Collector Setup Instructions](./collector/README.md)

## Project Status

Notify Cyber was officially retired on October 31, 2025. The decision was made because the project could not achieve sufficient monetization to cover its ongoing maintenance and operational costs. This repository provides a static and open sourced version of the platform as a tribute to its legacy and a resource for the community. The domain will remain active to ensure continued access to this snapshot.

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.
