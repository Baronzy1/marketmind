import '../styles/globals.css';
import type { AppProps } from 'next/app';

export default function App({ Component, pageProps }: AppProps) {
  return (
    <div className="dark bg-neutral-950 text-neutral-100 min-h-screen">
      <Component {...pageProps} />
    </div>
  );
}