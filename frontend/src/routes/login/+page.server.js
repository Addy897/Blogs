
import { handlers } from "$lib/handlers";
import { signJWT } from "$lib/jwtHadlers";
import { fail, redirect } from "@sveltejs/kit";
/** @type {import('./$types').PageServerLoad} */
export async function load({ locals }) {

    if (locals.user) {
        

        throw redirect(303, "/")
    }


}
/** @type {import('./$types').Actions} */
export const actions = {
    login: async ({ request, cookies }) => {
        let formData = await request.formData();
        let email = formData.get('email')?.toString();
        let phone = formData.get('phone')?.toString();

        let password = formData.get('password')?.toString();
        if (email || phone) {
            if (phone && phone.length != 10) {
                return fail(400, { errormsg: "Invaild Phone", serror: true })
            }
            if (password) {
                let user = await handlers.singIn(email,phone, password)
               
                if (!user.user || user.Code !== 200) {
                    if (user.errorMessage) {
                        return fail(400, { errormsg: user.errorMessage, serror: true });
                    }
                    return fail(400, { errormsg: "Invalid Id Or Password", serror: true });

                }
                let token = null
                try {
                    token = await signJWT({ user: user.user })
                } catch (e) {
                    console.log(e)
                    throw redirect(303, "/login")
                }
                if (!token) {
                    throw redirect(303, "/login")
                }
                cookies.set("user", token, {
                    httpOnly: true,
                    sameSite: 'strict',
                    secure: false,
                    path: '/',
                    maxAge: 60 * 60 * 24 * 7
                })

            }else{
                
                return fail(400, { errormsg: "Password is Required", serror: true })
            }
        } else{
                return fail(400, { errormsg: "Enter Email or Phone", serror: true })
            }
    },
    signup: async ({ request, cookies }) => {
        let formData = await request.formData();
        let email = formData.get('email')?.toString();
        let phone = formData.get('phone')?.toString();
        let password = formData.get('password')?.toString();
        let cpassword = formData.get('cpassword')?.toString();
        let name = formData.get('name')?.toString();
        if (email || phone) {
            if (phone && phone.length != 10) {
                return fail(400, { errormsg: "Invaild Phone", serror: true })
            }
            if (password) {
                if (password !== cpassword) {
                    return fail(400, { errormsg: "Passwords are not same", serror: true });
                }
                let user = await handlers.signUp({ email: email,phone:phone, password: password, name: name })
                if (!user.user || user.Code !== 200) {
                    if (user.errorMessage) {
                        return fail(400, { errormsg: user.errorMessage, serror: true });
                    }
                    return fail(400, { errormsg: "Unknown Error Occured", serror: true });

                }
                let token = null
                try {
                    token = await signJWT({ user: user.user })
                } catch (e) {
                    console.log(e)
                    throw redirect(303, "/login")
                }
                if (!token) {
                    throw redirect(303, "/login")
                }
                cookies.set("user", token, {
                    httpOnly: true,
                    sameSite: 'strict',
                    secure: false,
                    path: '/',
                    maxAge: 60 * 60 * 24 * 7
                })

            }
        }
    },
    logout: async ({ request, cookies }) => {
        cookies.delete("user", {
            httpOnly: true,
            sameSite: 'strict',
            secure: false,
            path: '/',
            maxAge: 60 * 60 * 24 * 7
        })
        throw redirect(301, "/login")

    },
    google:async({request,cookies})=>{
        let formData = await request.formData();
        let guser= JSON.parse(formData.get('user'))
        let user= await handlers.addGoogle(guser)
        if (!user.user || user.Code !== 200) {
            if (user.errorMessage) {
                return fail(400, { errormsg: user.errorMessage, serror: true });
            }
            return fail(400,{ errormsg: "Account already exist with same email", serror: true });

        }
        let token = null
        try {
            token = await signJWT({ user: user.user })
        } catch (e) {
            console.log(e)
            throw redirect(303, "/login")
        }
        if (!token) {
            throw redirect(303, "/login")
        }
        cookies.set("user", token, {
            httpOnly: true,
            sameSite: 'strict',
            secure: false,
            path: '/',
            maxAge: 60 * 60 * 24 * 7
        })

  
    }
};
