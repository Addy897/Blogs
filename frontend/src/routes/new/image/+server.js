import { API_KEY, CLOUD_NAME, API_SECRET } from "$env/static/private";
import { v2 as cloudinary } from 'cloudinary';

cloudinary.config({
    cloud_name: CLOUD_NAME,
    api_key: API_KEY,
    api_secret: API_SECRET,
    secure: true,
});

function base64ToArrayBuffer(base64) {
    const binaryString = atob(base64);
    const bytes = new Uint8Array(binaryString.length);
    for (let i = 0; i < binaryString.length; i++) {
        bytes[i] = binaryString.charCodeAt(i);
    }
    return bytes.buffer;
}

export async function POST({ request }) {
    try {
        const requestBody = await request.text();
        const requestData = JSON.parse(requestBody);
        console.log("POST -> new/image");

        let { cover_photo } = requestData;

        if (cover_photo && !cover_photo.startsWith("http")) {
            const buffer = new Uint8Array(base64ToArrayBuffer(cover_photo.split(",")[1]));

            const uploadResult = await new Promise((resolve, reject) => {
                cloudinary.uploader.upload_stream({
                    folder: '',
                    resource_type: 'image'
                }, (error, result) => {
                    if (error) {
                        reject(error);
                    } else {
                        resolve(result);
                    }
                }).end(buffer);
            });

            if (uploadResult.url) {
                return new Response(JSON.stringify({ url: uploadResult.url }));
            } else {
                throw new Error("Failed to upload image to Cloudinary");
            }
        } else {
            return new Response(JSON.stringify({ url: cover_photo }));
        }
    } catch (error) {
        return new Response(JSON.stringify({ error: true, message: error.message }), { status: 500 });
    }
}
