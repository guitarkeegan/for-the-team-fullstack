import type { Metadata } from "next";
import { Roboto, Bebas_Neue } from "next/font/google";
import "./globals.css";

const roboto = Roboto({ 
  weight: ['400', '700'],
  subsets: ['latin'],
  variable: '--font-roboto',
});

const bebasNeue = Bebas_Neue({
  weight: '400',
  subsets: ['latin'],
  variable: '--font-bebas-neue',
});

export const metadata: Metadata = {
  title: "Clippers App",
  description: "Clippers team management application",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`${roboto.variable} ${bebasNeue.variable} font-sans`}>{children}</body>
    </html>
  );
}
