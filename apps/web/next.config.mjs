/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  transpilePackages: ['@chipforge/ai-core', '@chipforge/ui', '@chipforge/verilog-lang'],
  experimental: {
    typedRoutes: false,
  },
};

export default nextConfig;
