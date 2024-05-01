<script>
    export let data;
    import BlogCard from '$lib/components/blogCard.svelte';
    import ShowLoading from '$lib/components/showLoading.svelte';
	import { onMount } from 'svelte';
	import Faq from '../lib/components/faq.svelte';
	import { browser } from '$app/environment';
    let loading=false;
    let loadedTranslate=false;
    
    onMount(() => {
loadTranslate()
setTimeout(function () {
    googleTranslateInit()
}, 3000)
})
function googleTranslateInit() {
    const checkIfGoogleLoaded = setInterval(() => {
        if (google != null && google.translate != null && google.translate.TranslateElement != null) {
            clearInterval(checkIfGoogleLoaded)

            googleTranslateElementInit()
        }
    }, 1000)
}

function googleTranslateElementInit() {
   try{
    new google.translate.TranslateElement({ pageLanguage: 'en' }, 'google_translate_element')
    let doc=document.getElementById("google_translate_element").childNodes[0];
    
    if(doc){
        doc=doc.childNodes
    doc[1].remove()
    doc[1].remove()
    }
}catch(e){
}
}


function loadTranslate() {
    loading = true
    if (browser) {
        const domElement = document.createElement('script')
        domElement.setAttribute('src', '//translate.google.com/translate_a/element.js')
        domElement.onload = () => {
            loadedTranslate = true
        }
        document.body.appendChild(domElement)
    }
}
    let isSelected=null;
    $:onSelected=(item)=>{
        if(isSelected!==item){
        isSelected=item;
        }else{
            isSelected=null;
        }

        
    }

</script>

<svelte:head>
<script type="text/javascript" src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>
</svelte:head>

{#if data.drafts}
    {#await data.drafts}
        <ShowLoading/>
    {:then drafts}
        {#if drafts && typeof(drafts) === 'object' && drafts.length > 0}
            <section class="container flex flex-col mx-auto py-10 gap-4">
                

                <div class="flex text-2xl  md:text-4xl font-extrabold text-center leading-[72px] items-center justify-center w-full">Explore Some Health Gyan</div>
                
                <div class="flex flex-row w-full justify-center items-center">
                    <div id="google_translate_element" class="rounded-xl p-2 shadow-md text-nowrap">
                    
                    </div>
            </div>
            <div class="flex flex-row justify-center items-center w-full">
            <div class="flex flex-row md:w-3/4 justify-evenly  py-2 bg-gray-200 rounded-full">
                <button class="{isSelected==="Topic 1"?"bg-white":" bg-transparent"} p-1 px-4 rounded-full" on:click={()=>{onSelected("Topic 1")}}>Topic 1</button>
                <button class="{isSelected==="Topic 2"?"bg-white":" bg-transparent"} p-1 px-4 rounded-full" on:click={()=>{onSelected("Topic 2")}} >Topic 2</button>
                <button class="{isSelected==="Topic 3"?"bg-white":" bg-transparent"} p-1 px-4 rounded-full" on:click={()=>{onSelected("Topic 3")}} >Topic 3</button>
                
            </div></div>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                    {#each drafts as draft}
                        {#if isSelected && draft.topic===isSelected}
                        <BlogCard draft={draft} user={data.user} />
                        {:else if !isSelected}
                        <BlogCard draft={draft} user={data.user} />
                        {/if}

                    {/each}
                </div>
            </section>
        {:else}
            <section class="container mx-auto flex justify-center items-center h-60">
                <div class="text-lg text-gray-600">No blogs found.</div>
            </section>
        {/if}
    {:catch error}
        <div class="container mx-auto text-red-600">{error}</div>
    {/await}
    <Faq/>
{/if}
