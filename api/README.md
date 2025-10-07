# Notify Cyber API

## Overview

This is the API service for Notify Cyber. Built with Express and Node.js, it provides lightweight endpoints that enable the frontend to interact with the PostgreSQL database through Supabase. The API handles requests for fetching articles, retrieving configuration data, and supporting search functionality with intelligent stopword filtering.

## Features

The API provides the following capabilities:

- Article fetching with pagination support
- Latest article ID retrieval
- Configuration data endpoints
- Search query processing with stopword filtering
- Site status checking functionality

## Technology Stack

- **Runtime**: Node.js
- **Framework**: Express.js
- **Database Client**: Supabase JS
- **Deployment**: Vercel (serverless functions)

## Key Dependencies

- `express`: Web application framework
- `@supabase/supabase-js`: Supabase client for database interaction
- `axios`: HTTP client for external requests
- `uuid`: UUID generation for unique identifiers
- `dotenv`: Environment variable management

## Project Structure

- `api/index.js`: Main API endpoint handler with Express routes
- `api/lcpo.js`: Longest Common Prefix/Overlap utility functions
- `api/stopwords-en.json`: English stopwords list for search optimization
- `api/hash.json`: Hash configuration data
- `api/home.html`: API home page
- `vercel.json`: Vercel deployment configuration
- `package.json`: Project dependencies and scripts

## Setup

### Local Development

1. Navigate to the API directory
2. Install dependencies:

   ```bash
   yarn install
   ```

   or

   ```bash
   npm install
   ```

3. Create a `.env` file with the following variables:

   ```env
   SUPABASE_URL=your_supabase_url
   SUPABASE_SECRET_KEY=your_supabase_secret_key
   MAIN_TABLE=cybernews
   ```

4. Start the development server:
   ```bash
   yarn start
   ```
   or
   ```bash
   npm start
   ```

### Deployment

The API is configured for deployment on Vercel as a serverless function. The `vercel.json` configuration file handles routing all requests to the main API handler.

To deploy:

1. Install the Vercel CLI or connect your repository to Vercel
2. Configure the required environment variables in your Vercel project settings
3. Deploy using `vercel` command or through automatic Git deployments

## Security Configuration

### Hash Generation

The `api/hash.json` file contains security hashes used by the API. **You should regenerate these hashes before deploying to production.**

To generate new hashes:

```bash
node hashify.js
```

The script will prompt you for the number of hashes to generate, then automatically create/overwrite the `api/hash.json` file with new secure random hashes.

## Implementation Notes

The API uses English stopwords for search optimization to filter out common words that don't contribute to search relevance. The stopword list is based on the [stopwords-en package](https://github.com/interup/stopwords-en) and stored locally in `stopwords-en.json`.
