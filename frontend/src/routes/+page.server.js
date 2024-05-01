import { handlers } from '../lib/handlers'
import { signJWT } from '../lib/jwtHadlers';

/** @type {import('./$types').PageServerLoad} */
export async function load({ locals,url }) {
    let keyword=url.searchParams.get('keyword')
    const getAllDesign=async(title)=>{
        const drafts=await handlers.getAllBlogs(title)
        return drafts.blog;
    }

  
  if (locals.user) {
    return {user:locals.user,drafts:getAllDesign(keyword)}
  }
  return{drafts:getAllDesign(keyword)}
}

/** @type {import('./$types').Actions} */
export const actions = {
  search: async ({ request }) => {
    let formData = await request.formData();
    let keyword = formData.get('keyword');
    if (keyword) {


      const rawResponse = await fetch('http://127.0.0.1:8000/items/get/', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Api-Token': 'random',
          'Keyword': keyword,
        },
      });

      let content = await rawResponse.json();
      content = Buffer.from(content.response, "base64").toString()
      content=JSON.parse(content)

      if (content.length) {
        
        return { sucess: true, content: content }
      }
      return { sucess: true }
    }
  },
  like: async({request,locals,cookies})=>{
    if(locals.user){
      const {ref_id}= await request.json();
      let r=await handlers.likeCount(locals.user,ref_id)

        let error=r.error
        if(!error){
          cookies.delete('user',{ httpOnly: true,
            sameSite: 'strict',
            secure: false,
            path: '/',
            maxAge: 60 * 60*24*7})
          let token = null
            try{
              
                token= await signJWT({user:r})
            }catch(e){
                console.log(e)
                throw redirect(303,"/login")
            }
            if(!token){
                throw redirect(303,"/login")
            }
            cookies.set("user",token,{ httpOnly: true,
                sameSite: 'strict',
                secure: false,
                path: '/',
                maxAge: 60 * 60*24*7}) 
            locals.user=r
        }
      }
  }
};