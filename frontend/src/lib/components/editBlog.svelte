
<script>
    
	import BlogView from "./blogView.svelte";
	import { loginStore } from "../../stores/loginstore";
	import CustomQuil from "./customQuil.svelte";

   

    
    
    export let blogTitle;
    export let blogDescription;
    export let delta;
    export let preview;
    export let cover_photo;
    export let changed;
    let htmlContent;
    $: blog ={author:{name:$loginStore.userName},cover_photo:cover_photo,date:new Date().getDate(),title:blogTitle,description:blogDescription,delta:delta}
  const toolbarOptions = [
  [{ 'font': [] }],
  ['bold', 'italic', 'underline', 'strike'], 
  [{ 'size': ['small', false, 'large', 'huge'] }], 
  [{ 'header': 1 }, { 'header': 2 }],              
  ['blockquote', 'code-block'],
  ['link', 'video'],
  [{ 'list': 'ordered'}, { 'list': 'bullet' }, { 'list': 'check' }],
  [{ 'script': 'sub'}, { 'script': 'super' }],      
  [{ 'indent': '-1'}, { 'indent': '+1' }],          
  [{ 'direction': 'rtl' }],                         
  [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
  [{ 'color': [] }, { 'background': [] }],          
  [{ 'align': [] }],
  ['clean']                                         
];
    
    
    
    let f=[]
  
    const toggleMode = (e) => {
      preview = !preview;
      
    };
  
    
    

    
  </script>
  
 
<div class="flex flex-col items-center">
    
    {#if preview}
    <BlogView blog={blog}/>
    {:else}
      <form class="flex flex-col items-center w-full p-4">
        <input type="text" placeholder="Title" bind:value={blogTitle} class="mb-2 p-2 border border-gray-400 rounded" disabled>
        {#if delta}
        <CustomQuil  toolbarOptions={toolbarOptions} f={f} bind:htmlContent={htmlContent} bind:delta={delta} bind:changed />
        {/if}
      </form>
    {/if}
  </div>
  <div class="fixed bottom-4">
    <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" on:click={toggleMode}>
      {preview ? 'Edit ' : 'Preview'}
    </button>
  </div>
  