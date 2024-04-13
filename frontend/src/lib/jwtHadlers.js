// @ts-nocheck
import { JWT_SECRET_KEY,JWT_EXPIRES_IN } from '$env/static/private';
import { SignJWT, jwtVerify } from 'jose';

export const signJWT = async (payload, options={exp:"168h"}) => {
	try {
		const secret = new TextEncoder().encode(JWT_SECRET_KEY);
		const alg = 'HS256';
		return new SignJWT(payload)
			.setProtectedHeader({ alg })
			.setExpirationTime(options.exp)
			.setIssuedAt()
			.sign(secret);
	} catch (error) {
		throw error;
	}
};
export const verifyJWT = async (token)=>{
	try {
		return (await jwtVerify(token, new TextEncoder().encode(JWT_SECRET_KEY))).payload;
	} catch (error) {
        
		console.log(error)
		return ({user:null})
	}
};
