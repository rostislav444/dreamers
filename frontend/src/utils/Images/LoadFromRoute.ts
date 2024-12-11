export function LoadFromRoute(image: string) {
    return `/api/image-proxy?url=${encodeURIComponent(image)}`
}