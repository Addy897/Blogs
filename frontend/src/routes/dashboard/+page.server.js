import { handlers } from '../../lib/handlers'
import { signJWT } from '../../lib/jwtHadlers'

 

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
