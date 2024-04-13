import { error, redirect } from '@sveltejs/kit';
import { verifyJWT } from './lib/jwtHadlers';




export async function handle({ event, resolve }) {


	let authToken = event.cookies.get('user');
	try {
		if (authToken) {
			const { user } = await verifyJWT(authToken);
			
			if (!user) {
					throw error(401, 'User belonging to this token no longer exists');
				}

				


			event.locals.user = user;
		}
	} catch (err) {
		console.log(err)
		event.cookies.delete('user', { path: "/" })
       
		event.locals.user = null;
		if (event.url.pathname.startsWith('/dashboard')) {
			throw redirect(303, "/login")
		}
	}


	
	return await resolve(event);
}
