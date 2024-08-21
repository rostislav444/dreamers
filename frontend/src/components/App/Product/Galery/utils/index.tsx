import {MEDIA_URL} from "@/local";
import mergeImages from "merge-images";
import {saveAs} from "file-saver";


export const handleImageMergeAndDownload = async (images: string[]) => {
    try {
        const imageBlobs = await Promise.all(images.map(async (image) => {
            const response = await fetch(MEDIA_URL + image);
            const blob = await response.blob();
            return URL.createObjectURL(blob);
        }));

        const merged = await mergeImages(imageBlobs);
        // Конвертируем base64 в Blob
        const byteString = atob(merged.split(',')[1]);
        const mimeString = merged.split(',')[0].split(':')[1].split(';')[0];
        const ab = new ArrayBuffer(byteString.length);
        const ia = new Uint8Array(ab);
        for (let i = 0; i < byteString.length; i++) {
            ia[i] = byteString.charCodeAt(i);
        }
        const blob = new Blob([ab], {type: mimeString});

        // Генерация рандомного имени файла
        const randomFileName = `dreamers-${Math.random().toString(36).substr(2, 9)}.png`;

        // Скачивание файла
        saveAs(blob, randomFileName);
    } catch (error) {
        console.error('Error merging images:', error);
    }
};