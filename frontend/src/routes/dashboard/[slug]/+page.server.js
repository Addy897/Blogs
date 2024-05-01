import { error } from '@sveltejs/kit'
import { handlers } from '$lib/handlers.js'

export async function load({url,params,locals}) {
    if(locals.user.access_level==="Admin"){
        let draft=url.searchParams.get('for')
        if(draft==="draft"){
            let blog=await handlers.getUserBlog(locals.user.email,params.slug)
            if(blog.draft[0].author.uid===locals.user.uid){
            return{user:locals.user,blog:blog.draft}
            }else{
                error(404,"Not Found");
            }
        }
        let forReview=await handlers.getForReviewBlogs(locals.user,params.slug)
        
        return{user:locals.user,review:forReview.draft}
    }else{
    let blog=await handlers.getUserBlog(locals.user.email,params.slug)
    if(blog.draft && blog.draft[0].author.uid===locals.user.uid){
    return{user:locals.user,blog:blog.draft}
    }else{
        error(404,"Not Found");
    }
}
}
/** @type {import('./$types').Actions} */
export const actions = {
    getMD:async ({locals,params})=>{
        if(locals.user && params.slug){
            let {draft}=await handlers.getUserDraft(locals.user,params.slug)
            
            return draft;
        }

    },
    setMD:async ({request,locals})=>{
        const {md,ref_id}= await request.json();
        if(locals.user){
            let resposne=await handlers.edithUserBlog(locals.user,md,ref_id)
            if(resposne.error){
                return resposne
            }
            
        }

    },
    pub:async ({request,locals})=>{
        const {ref_id}= await request.json();
        if(locals.user){
            let resposne=await handlers.publishUserBlog(locals.user,ref_id)
            if(resposne.error){
                return resposne
            }
            
        }

    },
    rpub:async ({request,locals})=>{
        const {ref_id}= await request.json();
        if(locals.user){
            let resposne=await handlers.publishUserBlog(locals.user,ref_id)
            if(resposne.error){
                return resposne
            }
            
        }

    }
};