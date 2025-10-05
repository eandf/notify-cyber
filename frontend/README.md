# Notify Cyber Frontend

## Overview

This is the frontend web application for [Notify Cyber](https://notifycyber.com/). Built with Next.js and React, it provides a modern, responsive interface for browsing cybersecurity news articles with infinite scrolling, search functionality, and source filtering capabilities.

## Running Locally

1. Clone the project and run `npm install` in the root directory to install the required packages.

2. Create a file called `.env.local` in the root directory and populate it with the environment variables listed in `.env.local.template`.

3. Run `npm run dev` to start the development server. Terminal output will tell you what port the server is running on.

<br>

## Deploying to Vercel

Follow the [Vercel deployment guide](https://vercel.com/docs/concepts/deployments/git#deploying-a-git-repository) to deploy from a web hosted git repository. When configured this way, you can set a branch to be your production branch (defaults to main), and the site will automatically redeploy whenever you push to that branch. Pushing to other branches will create preview deployments, allowing you to test changes in a production like environment without affecting the live site.

**Note**: Environment variables must be configured in your Vercel project settings through the Vercel website.

## Configuration Files

Key configuration files and their purposes:

| File Path                             | Description                        |
| ------------------------------------- | ---------------------------------- |
| `./app.config.js`                     | General application configuration  |
| `./src/app/about/page.tsx`            | About page content                 |
| `./src/components/PinnedCard.tsx`     | Pinned card content                |
| `./src/backend/config.ts`             | Backend and database configuration |
| `./src/app/rss/route.ts`              | Default sources for the RSS feed   |
| `./src/providers/SettingsContext.tsx` | Default search and filter settings |

## Project Structure

### Root Directory Configuration Files

- `.env.local`: Environment variables for local development
- `.env.local.template`: Template showing required environment variables
- `.eslintrc.json`: ESLint configuration for static error checking
- `app.config.js`: Hard coded values used throughout the app, such as external links
- `next.config.js`: Next.js configuration including redirects, rewrites, and webpack settings for SVG loading and import aliases
- `tsconfig.json`: TypeScript configuration with import alias settings

### Components Directory

`src/components/` contains custom React component definitions:

- `index.js`: Barrel file that re-exports all components for cleaner imports
- `Article.tsx`: Displays information for a single article from the database
- `ArticleList.tsx`: Infinitely scrollable list of articles
- `Card.tsx`: Container component that visually separates nested content
- `CheckboxList.tsx`: List of selectable items
- `Dropdown.tsx`: Simple dropdown menu supporting arbitrary nested components
- `FilterBar.tsx`: Search bar and source selection dropdown
- `LoadingSpinner.tsx`: Loading indicator spinner
- `Navbar.tsx`: Navigation bar with logo and menu items
- `PinnedCard.tsx`: Pinned card displayed at the top of the article list
- `SearchBox.tsx`: Search input with magnifying glass icon

### SVG Components

`src/components/svg` contains SVG files loaded as React components using the `@svgr/webpack` package:

- `index.js`: Barrel file that re-exports all SVG files

### Custom Hooks

`src/hooks/` contains custom React hook definitions:

- `useLocalStorage.ts`: Wrapper around `useState` that persists state to local storage
- `useOutsideClickListener.ts`: Creates an element reference with a click listener for detecting clicks outside the element
- `usePaginatedDatabaseData.ts`: Fetches paginated data from the database

### Utility Functions

`src/lib/` contains utility functions:

- `formatEpochAsDate.ts`: Formats UNIX epoch timestamps as human readable strings

### Pages

`src/app/` contains React components that correspond to website pages:

- `layout.tsx`: Root application layout including site metadata
- `page.tsx`: Home page component
- `about/page.tsx`: About page component
- `contact/page.tsx`: Contact page component
- `join/page.tsx`: Join page component
- `rss/route.ts`: API endpoint that returns the RSS feed

### Backend

`src/backend/` contains backend functions for database interaction:

- `config.ts`: Database configuration object
- `logger.ts`: Backend logging functionality
- `utils.ts`: Utility functions for Supabase interaction
- `getConfig.ts`: Returns the database configuration
- `getEvents.ts`: Retrieves articles from the collector
- `getLatestID.ts`: Returns the ID of the most recent article

### Context Providers

`src/providers/` contains custom React context provider definitions:

- `SettingsContext.tsx`: Manages search and filter settings using React context

### Styles

`src/styles/` contains CSS files for components and pages. File names generally match those in `components/` and `app/`. The `globals.css` file contains global styles applied to the entire HTML document.

### Public Assets

`public/` contains static assets served with the website:

- `logo_transparent.png`: Full Notify Cyber logo as PNG with transparent background
- `nc_logo.svg`: Small Notify Cyber logo as SVG
- `site.webmanifest`: Configuration for mobile home screen display
- `browserconfig.xml`: Configuration for Windows start menu and taskbar
- Additional icon images automatically generated from `nc_logo.svg` for various environments

## Package Dependencies

Key dependencies beyond the default Next.js packages (run `npm list` or check `package.json` for the complete list):

| Package                                                                        | Purpose                                                    |
| ------------------------------------------------------------------------------ | ---------------------------------------------------------- |
| [`@vercel/analytics`](https://www.npmjs.com/package/@vercel/analytics)         | Web analytics collection when deployed to Vercel           |
| [`react-div-100vh`](https://www.npmjs.com/package/react-div-100vh)             | Properly sizes full height HTML elements on mobile devices |
| [`@svgr/webpack`](https://www.npmjs.com/package/@svgr/webpack)                 | Loads SVG files as React components                        |
| [`@supabase/supabase-js`](https://www.npmjs.com/package/@supabase/supabase-js) | Supabase client for database interaction                   |
| [`moment`](https://www.npmjs.com/package/moment)                               | Adds timestamps to backend logging messages                |
| [`rss`](https://www.npmjs.com/package/rss)                                     | RSS feed generation                                        |
| [`@types/rss`](https://www.npmjs.com/package/@types/rss)                       | TypeScript type definitions for the RSS package            |
| [`stopwords-en`](https://www.npmjs.com/package/stopwords-en)                   | English stopwords list for search string filtering         |
| [`simplebar-react`](https://www.npmjs.com/package/simplebar-react)             | Cross browser consistent scrollbar styling                 |

## Additional Resources

### React

- [React Documentation](https://react.dev)
- [Built in Hooks](https://react.dev/reference/react)
- [Custom Hooks](https://react.dev/learn/reusing-logic-with-custom-hooks#custom-hooks-sharing-logic-between-components)
- [Context API](https://react.dev/learn/passing-data-deeply-with-context)
- [Infinite Scroll Tutorial](https://www.youtube.com/watch?v=JWlOcDus_rs&t=1526s)
- [Fireship React Hooks Explanation](https://www.youtube.com/watch?v=TNhaISOUy6Q)

### Next.js

- [Next.js Documentation](https://nextjs.org/docs)
- [React Essentials](https://nextjs.org/docs/getting-started/react-essentials)
- [CSS Modules](https://nextjs.org/docs/app/building-your-application/styling/css-modules)
- [Import Aliases](https://nextjs.org/docs/pages/building-your-application/configuring/absolute-imports-and-module-aliases)
- [App Directory File Conventions](https://nextjs.org/docs/getting-started/project-structure#app-routing-conventions)
- [Metadata Configuration](https://nextjs.org/docs/app/building-your-application/optimizing/metadata)

### TypeScript

- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [Barrel Files](https://basarat.gitbook.io/typescript/main-1/barrel)

### CSS

- [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS)
- [CodePen](https://codepen.io/)
- [Hamburger Menu Tutorial](https://www.youtube.com/watch?v=dAIVbLrAb_U)

### Tools

- [Favicon Generator](https://realfavicongenerator.net/)
- [Vectornator SVG Editor](https://www.vectornator.io/)
