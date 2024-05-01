import { redirect } from '@sveltejs/kit';

/** @type {import('./$types').PageServerLoad} */
export async function load({locals}) {
    if(!locals.user){
        redirect(303,"/login")
    } else if(locals.user.access_level==="Read"){
        redirect(303,"/dashboard")
    }
}