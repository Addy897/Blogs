
<script>
	import {loginStore} from "./../stores/loginstore"
    import icon from "$lib/images/icon.png"
	import { browser } from "$app/environment";
    $: isVisible = false;
        const showNav = () => {
        isVisible = !isVisible;
    };
    
	let isactive=(browser)?window.location.pathname.substring(1):"home";
    const changeIsActive=(current)=>{isactive=current};
   
    let navButtonClass =
        "w-full sm:pl-0 cursor-pointer sm:w-auto max-sm:hover:text-black max-sm:hover:bg-white sm:hover:text-2xl lg:mx-3 px-2 shadow-md rounded-lg flex justify-center flex-row items-center text-center";
    navButtonClass = "";
</script>

<nav class="bg-white p-4 border-b-2">
    <div class="container mx-auto flex justify-evenly md:justify-between items-center flex-wrap gap-5">
        <div class="w-1/2 md:w-auto">
           <img src={icon} alt="icon"/>
        </div>
        <div class="md:hidden absolute left-[90%]">
            <button
                id="mobile-menu-button"
                class="text-black focus:outline-none"
                on:click={showNav}
            >
                <i class={!isVisible ? "fa fa-bars" : "fa fa-xmark"}></i>
            </button>
        </div>
        <div class="hidden md:flex flex-row justify-center items-center text-xl font-sans gap-5">
            <a
                href="/"                    
                class="border-solid  block px-3 py-2 rounded-lg font-medium {!isactive.startsWith('home')?"text-black":"text-red-600"}"
                on:click={()=>{changeIsActive("home")}}
                >Home</a
            >
            <a
                href="/about"   
                class=" border-solid   block px-3 py-2 rounded-lg font-medium {!isactive.startsWith('about')?"text-black":"text-red-600"}"
                on:click={()=>{changeIsActive("about")}}
                >About</a
            >
            {#if $loginStore.isLogged}
                <a
					href="/dashboard"
                    class="border-solid   flex flex-row items-center gap-3 justify-center px-3 py-2 rounded-lg font-medium {!isactive.startsWith('dashboard')?"text-black":"text-red-600"}"
                    on:click={()=>{changeIsActive("dashboard")}}
                    >{$loginStore.userName}
                        <img
                            class="rounded-full h-12 w-12"
                            src={$loginStore.pf_photo}
                            alt=""
                            referrerpolicy="no-referrer"
                        />
                    </a
                >
                
                
            {:else}
                <a 
					href="/login"
                    class="  block px-3 py-2 rounded-lg font-medium {!isactive.startsWith('login')?"text-black":"text-red-600"}"
                    on:click={()=>{changeIsActive("login")}}

                    >Login</a
                >
            {/if}
        </div>
        <div>
        <a href=" " class="inline-block mt-2 bg-[#FF3A1D] text-white font-bold py-2 px-8 rounded-full">Join the waitlist</a>
        </div>


    </div>

</nav>

<!-- Mobile Menu -->
<div
    class="md:hidden bg-white absolute left-0 top-0 h-full w-48 z-50 {!isVisible
        ? 'hidden'
        : ''}"
>
    <div
        class="flex flex-col justify-center items-center px-2 pt-2 pb-3 space-y-1 gap-5"
    >
        <img src={icon} alt="icon" class="py-2 px-3 border-b-2 w-full flex justify-center text-black"
            
        />

        <button
            on:click={() => {
                
                  location.href="/"

            }}
            class="text-black  block px-3 py-2 rounded-md font-medium"
            >Home</button
        >
        <button
            on:click={() => {
               location.href="/about"
               
            }}
            class="text-black  block px-3 py-2 rounded-md font-medium"
            data-sveltekit-preload-data="hover"
            >about</button
        >
        {#if $loginStore.isLogged}
            <a
                href="/dashboard"
                on:click={()=>{isVisible=false}} 
                
                class="text-black  flex flex-row px-3 py-2 rounded-md font-medium gap-2"
               
                >{$loginStore.userName}<img
                class="rounded-full h-7 w-7 "
                src={$loginStore.pf_photo}
                alt=""
                referrerpolicy="no-referrer"
            /></a
            >
           
        {:else}
            <button
                on:click={() => {
                    location.href="/login"
                }}
                class="text-black  block px-3 py-2 rounded-md font-medium"
                >Login</button
            >
        {/if}
    </div>
</div>

