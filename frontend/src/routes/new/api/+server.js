import { handlers } from '../../../lib/handlers.js';
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
    console.log("POST -> new/api")
    let{ cover_photo, topic, description,delta, title, action,tag,domain } = requestData;
    if(action==="Publish"){
        action="InReview"
    }else{
        action="Draft"
    }
    let parsed=JSON.parse(delta)
    let ops=parsed.ops
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
    }else{
        cover_photo=null
    }
    
    for (let i = 0; i < ops.length; i++) {
        const element = ops[i];
        if(element.insert && element.insert.image){
           if(String(element.insert.image).startsWith("http")){
            continue
           }
            let buffer=new Uint8Array(base64ToArrayBuffer(element.insert.image.split(",")[1]))
            const uploadStream = await new Promise((resolve, reject) => {
                cloudinary.uploader
                    .upload_stream({
                        folder: '',
                        resource_type: 'image'}, function (error, result) {
                        if (error) {
                            return reject(error);
                        }
                        return resolve(result);
                    })
                    .end(buffer);
            });
            let url=null
           if(!uploadStream.Error){
            url=uploadStream.url;
            ops[i].insert.image=url
           }
           else{
            return new Response(JSON.stringify({error:true,msg:rawResponse.error}))
           }
        }
        
    }; 
    parsed.ops=ops;
    parsed=JSON.stringify(parsed)
    
   let rawResponse=await handlers.setUserBlog(locals.user,title,description,parsed,cover_photo,action,topic,tag,domain)    
      
    return new Response(JSON.stringify(rawResponse))
  }
  