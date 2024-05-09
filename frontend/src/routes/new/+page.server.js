import { redirect } from '@sveltejs/kit';
import {API_KEY,CLOUD_NAME,API_SECRET} from "$env/static/private";
import { v2 as cloudinary } from 'cloudinary';
import { goto } from '$app/navigation';
import { signJWT } from '../../lib/jwtHadlers';

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
/** @type {import('./$types').PageServerLoad} */
export async function load({locals}) {
    if(!locals.user){
        redirect(303,"/login")
    } else if(locals.user.access_level==="Read"){
        redirect(303,"/dashboard")
    }
}
/** @type {import('./$types').Actions} */
export const actions = {
    image:async ({request,locals})=>{
        let data=await request.formData();
        return;
       
       
    },
};