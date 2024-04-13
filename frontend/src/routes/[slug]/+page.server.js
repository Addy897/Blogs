import { handlers } from '../../lib/handlers.js'

export async function load({params,locals}) {
    
    let blog=await handlers.getBlogs(params.slug)
    locals.blog=blog.blog
    return{user:locals.user,blog:blog.blog}


}
/** @type {import('./$types').Actions} */
export const actions = {
    addComment:async ({request,locals,params})=>{
            let formData = await request.formData();
            
            if(locals.user){
                let comment=formData.get('comment');
                if(comment){
                    let r=await handlers.addComment(locals.user,comment,params.slug);

                    if(r.error){
                        return r;
                    }

                }else{
                return {error:true,errorMessage:"Empty Comment!!"}
                }
            }
    },
    remove:async({request,locals})=>{
        const {cid,cuid}= await request.json();
        
        if(locals.user){
            if(cid && cuid){
                
                let r=await handlers.removeComment(cid,cuid);
               if(r.error){
                    return r;
                }

            }
            return {error:true,errorMessage:"Empty Comment!!"}
        }
    },
    report:async({request,locals})=>{
        const {cid}= await request.json();
        
        if(locals.user){
            if(cid){
                
                let r=await handlers.report(cid);
                if(r.error){
                    return r;
                }

            }
            return {error:true,errorMessage:"Empty Comment!!"}
        }
    }
};