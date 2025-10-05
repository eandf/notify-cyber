// this react component wraps all pages on the site
// it includes metadata and the vercel analytics component

import appConfig from "@/app.config";
import "@/src/styles/globals.css";
import { Analytics } from "@vercel/analytics/react";
import { Metadata } from "next";

// the exported metadata object defines the site metadata
// see: https://nextjs.org/docs/app/building-your-application/optimizing/metadata
// the documentation for this type is pretty bad, I would recommend just
// going through the source code to figure it out
// its also new enought that it isn't in chatgpt's training data
export const metadata: Metadata = {
  title: "Notify Cyber",
  description: "Stay on top of new cybersecurity threats with Notify Cyber",
  generator: "Next.js",
  keywords: ["cybersecurity", "news"],
  referrer: "no-referrer-when-downgrade",
  themeColor: "#4b4577",
  colorScheme: "normal",
  viewport: {
    width: "device-width",
    initialScale: 1.0,
    viewportFit: "cover",
  },
  // robots: {}, TODO: fill this in
  alternates: {
    canonical: appConfig.deploymentURL,
    types: {
      "application/rss+xml": [{ url: "rss", title: "rss" }],
    },
  },
  // fill these out for embed previews
  // openGraph: {}
  // twitter: {}
  appleWebApp: {
    capable: false,
  },
  formatDetection: {
    telephone: false,
    date: false,
    address: false,
    email: false,
    url: false,
  },

  icons: [
    {
      rel: "apple-touch-icon",
      sizes: "180x180",
      url: "/apple-touch-icon.png",
    },
    {
      rel: "icon",
      type: "image/png",
      sizes: "32x32",
      url: "/favicon-32x32.png",
    },
    {
      rel: "icon",
      type: "image/png",
      sizes: "16x16",
      url: "/favicon-16x16.png",
    },
    {
      rel: "mask-icon",
      // @ts-ignore: 'color' does not exist in type 'URL | IconDescriptor'
      color: "#5bbad5",
      url: "/safari-pinned-tab.svg",
    },
  ],
  manifest: "/site.webmanifest",
  other: {
    "msapplication-TileColor": "#2b5797",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  );
}
