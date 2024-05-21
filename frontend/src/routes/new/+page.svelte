<script>
    import { browser } from '$app/environment';
	import ShowLoading from "../../lib/components/showLoading.svelte";
  import BlogView from '$lib/components/blogView.svelte';
	import { loginStore } from '../../stores/loginstore';
	import CustomQuil from "../../lib/components/customQuil.svelte";
	import {addToast} from "../../lib/components/toast/store.js";
	import Toasts from '../../lib/components/toast/Toasts.svelte';

    let loading =false;
    let blogTitle = "";
    let blogDescription = "";
    let delta = null;
    let domain = "General";
    let htmlContent = "";
    let preview = false;
    let f = [];
    let error=null;
  
    const toolbarOptions = [
  [{ 'font': [] }],
  ['bold', 'italic', 'underline', 'strike'], 

  [{ 'size': ['small', false, 'large', 'huge'] }],  // custom dropdown

  [{ 'header': 1 }, { 'header': 2 }],              
  ['blockquote', 'code-block'],
  ['link', 'image', 'video'],

  [{ 'list': 'ordered'}, { 'list': 'bullet' }, { 'list': 'check' }],
  [{ 'script': 'sub'}, { 'script': 'super' }],      // superscript/subscript
  [{ 'indent': '-1'}, { 'indent': '+1' }],          // outdent/indent
  [{ 'direction': 'rtl' }],                         // text direction

  [{ 'header': [1, 2, 3, 4, 5, 6, false] }],

  [{ 'color': [] }, { 'background': [] }],          // dropdown with defaults from theme
  [{ 'align': [] }],

  ['clean']                                         // remove formatting button
];
  
  let show=false
  let message = null;
  let type = "success";
  let dismissible = true;
  let timeout = 0;
    $:if(show){
      addToast({message, type, dismissible, timeout })
      show=false;
    }
  const toggleMode = (event)=>{
    preview=!preview;
  }
   
    
   
   
    function wait (time) {
  return new Promise((resolve) => {
    setTimeout(resolve, time);
  });
}
    const handleDraft = async (event) => {
      loading=true;
      event.preventDefault();
      let action="Draft"
      if(event.srcElement.innerText==="Publish"){
       action="Publish"
      }
      let cUrl;
      if(!blogTitle || ! blogDescription){
          
          message="Please Enter Title or Description"
          type="error"
          loading=false;
          show=true;
          return
      }
      await fetch("new/image",{
        method:"POST",
        headers:{ "Content-Type": "application/json" },
        body:JSON.stringify({cover_photo:iSrc}),
      }).then(async (response)=>{
            let resp=await response.json()
            cUrl=resp.url
          }).catch((err)=>{
            cUrl=null
          })
      const data={"cover_photo":cUrl,"topic":topic,"description":blogDescription,"title":blogTitle,"delta":JSON.stringify(delta),"action":action,"tag":tag,"domain":domain}
          
        await fetch("new/api/",{
            method:"POST",
            headers: { "Content-Type": "application/json" },

            body:JSON.stringify(data),
        }).then(async (response)=>{
            let resp=await response.json()
           
            let e=resp.error
            if(e){
              
                error=resp.msg||e;
                message=error
                type="error"
                loading=false;
                show=true;
                delta=resp.delta||delta
            }else{
                error=null
                timeout=3000;
                type="success"

                if(action==="Draft"){
                  message="Saved the Blog to Draft";
                 
                  
                }else{
                  message="Sucessfully Published Blog.The Blog is InReview Process."
                }
                loading=false;
                show=true;
                await wait(timeout)
                window.location=`dashboard/${encodeURI(blogTitle)}?for=draft`
            }
            
        }).catch((err)=>{
          loading=false;
          type="error"
          message=err;
          show=true;
        });  
    }
    let topics=['Topic 1','Topic 2','Topic 3','Misc']
    let tags= ["All", "Mens", "Female", "LGBTQ"]
    let topic=topics[0];
    let tag=tags[0];
    let iSrc = 'https://flowbite.com/docs/images/blog/image-1.jpg'; 
    let cover_photo=null;
    $: if(!iSrc){cover_photo=null;iSrc="https://flowbite.com/docs/images/blog/image-1.jpg"};
    $: blog ={author:{name:$loginStore.userName},cover_photo:iSrc,date:new Date().getDate(),title:blogTitle,description:blogDescription,delta:delta,topic:topic,domain:domain}
function handleCoverPhoto(event) {
   cover_photo = event.target.files[0]; 
  if (cover_photo) {
    const reader = new FileReader();
    reader.onloadend = () => {
      iSrc = reader.result; 
    };
    reader.readAsDataURL(cover_photo); 
  }
}
  </script>
  <svelte:head>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/quill@2.0.1/dist/quill.snow.css" rel="stylesheet">

  </svelte:head>
  
  {#if loading}
  <div class="flex flex-col items-center">
      <ShowLoading/>
  </div>
  {:else}
  <div class="flex flex-col items-center">
    <Toasts/>
    {#if preview}
        <BlogView blog={blog}/>
    {:else}
      <form class="flex flex-col items-center w-full p-4 gap-2" method="post">
        
        <div class="flex gap-2">
          <label for="cover_photo" class="cursor-pointer bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
            Add Cover Image
            <input type="file" id="cover_photo" accept="image/*" class="hidden" on:change={handleCoverPhoto}>
          </label>          
          {#if cover_photo}
          <img src={iSrc} alt=" " class="h-10 w-10 rounded-full">
          <button type="button" class="bg-red-500 hover:bg-red-700 text-white font-bold py-1 px-2 rounded" on:click={() => iSrc=null}>Remove</button>          {/if}
        </div>
        <input type="text" placeholder="Title" bind:value={blogTitle} class="mb-2 p-2 border border-gray-400 rounded">
        <input type="text" placeholder="Description" bind:value={blogDescription} class="mb-2 p-2 border border-gray-400 rounded">
        <input type="text" placeholder="Domain" bind:value={domain} class="mb-2 p-2 border border-gray-400 rounded">
        <div class=" flex flex-row gap-5">
          <label for="topic">Topic:</label>
        <select id="topic" bind:value={topic} required>
            {#each Object.entries(topics) as [index,value] }
              {#if index===0}
              <option value="{value}" selected="selected">{value}</option>
              {:else}
              <option value="{value}">{value}</option>

              {/if}
            {/each}
        </select>
        <label for="tag">Tag:</label>

        <select id="tag" bind:value={tag} required>
          {#each Object.entries(tags) as [index,value] }
            {#if index===0}
            <option value="{value}" selected="selected">{value}</option>
            {:else}
            <option value="{value}">{value}</option>

            {/if}
          {/each}
      </select></div>
        <CustomQuil  toolbarOptions={toolbarOptions} f={f} bind:htmlContent={htmlContent} bind:delta={delta} />
    
        <div class="flex justify-between w-full sm:w-auto mb-10">
          <button type="submit" class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded mt-4 mr-2" on:click={handleDraft}>Publish</button>
          <button type="button" class="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded mt-4 ml-2" on:click={handleDraft}>Save as Draft</button>
          
        </div>
        
      </form>
    {/if}
  </div>
  <div class="fixed bottom-4">
    <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" on:click={toggleMode}>
      {preview ? 'Edit ' : 'Preview'}
    </button>
  </div>
  
  {/if}