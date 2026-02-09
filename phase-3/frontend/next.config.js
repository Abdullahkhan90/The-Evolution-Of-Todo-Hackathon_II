/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  },
  // Add rewrites to proxy API calls through Next.js (avoids CORS issues)
  async rewrites() {
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'https://hafizabdullah9-phase-3-backend-todo-chatbot.hf.space';
    return {
      beforeFiles: [
        {
          source: '/api/:path*',
          destination: `${backendUrl}/api/:path*`,
        },
        {
          source: '/auth/:path*',
          destination: `${backendUrl}/auth/:path*`,
        },
        {
          source: '/health',
          destination: `${backendUrl}/health`,
        },
      ],
    };
  },
}

module.exports = nextConfig