import { put } from "@vercel/blob";

/** @type {import('./$types').Actions} */
export const actions = {
    test:async({request,locals})=>{
        let response=await request.formData();
        let content=response.get('content');
        
        console.log(content);
    },
    upload:async({request,locals})=>{
        let images=await request.formData();
        let length=images.get('length')
        let markdownContent=images.get('content')
        let url_list=[]
        for(let i=0;i<length;i++){
            let fileToUpload=images.get(String((i+1)))
            let name=`uploads/${fileToUpload.name.replace(" ","_")}.png`
            let url  = await put(name, fileToUpload, { access: 'public',token:"vercel_blob_rw_X9mFAlR8Ju6WpJqj_025bj7SwNE7AEjy8UHFRtRhJQf8F2U"});
            url_list=[...url_list,url.url]
        }
        
        markdownContent=markdownContent.replace(/\!\[Image(\d+)\]/g, (match, index) => {
            const imageIndex = parseInt(index) - 1;
            if (url_list[imageIndex]) {
              return `![Image${index}](${url_list[imageIndex]})`;
            }
            return match
        });
    }
};