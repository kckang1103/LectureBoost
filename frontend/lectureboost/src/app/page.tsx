'use client'

import LandingPage from "./landing";
import Link from 'next/link'

export default function Home() {
  return (
    <Link href="/">
        <LandingPage />
    </Link>
  );
}
