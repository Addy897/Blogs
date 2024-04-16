<script>
	export let data;
	import BlogCard from '$lib/components/blogCard.svelte';
	import ShowLoading from '$lib/components/showLoading.svelte';
	

	
</script>
{#if data.drafts}
		{#await data.drafts}
            <ShowLoading/>
	    {:then drafts}
    
        {#if drafts && typeof(drafts)==='object'}
            <section class="w-full h-full grid place-items-start  sm:grid-cols-2 md:grid-cols-3 gap-5 pt-10">
                {#each drafts as draft}
                    <BlogCard draft={draft} user={data.user}/>
                {/each}
            </section>
        {:else}
            <section
            class="w-full h-[50vh] flex justify-center items-center"
            >
                    <div class="text-[4vw]">No Blogs Found</div>
            </section>
        {/if}
	
    {:catch error}
        <div>{error}</div>
		{/await}
	{/if}

