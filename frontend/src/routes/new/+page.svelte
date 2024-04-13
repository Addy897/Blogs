<script>
    import {marked} from "marked";
    import { onMount } from "svelte";
    import { browser } from '$app/environment';

    let markdownTitle = "";
    let markdownContent = "";
    let htmlContent = "";
    let markdownMode = false;
    let toolboxVisible = false;
    let helpVisible = false;
    let images = [];
    let f = [];
    let error=null;
    onMount(() => {
      updateMarkdown();
    });
  
    const updateMarkdown = () => {
        const replacedContent = markdownContent.replace(/\!\[Image(\d+)\]/g, (match, index) => {
        const imageIndex = parseInt(index) - 1;
        if (images[imageIndex]) {
          return `![Image${index}](${images[imageIndex]})`;
        }
        return match; // If the image with the specified index doesn't exist, return the original syntax
      });
      htmlContent = marked(replacedContent);
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
    const addImage = (url, size) => {
        
        if (size <= (2 * 1024 * 1024) && images.length < 3) { 
            
          images = [...images, url];
          updateMarkdown();
        } else {
          alert("Image size exceeds 2 MB limit or maximum number of images reached.");
        }
    };
    const removeImage = (index) => {
      images = images.filter((_, i) => i !== index);
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
    const handleImageUpload = (event) => {
        const file = event.target.files[0];
        const fileSize = file.size;
        const reader = new FileReader();
        if(fileSize <= (2 * 1024 * 1024)){
            f = [...f, file];
        }
        reader.onload = (e) => {
        const imageUrl = e.target.result;
        addImage(imageUrl, fileSize);
        };
        
        reader.readAsDataURL(file);
  };
    const handlePublish = async (event) => {
      event.preventDefault();
      const formData=new FormData();
      formData.append("length",f.length);
      for(let i=0;i<f.length;i++){
        formData.append(String((i+1)),f[i]);
      }
      formData.append("title",markdownTitle)
      formData.append("content",markdownContent)
        await fetch("/dashboard?/publish",{
            method:"POST",
            body:formData
        }).then(async (response)=>{
            let resp=await response.json()
            let d=JSON.parse(resp.data)
           
            let index=d[0].error
            if(d[index]){
                error=d[index+1];
                return
            }else{
                error=null
            }
            
        });
        if(browser && !error){
            window.location.href="/";
        }
        
    }
    const handleDraft = async (event) => {
      event.preventDefault();
      const formData=new FormData();
      formData.append("length",f.length);
      for(let i=0;i<f.length;i++){
        formData.append(String((i+1)),f[i]);
      }
      formData.append("title",markdownTitle)
      formData.append("content",markdownContent)
        await fetch("/dashboard?/draft",{
            method:"POST",
            body:formData
        }).then(async (response)=>{
            let resp=await response.json()
            let d=JSON.parse(resp.data)
           
            let index=d[0].error
            if(d[index]){
                error=d[index+1];
                return
            }else{
                error=null
            }
            
        });
        if(browser && !error){
            window.location.href="/";
        }
        
    }
  </script>
  
  <style>
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
          <!-- Add more buttons for other Markdown syntax -->
        
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
        <h1 class="underline">{markdownTitle}</h1>
      <div class="preview p-4 w-full sm:w-auto">{@html htmlContent}</div>
    {:else}
      <form class="flex flex-col items-center w-full p-4" method="post">
        <input type="text" placeholder="Title" bind:value={markdownTitle} class="mb-2 p-2 border border-gray-400 rounded">
        <textarea bind:value={markdownContent} name="content" id="markdownTextarea" class="m-2 px-2 lg:p-4 md:p-4 sm:p-3 border-solid border-2 border-black min-w-full h-[50vh] rounded-2xl shadow-md"></textarea>
        <div class="flex items-center space-x-2">
            {#each images as image, index (image)}
              <div class="flex items-center space-x-2" key={index}>
                <img src={image} alt=" " class="h-10 w-10 rounded-full">
                <button type="button" class="bg-red-500 hover:bg-red-700 text-white font-bold py-1 px-2 rounded" on:click={() => removeImage(index)}>Remove</button>
              </div>
            {/each}
            {#if images.length < 3}
              <label for="imageInput" class="cursor-pointer bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                Add Image
                <input type="file" id="imageInput" accept="image/*" class="hidden" on:change={handleImageUpload}>
              </label>
            {/if}
          </div>
        <div class="flex justify-between w-full sm:w-auto mb-10">
          <button type="submit" class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded mt-4 mr-2" on:click={handlePublish}>Publish</button>
          <button type="button" class="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded mt-4 ml-2" on:click={handleDraft}>Save as Draft</button>
          
        </div>
        {#if error}
          <p class="text-red-500">{error}</p>
          {/if}
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
  