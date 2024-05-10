import { handlers } from '../../../lib/handlers.js';
import { API_KEY, CLOUD_NAME, API_SECRET } from "$env/static/private";
import { v2 as cloudinary } from 'cloudinary';

// Configure Cloudinary
cloudinary.config({
    cloud_name: CLOUD_NAME,
    api_key: API_KEY,
    api_secret: API_SECRET,
    secure: true,
});

// Function to convert base64 to array buffer
function base64ToArrayBuffer(base64) {
    const binaryString = atob(base64);
    const bytes = new Uint8Array(binaryString.length);
    for (let i = 0; i < binaryString.length; i++) {
        bytes[i] = binaryString.charCodeAt(i);
    }
    return bytes.buffer;
}

// Function to upload images in Quill delta to Cloudinary
async function uploadImagesToCloudinary(delta) {
    return Promise.all(delta.ops.map(async (element) => {
        if (element.insert && element.insert.image && !element.insert.image.startsWith("http")) {
            const buffer = new Uint8Array(base64ToArrayBuffer(element.insert.image.split(",")[1]));
            const result = await new Promise((resolve, reject) => {
                cloudinary.uploader.upload_stream({
                            folder: '',
                            resource_type: 'image'}, function (error, result) {
                if (error) {
                  return reject(error);
                }
                return resolve(result);
              })
              .end(buffer);
          });
            element.insert.image = result.url;
        }
        return element;
    }));
}

// Handler function for POST request
export async function POST({ request, locals }) {
    try {
        const requestBody = await request.text();
        const requestData = JSON.parse(requestBody);
        console.log("POST -> new/api");

        let { cover_photo,topic, description, delta, title, action, tag, domain } = requestData;

        action = (action === "Publish") ? "InReview" : "Draft";
        const updatedDelta = await uploadImagesToCloudinary(JSON.parse(delta));
        const rawResponse = await handlers.setUserBlog(locals.user, title, description, JSON.stringify({ ops: updatedDelta }), cover_photo, action, topic, tag, domain);
        if(rawResponse.error){
            return new Response(JSON.stringify({ error: true, msg: rawResponse.error, delta:{ops: updatedDelta },cover_photo:cover_photo }), { status: 500 });
        }
        return new Response(JSON.stringify(rawResponse));
    } catch (error) {
        return new Response(JSON.stringify({ error: true, msg: error.message, delta:{ops: updatedDelta },cover_photo:cover_photo }), { status: 500 });
    }
}
