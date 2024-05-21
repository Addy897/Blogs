import { handlers } from '../../../lib/handlers';
import { signJWT } from '../../../lib/jwtHadlers';
import { v2 as cloudinary } from 'cloudinary';
import { API_KEY, CLOUD_NAME, API_SECRET } from "$env/static/private";

cloudinary.config({
    cloud_name: CLOUD_NAME,
    api_key: API_KEY,
    api_secret: API_SECRET,
    secure: true,
});
async function uploadProfileImage(file){
        let pf_URL=null
        let filedata=await file.arrayBuffer();
        const buffer = new Uint8Array(filedata);
        const uploadStream = await new Promise((resolve, reject) => {
            cloudinary.uploader
                .upload_stream({
                    folder: '',
                    resource_type: 'image'}, function (error, result) {
                    if (error) {
                        return reject(error);
                    }
                    return resolve(result);
                })
                .end(buffer);
        });
    if(!uploadStream.Error){
        pf_URL=uploadStream.url;
    }
    return pf_URL
}
/** @type {import('./$types').RequestHandler} */
export async function POST({request,locals,cookies}) {
        let data=await request.formData();
        let name = data.get('name')
        let file = data.get('profile')
        if(file){
            file = await uploadProfileImage(file);
        }
        if(locals.user){
        let resp=await handlers.save(locals.user,name,file);
        if(resp.error){
            return new Response(JSON.stringify({error:resp.errorMessage}))
        }
        let token = null
        try {
            token = await signJWT({ user: resp })
            
        } catch (e) {
            console.log(e)
            throw redirect(303, "/login")
        }
        if (!token) {
            throw redirect(303, "/login")
        }
        cookies.delete("user", {
            httpOnly: true,
            sameSite: 'strict',
            secure: false,
            path: '/',
            maxAge: 60 * 60 * 24 * 7
        })
        cookies.set("user", token, {
            httpOnly: true,
            sameSite: 'strict',
            secure: false,
            path: '/',
            maxAge: 60 * 60 * 24 * 7
        })
        return   new Response(JSON.stringify({sucess:true}))
        }else{
            goto("/login")
        }
    
    return new Response(JSON.stringify({error:false}));
}