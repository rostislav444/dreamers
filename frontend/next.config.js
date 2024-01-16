/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    images: {
        domains: [
            'dreamers.s3.eu-north-1.amazonaws.com',
            'dreamers.s3.amazonaws.com',
            'dreamers.com.ua',
            '0.0.0.0'
        ],
    },
}

module.exports = nextConfig
