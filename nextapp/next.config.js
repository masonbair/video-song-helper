module.exports = {
  reactStrictMode: true,
  images: {
    domains: ['example.com', 'placehold.co', 'p16-sign-va.tiktokcdn.com'], // Add TikTok domains for cover images
  },
  env: {
    CUSTOM_API_URL: process.env.CUSTOM_API_URL, // Example of an environment variable
  },
  publicRuntimeConfig: {
    // Will be available on both server and client
    NEXT_PUBLIC_API_URL: process.env.CUSTOM_API_URL || 'http://localhost:8000',
  },
};