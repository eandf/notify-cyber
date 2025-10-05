# Notify Cyber Database Setup

## Overview

This directory contains the setup scripts for the PostgreSQL database that stores all cybersecurity news articles collected by the collector. The primary table, `cybernews`, is designed to hold essential information for each article.

## Quick Start with Docker

For a fast and easy setup, a `run.sh` script is provided to automate the process using Docker.

### Prerequisites

- Docker must be installed and running on your system. You can download it from the official website: [Docker Get Started](https://www.docker.com/get-started/).

### Usage

Simply execute the script from this directory:

```bash
bash ./run.sh
```

This script will:

1. Check if a PostgreSQL container is already running
2. If not, start a new PostgreSQL container named `pgDB-<timestamp>`
   - The default password for the `postgres` user is set to `password`
   - The database port `5432` is mapped to your local machine
3. Automatically open an interactive `psql` shell connected to the database

Once inside the `psql` shell, you can proceed to run the schema setup.

## Manual Setup

If you prefer to set up the database without the script or on a non-Docker instance, follow these steps.

1. **Create the Database**:

   ```bash
   psql -U postgres -c "CREATE DATABASE notify_cyber;"
   ```

2. **Connect to the Database**:

   ```bash
   psql -U postgres -d notify_cyber
   ```

3. **Run Schema Setup**:
   Once connected, run the `setup.sql` script to create the necessary tables and schema.
   ```sql
   \i setup.sql
   ```
   Alternatively, you can run it directly from your shell:
   ```bash
   psql -U postgres -d notify_cyber -f setup.sql
   ```

The database will then be ready for the collector service to populate it with data.

## Tools

This directory includes several SQL scripts in the `tools/` directory for database analysis and maintenance:

- **`avg_per_day.sql`**: Calculates the average number of daily entries over 24 months
- **`count_tables.sql`**: Counts rows by source (CVE vs. non CVE)
- **`full_db_size.sql`**: Reports the total database size and row count
- **`full_search.sql`**: Performs a full text search (requires preparing and executing with a search term)
- **`list_duplicated_urls.sql`**: Finds duplicate URLs in the `cybernews` table
- **`top_latest_ids.sql`**: Retrieves the 10 most recent entries

You can run any of these tools with the following command, replacing `script.sql` with the desired file:

```bash
psql -U postgres -d notify_cyber -f tools/script.sql
```
