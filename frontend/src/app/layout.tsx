import type { Metadata } from "next";
// Remove: import { Geist, Geist_Mono } from "next/font/google"; // <--- DELETE THIS LINE
import "./globals.css";

// Remove: const geistSans = Geist({ ... }); // <--- DELETE THIS BLOCK
// Remove: const geistMono = Geist_Mono({ ... }); // <--- DELETE THIS BLOCK

export const metadata: Metadata = {
  title: "KeyFrame AI Video Generator", // Update Title
  description: "AI-Powered Short Video Generator MVP", // Update Description
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
      // Clean the className. We rely only on globals.css for styling now.
      // If you were using any custom global classes, they would go here.
      // We ensure no conflicting background classes remain.
      >
        {children}
      </body>
    </html>
  );
}