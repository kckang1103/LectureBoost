import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  experimental: {
    serverActions: {
      bodySizeLimit: '50mb',
    },
  },
  env: {
    NEXT_PUBLIC_BACKEND_URL: process.env.BACKEND_URL,
  }
};

export default nextConfig;
