import type { Metadata } from "next";
import { GeistSans } from "geist/font/sans";
import { GeistMono } from "geist/font/mono";
import "./globals.css";

export const metadata: Metadata = {
  title: "Agile Refinery | Transform Ideas into Action",
  description:
    "Transform rough ideas into polished, actionable agile work items with AI-powered refinement. Built for modern product teams.",
  keywords: [
    "agile",
    "work items",
    "user stories",
    "AI",
    "product management",
    "scrum",
    "refinement",
  ],
  authors: [{ name: "Agile Refinery" }],
  openGraph: {
    title: "Agile Refinery | Transform Ideas into Action",
    description:
      "Transform rough ideas into polished, actionable agile work items with AI-powered refinement.",
    type: "website",
    locale: "en_US",
  },
  twitter: {
    card: "summary_large_image",
    title: "Agile Refinery | Transform Ideas into Action",
    description:
      "Transform rough ideas into polished, actionable agile work items with AI-powered refinement.",
  },
  robots: {
    index: true,
    follow: true,
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body
        className={`${GeistSans.variable} ${GeistMono.variable} font-sans antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
