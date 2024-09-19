/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: `${process.env.NEXT_PUBLIC_BASE_URL}/:path*`, // Proxy to API
      },
    ];
  },
  env: {
    NEXT_PUBLIC_TEAM_ID: process.env.NEXT_PUBLIC_TEAM_ID,
  },
};

export default nextConfig;
