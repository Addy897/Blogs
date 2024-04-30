import { redirect } from '@sveltejs/kit'
import { handlers } from '../../lib/handlers'
import { put } from "@vercel/blob";
import { writeFileSync } from 'fs';
import {API_KEY,CLOUD_NAME,API_SECRET} from "$env/static/private";
import { v2 as cloudinary } from 'cloudinary';

cloudinary.config({
    cloud_name: CLOUD_NAME ,
    api_key: API_KEY ,
    api_secret: API_SECRET,
    secure: true,
  });
 

/** @type {import('./$types').PageServerLoad} */
export async function load({locals}) {
   
    if(locals.user.access_level==="Admin"){
       
        let getdrafts=()=>{return handlers.getUserBlog(locals.user.email)}
        let getreview=()=>{ return handlers.getForReviewBlogs(locals.user)}
        return{user:locals.user,getdrafts:getdrafts(),extra:getreview()}
    }else{
        let getdrafts=()=>{return handlers.getUserBlog(locals.user.email)}

        
        return{user:locals.user,getdrafts:getdrafts()}
    }
    
    
}
/** @type {import('./$types').Actions} */
export const actions = {
    publish: async ({request,locals})=>{
        
        let data=await request.formData();
        
        let length=data.get('length')
        let markdownContent=data.get('content')
        let coverPhoto=data.get('coverPhoto')
        if(coverPhoto!=='null'){
            let filedata=await coverPhoto.arrayBuffer();
            const buffer = new Uint8Array(filedata);
			const uploadStream = await new Promise((resolve, reject) => {
				cloudinary.uploader
					.upload_stream({
                        filename_override:coverPhoto.name,
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
            coverPhoto=uploadStream.url;
           }else{
            coverPhoto=null;
           }
        }else{
            coverPhoto=null
        }
        let title=data.get('title')
        let topic=data.get('topic')
        let url_list=[]
        for(let i=0;i<length;i++){
            let fileToUpload=data.get(String((i+1)))
            let filedata=await fileToUpload.arrayBuffer();
			const buffer = new Uint8Array(filedata);
			const uploadStream = await new Promise((resolve, reject) => {
				cloudinary.uploader
					.upload_stream({
                        filename_override:fileToUpload.name,
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
           }
           else{
            return {error:true,msg:uploadStream.Error}
           }
           // writeFileSync(name,Buffer.from(filedata) );

            url_list=[...url_list,url]
        }
        if(url_list.length>0){
                markdownContent=markdownContent.replace(/\!\[Image(\d+)\]/g, (match, index) => {
                    const imageIndex = parseInt(index) - 1;
                    if (url_list[imageIndex]) {
                    return `![Image${index}](${url_list[imageIndex]})`;
                    }
                    return match
                });
        }
       let rawResponse=await handlers.setUserBlog(locals.user,title,markdownContent,coverPhoto,"2",topic)
       if (rawResponse.error) {
        return {error:true,msg:rawResponse.error}
       }
       return{sucess:true}
    },
    draft: async({request,locals})=>{
        let data=await request.formData();
        
        let length=data.get('length')
        let markdownContent=data.get('content')
        let title=data.get('title')
        let topic=data.get('topic')

        let coverPhoto=data.get('coverPhoto')
       
        if(coverPhoto!=='null'){
            let filedata=await coverPhoto.arrayBuffer();
            const buffer = new Uint8Array(filedata);
			const uploadStream = await new Promise((resolve, reject) => {
				cloudinary.uploader
					.upload_stream({
                        filename_override:coverPhoto.name,
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
            coverPhoto=uploadStream.url;
           }else{
            coverPhoto=null;
           }
        }else{
            coverPhoto=null

        }
        let url_list=[]
        for(let i=0;i<length;i++){
            let fileToUpload=data.get(String((i+1)))

            let filedata=await fileToUpload.arrayBuffer();
			const buffer = new Uint8Array(filedata);
			const uploadStream = await new Promise((resolve, reject) => {
				cloudinary.uploader
					.upload_stream({
                        filename_override:fileToUpload.name,
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
           }
           else{
            return {error:true,msg:uploadStream.Error}
           }
            url_list=[...url_list,url.url]
        }
        if(url_list.length>0){
                markdownContent=markdownContent.replace(/\!\[Image(\d+)\]/g, (match, index) => {
                    const imageIndex = parseInt(index) - 1;
                    if (url_list[imageIndex]) {
                    return `![Image${index}](${url_list[imageIndex]})`;
                    }
                    return match
                });
        }
       let rawResponse=await handlers.setUserBlog(locals.user,title,markdownContent,coverPhoto,"1",topic)
       if (rawResponse.Code !== 200) {
        return {error:true,msg:rawResponse.errorMessage}
       }
       return{sucess:true}
       
        
    }
};
