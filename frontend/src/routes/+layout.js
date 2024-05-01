import { browser } from '$app/environment';
import { loginStore } from '../stores/loginstore';

/** @type {import('./$types').LayoutLoad} */
export async function load({data}) {
    if(browser){
        if(data && data.user){
            loginStore.set({isLogged:true,userName:data.user.displayName,pf_photo:data.user.pf_photo})
        }
        else{
            loginStore.set({isLogged:false,userName:null,pf_photo:null})
        }
    }
    return data
}