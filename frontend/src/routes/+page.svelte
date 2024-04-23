<script>
    export let data;
    import BlogCard from '$lib/components/blogCard.svelte';
    import ShowLoading from '$lib/components/showLoading.svelte';
	import Faq from '../lib/components/faq.svelte';
    let isSelected;

    $:onSelected=(item)=>{
        isSelected=item;
    }
</script>

{#if data.drafts}
    {#await data.drafts}
        <ShowLoading/>
    {:then drafts}
        {#if drafts && typeof(drafts) === 'object' && drafts.length > 0}
            <section class="container flex flex-col mx-auto py-10 gap-4">
                

                <div class="flex text-2xl  md:text-4xl font-extrabold text-center leading-[72px] items-center justify-center w-full">Explore Some Health Gyan</div>
            <div class="flex flex-col w-full justify-center items-center">
                <select class="rounded-xl px-4 p-2 shadow-md">
                    <option>English</option>
                    <option>Hindi</option>
                    <option>...</option>
                </select>
            </div>
            <div class="flex flex-row justify-center items-center w-full">
            <div class="flex flex-row w-3/4 justify-evenly  py-2 bg-gray-200 rounded-full">
                <button class="{isSelected==="Topic1"?"bg-white":" bg-transparent"} p-1 px-4 rounded-full" on:click={()=>{onSelected("Topic1")}}>Topic 1</button>
                <button class="{isSelected==="Topic2"?"bg-white":" bg-transparent"} p-1 px-4 rounded-full" on:click={()=>{onSelected("Topic2")}} >Topic 2</button>
                <button class="{isSelected==="Topic3"?"bg-white":" bg-transparent"} p-1 px-4 rounded-full" on:click={()=>{onSelected("Topic3")}} >Topic 3</button>
                
            </div></div>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                    {#each drafts as draft}
                        <BlogCard draft={draft} user={data.user} />
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
