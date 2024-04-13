import { browser } from "$app/environment"
import { redirect } from "@sveltejs/kit"
import {loginStore} from "../../stores/loginstore"

/** @type {import('./$types').PageLoad} */
export async function load({data}) {
    if(data && data.user){
        return data
    }
}