import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'MakolaMetric AI - Currency Conversion',
  description: 'AI-powered currency conversion with confidence scoring',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
