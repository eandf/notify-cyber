// centralized exporting of svg files to make importing cleaner and easier
// see: https://basarat.gitbook.io/typescript/main-1/barrel
// note: svg files are loaded using the @svgr/webpack package
// this allows them to be used as if they were react components

export { default as SearchIcon } from "./search-svgrepo-com.svg";
export { default as ChevronUpIcon } from "./chevron-top-svgrepo-com.svg";
export { default as ChevronDownIcon } from "./chevron-bottom-svgrepo-com.svg";
export { default as CloseIcon } from "./close-svgrepo-com.svg";
export { default as TwitterIcon } from "./TwitterIcon.svg";
export { default as MediumIcon } from "./MediumIcon.svg";
export { default as RedditIcon } from "./RedditIcon.svg";
export { default as RSSIcon } from "./RSSIcon.svg";
