import { redirect } from '@sveltejs/kit'
import { handlers } from '../../lib/handlers'
import { put } from "@vercel/blob";

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
        let title=data.get('title')
        let url_list=[]
        for(let i=0;i<length;i++){
            let fileToUpload=data.get(String((i+1)))
            let name=`uploads/${fileToUpload.name.replace(" ","_")}.png`
            let url  = await put(name, fileToUpload, { access: 'public',token:"vercel_blob_rw_X9mFAlR8Ju6WpJqj_025bj7SwNE7AEjy8UHFRtRhJQf8F2U"});
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
       let rawResponse=await handlers.setUserBlog(locals.user,title,markdownContent,"2")
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
        let url_list=[]
        for(let i=0;i<length;i++){
            let fileToUpload=data.get(String((i+1)))
            let name=`uploads/${fileToUpload.name.replace(" ","_")}.png`
            let url  = await put(name, fileToUpload, { access: 'public',token:"vercel_blob_rw_X9mFAlR8Ju6WpJqj_025bj7SwNE7AEjy8UHFRtRhJQf8F2U"});
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
       let rawResponse=await handlers.setUserBlog(locals.user,title,markdownContent,"1")
       if (rawResponse.Code !== 200) {
        return {error:true,msg:rawResponse.errorMessage}
       }
       return{sucess:true}
       
        
    }
};
