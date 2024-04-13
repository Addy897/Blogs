import { deleteApp, getApp, getApps, initializeApp } from "firebase/app";
const firebaseConfig = {
  apiKey: import.meta.env.VITE_APIKEY,
  authDomain: import.meta.env.VITE_authDomain,
  projectId: import.meta.env.VITE_projectId,
  storageBucket: import.meta.env.VITE_storageBucket,
  messagingSenderId: import.meta.env.VITE_messagingSenderId,
  appId: import.meta.env.VITE_appId,
  measurementId: import.meta.env.VITE_measurementId
};

// Initialize Firebase
let fApp;
if(!getApps().length){
    fApp=initializeApp(firebaseConfig,{experimentalForceLongPolling: true, // this line
    useFetchStreams: false});
}else{
    deleteApp(getApp(firebaseConfig));
    fApp=initializeApp(firebaseConfig,{experimentalForceLongPolling: true, // this line
    useFetchStreams: false});
}
export const firebaseApp=fApp;