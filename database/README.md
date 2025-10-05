# Notify Cyber Database Setup

## Overview

PostgreSQL database for storing scraped cybersecurity news. Main table: `cybernews` (id, source, url, title, date, recorded, details, html).

## Setup

1. Create database:

   ```bash
   psql -U postgres -c "CREATE DATABASE notify_cyber;"
   psql -U postgres -d notify_cyber
   ```

2. Run schema:

   ```bash
   psql -U postgres -d notify_cyber -f setup.sql
   ```

3. Data is populated by the collector service.

## Tools

SQL utilities in `tools/` for analysis and maintenance:

- `avg_per_day.sql`: Average daily entries over 24 months
- `count_tables.sql`: Row counts by source (CVE vs non-CVE)
- `full_db_size.sql`: Database size and total rows
- `full_search.sql`: Full-text search (prepare/execute with term)
- `list_duplicated_urls.sql`: Find duplicate URLs
- `top_latest_ids.sql`: 10 latest entries

Run with: `psql -U postgres -d notify_cyber -f tools/script.sql`
