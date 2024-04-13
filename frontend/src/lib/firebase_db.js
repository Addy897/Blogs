import { getFirestore } from "firebase/firestore";
import { firebaseApp } from "./firebase_config";
export const db = getFirestore(firebaseApp);
