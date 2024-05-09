import {API_KEY,CLOUD_NAME,API_SECRET} from "$env/static/private";
import { v2 as cloudinary } from 'cloudinary';

cloudinary.config({
    cloud_name: CLOUD_NAME ,
    api_key: API_KEY ,
    api_secret: API_SECRET,
    secure: true,
  });
  function base64ToArrayBuffer(base64) {
    var binaryString = atob(base64);
    var bytes = new Uint8Array(binaryString.length);
    for (var i = 0; i < binaryString.length; i++) {
        bytes[i] = binaryString.charCodeAt(i);
    }
    return bytes.buffer;
}
export async function POST({request,locals}) {

const requestBody = await request.text();
    const requestData = JSON.parse(requestBody);
    console.log("POST -> new/image")
    let{ cover_photo} = requestData;
    if(cover_photo!==null && !String(cover_photo).startsWith("http")){
        let buffer=new Uint8Array(base64ToArrayBuffer(cover_photo.split(",")[1]))
        const uploadStream = await new Promise((resolve, reject) => {
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
       if(!uploadStream.Error){
        cover_photo=uploadStream.url;
       }else{
        cover_photo=null;
       }
    }
    return new Response(JSON.stringify({url:cover_photo}))
}