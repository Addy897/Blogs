
<script>
	import { enhance } from "$app/forms";
    import {
    signInWithPopup,
    GoogleAuthProvider,
  } from "firebase/auth";
  import { auth } from "$lib/firebase_auth";
	import ShowLoading from "../../lib/components/showLoading.svelte";
    export let form;
    let login=true;
    let logging=false;
    const google = async () => {
    const provider = new GoogleAuthProvider();
    let user = null;
    logging = true;
    signInWithPopup(auth, provider)
      .then((res) => {
        user = res.user;
        let formData=new FormData()
        formData.append("user",JSON.stringify(user))
        if (user) {
          fetch("?/google", {
            method: "POST",
            body: formData,
          })
            .then(async (resp) => {
                let r=await resp.json()
                
                if(r.data && r.data!=="-1"){
                    r=JSON.parse(JSON.parse(r.data)[0])
                    if(r.serror){
                        form=r
                        logging=false
                        return;
                    }
                }
              location.href="/dashboard"
            })
            .catch((err) => {
              form={serror:true,errormsg:err};
              logging = false;
            });
        }
        
      })
      .catch((error) => {
        form={serror:true,errormsg:error.message};
        logging = false;
      });
    };
</script>

<div class="body-bg min-h-screen pt-12 md:pt-20 pb-6 px-2 md:px-0" style="font-family:'Lato',sans-serif;">
    {#if logging}
        <ShowLoading/>
    {:else if login}
        <div class="bg-white max-w-lg mx-auto p-8 md:p-12 my-10 rounded-lg shadow-2xl">
            <section>
                <h3 class="font-extrabold text-2xl">Welcome to EJY<span class="text-red-600">health</span></h3>
                <p class="text-gray-600 pt-2">Sign in to your account.</p>
            </section>

            <section class="flex flex-col justify-center items-center w-full">
                <form class="flex flex-col w-full" method="post"
                action="?/login"
                use:enhance={() => {
                    logging = true;
            
                    return async ({ update }) => {
                        await update();
                        logging = false;
                    };
                }}>
                    <div class="mb-3 pt-3 rounded-xl bg-gray-200">
                        <label class="block text-gray-700 text-sm font-bold mb-2 ml-3" for="email">Email</label>
                        <input type="text" id="email" name="email" class="bg-gray-200 rounded-xl w-full text-gray-700 focus:outline-none border-b-4 border-gray-300 focus:border-purple-600 transition duration-500 px-3 pb-3">
                    </div>
                    <span class="text-lg md:text-xl font-mono flex justify-center w-full">Or</span>
                    <div class="mb-6 pt-3 rounded-xl bg-gray-200">
                        <label class="block text-gray-700 text-sm font-bold mb-2 ml-3" for="phone">Phone</label>
                        <input type="number" id="phone" name="phone" class="bg-gray-200 rounded-xl w-full text-gray-700 focus:outline-none border-b-4 border-gray-300 focus:border-purple-600 transition duration-500 px-3 pb-3">
                    </div>
                    <div class="mb-6 pt-3 rounded-xl bg-gray-200">
                        <label class="block text-gray-700 text-sm font-bold mb-2 ml-3" for="password">Password</label>
                        <input type="password" id="password" name="password" class="bg-gray-200 rounded-xl w-full text-gray-700 focus:outline-none border-b-4 border-gray-300 focus:border-purple-600 transition duration-500 px-3 pb-3" required>
                    </div>
                    <div class="flex justify-between">
                        <a href="/" class="text-sm text-red-600 hover:text-red-700 hover:underline mb-6">Forgot your password?</a>
                        {#if form?.serror}
                            <div class="text-red-900">{form?.errormsg}</div>
                        {/if}
                    </div>
                    
                    <button class="bg-red-500 hover:bg-red-600 text-white font-bold py-2 rounded-3xl shadow-lg hover:shadow-xl transition duration-200" type="submit">Sign In</button>
                    <button
          class="mt-4 px-4 py-2 w-full justify-center bg-white border-black text-black border flex gap-2 rounded-3xl shadow-lg"
          type="button"
          on:click={google}
        >
          <img
            class="w-6 h-6"
            src="https://www.svgrepo.com/show/475656/google-color.svg"
            loading="lazy"
            alt="google logo"
          />
          <span>Login with Google</span>
                    </button>
                </form>
            </section>
        </div>

        <div class="max-w-lg mx-auto text-center mt-12 mb-6">
            <p class="text-black">Don't have an account? <button href="None" class="font-bold hover:underline" tabindex="-1"  on:click={()=>{login=!login}}>Sign up</button>.</p>
        </div>

        <div class="max-w-lg mx-auto flex justify-center text-black">
            <a href="/" class="hover:underline">Contact</a>
            <span class="mx-3">•</span>
            <a href="/" class="hover:underline">Privacy</a>
        </div>
        
    {:else}
        <div class="bg-white max-w-lg mx-auto p-8 md:p-12 my-10 rounded-lg shadow-2xl">
            <section>
                <h3 class="font-extrabold text-2xl">Welcome to EJY<span class="text-red-600">health</span></h3>
                <p class="text-gray-600 pt-2">Sign up to your account.</p>
            </section>

            <section class="mt-10">
                <form class="flex flex-col" method="post"
                action="?/signup"
                use:enhance={() => {
                    logging = true;
            
                    return async ({ update }) => {
                        await update();
                        logging = false;
                    };
                }}>
                    <div class="mb-6 pt-3 rounded-xl bg-gray-200">
                        <label class="block text-gray-700 text-sm font-bold mb-2 ml-3" for="name">Name</label>
                        <input type="text" id="name" name="name" class="bg-gray-200 rounded-xl w-full text-gray-700 focus:outline-none border-b-4 border-gray-300 focus:border-purple-600 transition duration-500 px-3 pb-3 -xl" required>
                    </div>
                    <div class="mb-6 pt-3 rounded-xl bg-gray-200">
                        <label class="block text-gray-700 text-sm font-bold mb-2 ml-3" for="email">Email</label>
                        <input type="text" id="email" name="email" class="bg-gray-200 rounded-xl w-full text-gray-700 focus:outline-none border-b-4 border-gray-300 focus:border-purple-600 transition duration-500 px-3 pb-3">
                    </div>
                    <div class="mb-6 pt-3 rounded-xl bg-gray-200">
                        <label class="block text-gray-700 text-sm font-bold mb-2 ml-3" for="phone">Phone</label>
                        <input type="number" id="phone" name="phone" class="bg-gray-200 rounded-xl w-full text-gray-700 focus:outline-none border-b-4 border-gray-300 focus:border-purple-600 transition duration-500 px-3 pb-3">
                    </div>
                    <div class="mb-6 pt-3 rounded-xl bg-gray-200">
                        <label class="block text-gray-700 text-sm font-bold mb-2 ml-3" for="password">Password</label>
                        <input type="password" id="password" name="password" class="bg-gray-200 rounded-xl w-full text-gray-700 focus:outline-none border-b-4 border-gray-300 focus:border-purple-600 transition duration-500 px-3 pb-3" required>
                    </div>
                    <div class="mb-6 pt-3 rounded-xl bg-gray-200">
                        <label class="block text-gray-700 text-sm font-bold mb-2 ml-3" for="confirm_password">Confirm Password</label>
                        <input type="password" id="confirm_password" name="cpassword" class="bg-gray-200 rounded-xl w-full text-gray-700 focus:outline-none border-b-4 border-gray-300 focus:border-purple-600 transition duration-500 px-3 pb-3" required>
                    </div>
                    <div class="flex justify-between">
                        {#if form?.serror}
                            <div class="text-red-800">{form?.errormsg}</div>
                        {/if}
                    </div>
                    
                    <button class="bg-red-500 hover:bg-red-600 text-white font-bold py-2 rounded-3xl shadow-lg hover:shadow-xl transition duration-200" type="submit">Sign In</button>
                </form>
            </section>
        </div>

        <div class="max-w-lg mx-auto text-center mt-12 mb-6">
            <p class="text-black">Already have an account? <button href="None" class="font-bold hover:underline" tabindex="-1"  on:click={()=>{login=!login}}>Sign in</button>.</p>
        </div>

        <div class="max-w-lg mx-auto flex justify-center text-black">
            <a href="/" class="hover:underline">Contact</a>
            <span class="mx-3">•</span>
            <a href="/" class="hover:underline">Privacy</a>
        </div>
    {/if}

</div>