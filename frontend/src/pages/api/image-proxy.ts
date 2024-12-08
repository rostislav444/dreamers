import type {NextApiRequest, NextApiResponse} from 'next';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
    const {url} = req.query;

    if (!url || Array.isArray(url)) {
        return res.status(400).json({error: 'URL parameter is required and must be a string'});
    }

    try {
        const imageRes = await fetch(url);
        const imageBuffer = await imageRes.arrayBuffer();
        const contentType = imageRes.headers.get('content-type') || 'image/jpeg';

        res.setHeader('Content-Type', contentType);
        res.setHeader('Cache-Control', 'public, max-age=31536000, immutable');
        res.send(Buffer.from(imageBuffer));
    } catch (error) {
        console.error('Error proxying image:', error);
        res.status(500).json({error: 'Failed to proxy image'});
    }
}

export const config = {
    api: {
        responseLimit: false,
    },
};