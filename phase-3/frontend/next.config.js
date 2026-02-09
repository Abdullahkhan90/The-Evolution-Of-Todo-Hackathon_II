/** @type {import('next').NextConfig} */
const nextConfig = {
  // Environment variables - frontend can access these with NEXT_PUBLIC_ prefix
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
    NEXT_PUBLIC_BACKEND_URL: process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000',
  },
  
  // Rewrites to proxy API calls through Next.js (fixes CORS issues)
  async rewrites() {
    // Get backend URL from environment
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || process.env.VERCEL_ENV === 'production' 
      ? process.env.NEXT_PUBLIC_BACKEND_URL
      : 'http://localhost:8000';
    
    console.log('Next.js rewrites using backend URL:', backendUrl);
    
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
  
  // Headers for API security
  async headers() {
    return [
      {
        source: '/api/:path*',
        headers: [
          { key: 'Access-Control-Allow-Origin', value: '*' },
        ],
      },
    ];
  },
}

module.exports = nextConfig