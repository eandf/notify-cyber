/** @type {import('next').NextConfig} */

const path = require("path");

const nextConfig = {
  // reactStrictMode is a debug tool that effectively renders every component
  // twice. This can cause problems with compoents that fetch data wich is
  // why I have it disabled
  reactStrictMode: false,
  swcMinify: true,
  async rewrites() {
    return [
      {
        // this effectivly makes /feed an alias of /rss
        source: "/feed",
        destination: "/rss",
      },
    ];
  },
  async redirects() {
    return [
      {
        // this is here because at one point /more showed up before / on bing
        source: "/more",
        destination: "/",
        permanent: false,
        basePath: false,
      },
    ];
  },
  webpack(config) {
    // tell webpack to use @svgr/webpack to load svg files
    // this makes svg images behave like react components
    config.module.rules.push({
      test: /\.svg$/,
      use: [{ loader: "@svgr/webpack", options: { icon: true } }],
    });
    // set up an import alias to make imports cleaner
    // NOTE: if you change this, you will also need to change the import alias
    // configuration in tsconfig.json
    config.resolve.alias = {
      ...config.resolve.alias,
      "@": path.resolve(__dirname, "./"),
    };
    return config;
  },
  // enable server actions so that we can interact with the database
  // without needing to create a middleman api
  experimental: {
    serverActions: true,
  },
};

module.exports = nextConfig;
