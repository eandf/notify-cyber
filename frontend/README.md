# nc-frontend

## Creator(s)

Dylan Eck

## About

[Notify-Cyber's](https://notifycyber.com/) frontend code.

## Running Locally

1. Clone the project and run `npm install` in the root directory to install the required packages.

2. Create a file called `.env.local` in the root directory and populate it with the environment variables listed in `.env.local.template`.

3. Run `npm run dev` to start the development server. Terminal output will tell you what port the server is running on.

<br>

## Deploying to Vercel

Follow [these](https://vercel.com/docs/concepts/deployments/git#deploying-a-git-repository) instructions to deploy from a web hosted git repository.
If you do it this way, then you set a branch to be your production branch (defaults to main) and whenever you push to that branch the site will automatically be redeployed. Additionally, if you push to a branch other than main, a preview deployment will be created allowing you to test things in a production-like environment without affecting the actual production deployment.

NOTE: environment variables will need to be defined in the Vercel project. This can be done on the Vercel website.

## Where to find hard coded values

|                                       |                                                      |
| ------------------------------------- | ---------------------------------------------------- |
| `./app.config.js`                     | contains general configuration for the app           |
| `./src/app/about/page.tsx`            | about page content defined here                      |
| `./src/components/PinnedCard.tsx`     | pinned card content defined here                     |
| `./src/backend/config.ts`             | backend / database configuration defined here        |
| `./src/app/rss/rout.ts`               | default sources for the RSS feed are hard coded here |
| `./src/providers/SettingsContext.tsx` | default search / filter settings are hard coded here |

## Project Structure:

The root directory contains a bunch of configuration files.

- `.env.local` contains environment variables used when running locally.
- `.env.local.template` shows how to populate `.env.local`.
- `.eslintrc.json` contains the ESLint configuration used for static error checking. (I have not made significant changes to this file)
- `app.config.js` contains hard coded values used throughout the app. (such as the Google form links)
- `next.config.js` contains the Next.js configuration. If you want to add redirects/rewrites to the site this is where you do it. You can also make changes to the webpack configuration here. I have made changes to the webpack configuration to configure SVG file loading and add an import alias.
- `tsconfig.json` contains the typescript configuration. I have left this file mostly unchanged except that addition of an import alias.

`src/components/` contains custom react component definitions.

- `index.js` re-exports all components from a single file to allow for cleaner and easier importing.

- `Article.tsx` defines a component that displays information related to a single article fetched from the database.
- `ArticleList.tsx` defines a component that displays an infinitely scrollable list of articles fetched from the database.
- `Card.tsx` defines a component that can contain nested components and is styled to visually separate those components from the rest of the page.
- `CheckboxList.tsx` defines a component containing a list of selectable items.
- `Dropdown.tsx` defines a simple dropdown menu that can display an arbitrary component when expanded.
- `FilterBar.tsx` contains the search bar and dropdown used to select sources.
- `LoadingSpinner.tsx` defines a simple spinner used to indicate that something is loading.
- `Navbar.tsx` defines the navigation bar component displayed at the top of each page of the site. This contains the logo and menu items.
- `PinnedCard.tsx` defines the pinned card that appears at the top of the article list.
- `SearchBox.tsx` defines a simple search bar component consisting of a text input and a magnifying glass icon.

<br>

`src/components/svg` contains `svg` files that are loaded as react components using the `@svgr/webpack` package.

- `index.js` re-exports all `svg` files to allow for cleaner and easier importing.

<br>

`src/hooks/` contains custom react hook definitions.

- `useLocalStorage.ts` is a wrapper around the React `useState` hook that keeps a copy of the state value in local storage.

- `useOutsideClickListener.ts` is a wrapper around the React `useRef` hook that creates an HTML element reference with an event listener that listens for clicks outside the referenced HTML element.
- `usePaginatedDatabaseData.ts` is a custom hook used to fetch paginated data from the database.

<br>

`src/lib/` contains utility functions.

- `formatEpochAsDate.ts` formats a UNIX epoch timestamp as a human-readable string

<br>

`src/app/` contains React components that correspond to the website's pages.

- `layout.tsx` is the root application layout and includes site metadata.
  NOTE: you can add some stuff to the metadata to make link previews work. (I left some comments in `layout.tsx`)

- `page.tsx` defines the React component that is rendered when users visit https://www.notifycyber.com.
- `about/page.tsx` defines the React component that is rendered when users navigate to https://www.notifycyber.com/about.
- `contact/page.tsx` defines the React component that is rendered when users navigate to https://www.notifycyber.com/contact.
- `join/page.tsx` defines the React component that is rendered when users navigate to https://www.notifycyber.com/join.
- `rss/route.ts` defines and endpoint that returns the RSS feed when a get request is made to https://www.notifycyber.com/rss.

<br>

`src/backend` contains backend functions to interact with the database.

- `config.ts` defines an object containing information about the configuration of the database.

- `logger.ts` defines logging functionality used by the backend.
- `utils.ts` provides utility functions for interacting with Supabase.
- `getConfig.ts` returns the config object defined in `config.ts`.
- `getEvents.ts` returns articles scraped by the collector.
- `getLatestID.ts` returns the ID of the most recently scraped article.

<br>

`src/providers/` contains custom react context provider definitions.

- `SettingsContext` manages the search and filter settings using React context.

<br>

`src/styles/` contains CSS files for components and pages. The file names generally mach the names in `components/` and `app/*` except for `styles/globals.css` which contains global styles applied to the entire HTML file.

<br>

`public/` contains static assets served alongside website. This includes icons and the Notify Cyber logo.

- `logo_transparent.png` The full Notify Cyber logo as a PNG image with a transparent background.

- `nc_logo.svg` The small Notify Cyber logo as an SVG image.
- `site.webmanifest` provides information about how the site should be displayed and function when saved to a mobile device's home screen.
- `browserconfig.xml` provides information about how the site should be displayed when saved to the Windows start menu or taskbar.
- All other images were automatically generated based on `nc_logo.svg` and are used as icons in various environments the site may be run in.

<br>

## Package Dependencies:

Packages included by default in Next.js projects t are not listed. Run `npm list` or consult `package.json` for a full list of dependencies

| Package                                                                        | Purpose                                                                        |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| [`@vercel/analytics`](https://www.npmjs.com/package/@vercel/analytics)         | Used to collect web analytics when deployed to Vercel                          |
| [`react-div-100vh`](https://www.npmjs.com/package/react-div-100vh)             | Used to properly size full height HTML elements on mobile devices              |
| [`@svgr/webpack`](https://www.npmjs.com/package/@svgr/webpack)                 | Used to load SVG files as React components                                     |
| [`@supabase/supabase-js`](https://www.npmjs.com/package/@supabase/supabase-js) | Used to interact with Supabase                                                 |
| [`moment`](https://www.npmjs.com/package/moment)                               | Used to add timestamps to logging messages in the backend                      |
| [`rss`](https://www.npmjs.com/package/rss)                                     | Used to create an RSS feed                                                     |
| [`@types/rss`](https://www.npmjs.com/package/@types/rss)                       | TypeScript type definitions for the RSS package                                |
| [`stopwords-en`](https://www.npmjs.com/package/stopwords-en)                   | list of English stopwords used to filter search strings                        |
| [`simplebar-react`](https://www.npmjs.com/package/simplebar-react)             | Used for better scrollbar styling that is consistent across different browsers |

<br>

## Useful links

### React

- [documentation](https://react.dev)
- [built in hooks](https://react.dev/reference/react)
- [custom hooks](https://react.dev/learn/reusing-logic-with-custom-hooks#custom-hooks-sharing-logic-between-components)
- [context](https://react.dev/learn/passing-data-deeply-with-context)
- [infinite scroll tutorial](https://www.youtube.com/watch?v=JWlOcDus_rs&t=1526s)
- [Fireship React Hooks explanation](https://www.youtube.com/watch?v=TNhaISOUy6Q)

### Next.js

- [documentation](https://nextjs.org/docs)
- [react essentials](https://nextjs.org/docs/getting-started/react-essentials)
- [CSS modules](https://nextjs.org/docs/app/building-your-application/styling/css-modules)
- [import aliases](https://nextjs.org/docs/pages/building-your-application/configuring/absolute-imports-and-module-aliases)
- [special file names in app directory](https://nextjs.org/docs/getting-started/project-structure#app-routing-conventions)
- [site metadata](https://nextjs.org/docs/app/building-your-application/optimizing/metadata)

### TypeScript

- [documentation](https://www.typescriptlang.org/docs/)
- [barrel files](https://basarat.gitbook.io/typescript/main-1/barrel)

### CSS

- [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/CSS)
- [codepen.io (for testing HTML/CSS stuff)](https://codepen.io/)
- [hamburger menu icon tutorial](https://www.youtube.com/watch?v=dAIVbLrAb_U)

### Favicon / icon generator

- [realfavicongenerator](https://realfavicongenerator.net/)

### Vector graphics (SVG) editor for creating icons

- [Vectornator](https://www.vectornator.io/)
