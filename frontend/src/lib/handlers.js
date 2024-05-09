
import { BACKEND_URL } from "$env/static/private"
import { API_TOKEN } from "$env/static/private"

export class handlers {
    /*
  static async signup(email, pass) {
    let user = null;
    let Code = 200;
    let msg = "";
    await createUserWithEmailAndPassword(auth, email, pass).then((userCredential) => {
      user = userCredential.user;
    })
      .catch((error) => {
        Code = error.code;
        msg = error.message;
      });
    if (Code !== 200) {
      msg = msg.split(":")[1]
      return ({ "Code": Code, "errorMessage": msg });
    }
    return ({ Code: Code, user: user })
  }
  static async updateUser(details) {
    let Code = 200;
    let msg = "";
    await updateProfile(auth.currentUser, details).then(() => {

    }).catch((error) => {
      Code = error.code;
      msg = error.message;
    });
    if (Code !== 200) {
      msg = msg.split(":")[1]
      return ({ "Code": Code, "errorMessage": msg });
    }
    return ({ Code: Code })
  }
  static async removeUser(user) {
    let Code = 200;
    let msg = "";
    await deleteUser(user).then(() => {

    }).catch((error) => {
      Code = error.code;
      msg = error.message;
    });
    if (Code !== 200) {
      msg = msg.split(":")[1]
      return ({ "Code": Code, "errorMessage": msg });
    }
    return ({ Code: Code })
  }
  static async singIn(email, pass) {
    let user = null;
    let Code = 200;
    let msg = "";
    await signInWithEmailAndPassword(auth, email, pass)
      .then((userCredential) => {
        user = userCredential.user;

      })
      .catch((error) => {
        Code = error.code;
        msg = error.message;
      });
    if (Code !== 200) {
      msg = msg.split(":")[1]
      return ({ "Code": Code, "errorMessage": msg });
    }
    return ({ Code: Code, user: user })
  }
  static async sendVerification(user) {

    await sendEmailVerification(auth.currentUser)
      .then(() => { })
      .catch((err) => { });

  }
  static async resetPass(email) {
    let Code = 200;
    let msg = "";
    await sendPasswordResetEmail(auth, email)
      .then(() => {
      })
      .catch((error) => {
        Code = error.code;
        msg = error.message
      });
    if (Code !== 200) {
      msg = msg.split(":")[1]
      return ({ "Code": Code, "errorMessage": msg });
    }
    return ({ Code: Code })
  }
  static async signout() {
    let Code = 200;
    let msg = "";
    await signOut(auth).then(() => {
    }).catch((error) => {
      Code = error.code;
      msg = error.message;
    });
    if (Code !== 200) {
      msg = msg.split(":")[1]
      return ({ "Code": Code, "errorMessage": msg });
    }
    return ({ Code: Code })
  }
*/
static async addGoogle(guser){
  let user = null;
  let Code = 200;
  let msg = "";
  try {
    const rawResponse = await fetch(BACKEND_URL+"users/google/", {

      method: "Post",
      headers: {
        'Accept': 'application/json',
        'api-token': API_TOKEN,
      },
      body: JSON.stringify({
        'guser':guser
      })
    });
    user = await rawResponse.json();
  } catch (error) {
    console.log("Error: ",error)
    Code = 404;
    msg = error;
  }
  if (Code !== 200 || !user) {
    return ({ "Code": Code, "errorMessage": msg });
  } else {
    return ({ Code: Code, user: user })
  }
}
  static async signUp(details) {
      
    let user = null;
    let Code = 200;
    let msg = "";
    try {
      const rawResponse = await fetch(BACKEND_URL+"users/register/", {

        method: "Post",
        headers: {
          'Accept': 'application/json',
          'api-token': API_TOKEN,
        },
        body: JSON.stringify({
          "email": details.email,
          "password": details.password,
          "name": details.name,
          "phone": details.phone
        })
      });
      user = await rawResponse.json();
    } catch (error) {
      console.log("Error: ",error)
      Code = 404;
      msg = error;
    }
    if (Code !== 200 || user.Error===true) {
      return ({ "Code": 404, "errorMessage": user.message || msg });
    } else {
      return ({ Code: Code, user: user })
    }
  }

  static async singIn(email,phone, pass) {

    let user = null;
    let Code = 200;
    let msg = "";
    try {
      const rawResponse = await fetch(BACKEND_URL+"users/login/", {

        method: "Post",
        headers: {
          'Accept': 'application/json',
          'api-token': API_TOKEN,
        },
        body: JSON.stringify({
          "email": email,
          "phone": phone,
          "password": pass
        })
      });
      user = await rawResponse.json();
    } catch (error) {
      Code = 404;
      msg = error;
    }
    if (Code !== 200 || user.Error===true) {
      return ({ "Code": 404, "errorMessage": user.message });
    } else {
      return ({ Code: Code, user: user })
    }
  }
  static async getUserBlog(user,title=null) {
    let response=null
    
    await fetch(BACKEND_URL + "getUserBlog/", {
      method: "POST",
      headers: {
        'api-token': API_TOKEN,
      },
      
      body: JSON.stringify({
        'email': user,
        'title': String(title),
      })
    }).then(async (respo) => {
       response= await respo.json();
        response=response.response
    }).catch((err) => {
      
    })

    return ({draft:response})
  }
  static async setUserBlog(user,title,description, delta,cover_photo,status,topic,tag,domain) {
    let r = { error: false }
    await fetch(BACKEND_URL + "setUserBlog/", {
      method: "POST",
      headers: {
        'api-token': API_TOKEN,
      },
      body: JSON.stringify({
        'user': user,
        'title':title,
        'description':description,
        'delta': delta,
        'tag': tag,
        'topic': topic,
        'status': status ,
        'domain': domain ,
        'cover_photo':cover_photo
      })
    }).then(async (respo) => {
      r = await respo.json()
      
    }).catch((err) => {
      
    })
    if (r.error) {
      return ({ error: r.errorMessage })
    }
    return {error:false,resposne:r}

  }
  static async likeCount(user, ref_id) {
    let r = { code: false }
    const res = await fetch(BACKEND_URL + "updateLikes/", {
      method: "POST", headers: {
        'api-token': API_TOKEN,
      }, body: JSON.stringify({
        "ref_id": String(ref_id),
        "user": user
      })
    }).then(async (response)=>{
      r = await response.json();
    })
    return r;
  }
  static async incView(ref_id) {
    let r = { code: false }
    const res = await fetch(BACKEND_URL + "incView/", {
      method: "POST", headers: {
        'api-token': API_TOKEN,
      }, body: JSON.stringify({
        "ref_id": ref_id
      })
    }).then(async (response)=>{
      r = await response.json();
    }).catch((err)=>{
      console.log(err)
    })
    return r;
  }
  static async save(user,name,file) {
    let r = { error: true }
    const res = await fetch(BACKEND_URL + "saveProfile/", {
      method: "POST", headers: {
        'api-token': API_TOKEN,
      }, body: JSON.stringify({
        "user":user,
        "name": name,
        "file":file
      })
    }).then(async (response)=>{
      r = await response.json();
    }).catch((err)=>{
      console.log(err)
    })
    return r;
  }
  static async getBlogs(title=null) {
    let blog = null
    await fetch(BACKEND_URL + "getBlog/", {
      method: "POST",
      headers: {
        'api-token': API_TOKEN,
      },
      body: JSON.stringify({
        'title':title,
        
      })
    }).then(async (respo) => {
      var response = await respo.json();
      blog=response.response;
    }).catch((err) => {
      console.log(err)
    })

    return ({ blog: blog })
  }
  static async getAllBlogs(title=null) {
    let blog = null
    await fetch(BACKEND_URL + "getAllBlogs/", {
      method: "POST",
      headers: {
        'api-token': API_TOKEN,
      },
      body: JSON.stringify({
        'title':String(title),
        
      })
    }).then(async (respo) => {
      
      var response = await respo.json();
      
      blog=response.response;
    }).catch((err) => {
      console.log(err)
    })

    return ({ blog: blog })
  }
  static async getUserDraft(user,title) {
    let response=null
    
    await fetch(BACKEND_URL + "getUserDraft/", {
      method: "POST",
      headers: {
        'api-token': API_TOKEN,
      },
      
      body: JSON.stringify({
        'user': user,
        'title': String(title),
      })
    }).then(async (respo) => {
       response= await respo.json();
        response=response.response
        return response

    }).catch((err) => {
      
    })

    return ({draft:response})
  }
  
  static async addComment(user,comment,title){
    let r = { code: false }
    const res = await fetch(BACKEND_URL + "addComment/", {
      method: "POST", headers: {
        'api-token': API_TOKEN,
      }, body: JSON.stringify({
        "comment":comment,
        "user": user,
        "title":title
      })
    }).then(async (response)=>{
      r = await response.json();
    })
    return r;
  }
  static async publishUserBlog(user, ref_id) {
    let r = { error: false }
    const res = await fetch(BACKEND_URL + "publishUserBlog/", {
      method: "POST", headers: {
        'api-token': API_TOKEN,
      }, body: JSON.stringify({
        "ref_id": String(ref_id),
        "user": user
      })
    }).then(async (response)=>{
      r = await response.json();
    })
    return r;
  }
  static async edithUserBlog(user, delta,ref_id) {
    let r = { error: false }
    const res = await fetch(BACKEND_URL + "editUserBlog/", {
      method: "POST", headers: {
        'api-token': API_TOKEN,
      }, body: JSON.stringify({
        "ref_id": String(ref_id),
        "delta": delta,
        "user": user
      })
    }).then(async (response)=>{
      r = await response.json();
    })
    return r;
  }
  static async getForReviewBlogs(user,title=null) {
    let response=null
    
    await fetch(BACKEND_URL + "getForReviewBlogs/", {
      method: "POST",
      headers: {
        'api-token': API_TOKEN,
      },
      
      body: JSON.stringify({
        'user': user,
        'title':String(title)
      })
    }).then(async (respo) => {
       response= await respo.json();
        response=response.response
        return response

    }).catch((err) => {
      
    })

    return ({draft:response})
  }
  static async removeComment(cid,cuid){
    let r = { code: false }
    await fetch(BACKEND_URL + "removeComment/", {
      method: "POST", headers: {
        'api-token': API_TOKEN,
      }, body: JSON.stringify({
        "cid": cid,
        "cuid":cuid
      })
    }).then(async (response)=>{
      r = await response.json();
    })
    return r;
  }
  
}

