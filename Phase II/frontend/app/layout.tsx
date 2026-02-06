import type { Metadata } from "next";
import "./globals.css";
import RootWrapper from './RootWrapper';

export const metadata: Metadata = {
  title: "TaskFlow - Secure Todo Application",
  description: "A modern, secure todo application with JWT-based authentication",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        <RootWrapper>
          {children}
        </RootWrapper>
      </body>
    </html>
  );
}
