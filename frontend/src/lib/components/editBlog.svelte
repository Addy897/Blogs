
<script>
    import {marked} from "marked";
    import { onMount } from "svelte";
	import BlogView from "./blogView.svelte";
	import { loginStore } from "../../stores/loginstore";

   

    
    
    export let markdownTitle;
    export let markdownDescription;
    export let markdownContent;
    export let markdownMode;
    export let cover_photo;
    let htmlContent = "";
    let toolboxVisible = false;
    let helpVisible = false;
    
    
    onMount(() => {
      updateMarkdown();
    });

    
    
    
    
    const updateMarkdown = () => {
      htmlContent = marked(markdownContent);
    };
  
    const insertMarkdown = (markdownSyntax) => {
      const textarea = document.getElementById("markdownTextarea");
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const before = markdownContent.substring(0, start);
      const after = markdownContent.substring(end);
      markdownContent = `${before}${markdownSyntax}${after}`;
      textarea.focus();
      textarea.selectionStart = start + markdownSyntax.length;
      textarea.selectionEnd = start + markdownSyntax.length;
      updateMarkdown();
    };
  
    const toggleMode = (e) => {
      markdownMode = !markdownMode;
      if (markdownMode) {
        updateMarkdown();
      }
    };
  
    const toggleToolbox = (e) => {
      toolboxVisible = !toolboxVisible;
    };
  
    const toggleHelp = (e) => {
      helpVisible = !helpVisible;
    };
    
    $: blog ={author:{name:$loginStore.userName},cover_photo:cover_photo,date:new Date().getDate(),title:markdownTitle,description:markdownDescription,content:htmlContent,topic:topic}

    
  </script>
  
  <style lang="postcss">
    .toolbox {
      @apply transition-transform duration-300 ease-in-out;
      transform: translateY(100%);
    }
  
    
    .help-box {
       
      @apply fixed inset-0 bg-black bg-opacity-50 text-white p-4  rounded shadow-lg transition-opacity duration-300 ease-in-out;
    }
  
    
  </style>
<div class="flex flex-col items-center">
    <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mb-2" on:click={toggleToolbox}>
      {toolboxVisible ? 'Hide Toolbox' : 'Show Toolbox'}
    </button>
    {#if toolboxVisible}
    <div class="toolbox my-4 p-4 w-full fixed bottom-[15vh] left-0 sm:fixed sm:left-[5%]  sm:w-auto  overflow-x-auto">
      <div class="flex">
        
          <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold w-auto text-nowrap py-2 px-4 rounded mr-2" on:click={() => insertMarkdown("# ")}>Heading</button>
          <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold w-auto text-nowrap py-2 px-4 rounded mr-2" on:click={() => insertMarkdown("[Link text](link-url)")} title="Link">Link</button>
          <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold w-auto text-nowrap py-2 px-4 rounded mr-2" on:click={() => insertMarkdown("![Alt text](image-url)")} title="Image">Image</button>
          <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold w-auto text-nowrap py-2 px-4 rounded mr-2" on:click={() => insertMarkdown("**Bold text**")} title="Bold">Bold</button>
          <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold w-auto text-nowrap py-2 px-4 rounded mr-2" on:click={() => insertMarkdown("*Italic text*")} title="Italic">Italic</button>
          <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold w-auto text-nowrap py-2 px-4 rounded mr-2" on:click={() => insertMarkdown("1. ")}>Numbered List</button>
          <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold w-auto text-nowrap py-2 px-4 rounded mr-2" on:click={() => insertMarkdown("- ")}>Bulleted List</button>
          <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold w-auto text-nowrap py-2 px-4 rounded mr-2" on:click={() => insertMarkdown("```\n// Your code here\n```")}>Code Block</button>
        
      </div>
    </div>
    {/if}
    {#if helpVisible}
    <div class="help-box" on:click={toggleHelp} on:keydown={toggleHelp} tabindex="-1" role="button">
      <h2 class="text-lg font-bold mb-2">Markdown Syntax Help</h2>
      <p>Heading: # Your heading text (# is largest ## is 2nd largest and so on)</p>
      <p>Image: ![Alt text](image-url)</p>
      <p>Link: [Link text](link-url)</p>
      <p>Bold: **Your bold text**</p>
      <p>Italic: *Your italic text*</p>
      <p>Numbered List: 1. Item 1</p>
      <p>Bulleted List: - Item 1</p>
      <p>Code Block: ```\n// Your code here\n```</p>
    </div>
    {/if}
    {#if markdownMode}
    <BlogView blog={blog}/>
    <div class="w-1/2"><img class="rounded-xl" src={cover_photo} alt="cover_photo"/></div>
        <h1 class="underline">{markdownTitle}</h1>
      <div class="preview p-4 w-full sm:w-auto">{@html htmlContent}</div>
    {:else}
      <form class="flex flex-col items-center w-full p-4">
        <input type="text" placeholder="Title" bind:value={markdownTitle} class="mb-2 p-2 border border-gray-400 rounded" disabled>
        <textarea bind:value={markdownContent} name="content" id="markdownTextarea" class="m-2 px-2 lg:p-4 md:p-4 sm:p-3 border-solid border-2 border-black min-w-full h-[50vh] rounded-2xl shadow-md"></textarea>
        
      </form>
    {/if}
  </div>
  <div class="fixed bottom-4">
    <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" on:click={toggleMode}>
      {markdownMode ? 'Edit ' : 'Preview'}
    </button>
  </div>
  <div class="fixed bottom-4 right-4">
    <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" on:click={toggleHelp}>
      {helpVisible ? 'Hide Help' : 'Show Help'}
    </button>
  </div>