# Notify Cyber API

## Overview

This is the API service for Notify Cyber. It provides lightweight endpoints that enable the frontend to interact with the database, handling requests for fetching articles, retrieving configuration data, and supporting search functionality.

## Features

The API includes:

- Article fetching endpoints
- Configuration data retrieval
- Search query processing with stopword filtering

## Implementation Notes

The API uses English stopwords for search optimization. The stopword list is sourced from the [stopwords-en](https://github.com/interup/stopwords-en) package.

## Setup

Detailed setup instructions will depend on your deployment environment. Ensure you have the necessary environment variables configured to connect to your PostgreSQL database.
