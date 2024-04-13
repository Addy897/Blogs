import { firebaseApp } from "./firebase_config";
import {getAuth} from "firebase/auth";

export const auth=getAuth(firebaseApp)