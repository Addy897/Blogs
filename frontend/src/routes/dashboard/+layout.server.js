import { redirect } from '@sveltejs/kit'

export async function load({locals,data}) {
    if(!locals.user){
        throw redirect(301,'/login')
    }
    if(locals.drafts){
        return{drafts:locals.drafts}
      }
}