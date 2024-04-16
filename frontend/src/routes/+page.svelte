<script>
    export let data;
    import BlogCard from '$lib/components/blogCard.svelte';
    import ShowLoading from '$lib/components/showLoading.svelte';
</script>

{#if data.drafts}
    {#await data.drafts}
        <ShowLoading/>
    {:then drafts}
        {#if drafts && typeof(drafts) === 'object' && drafts.length > 0}
            <section class="container mx-auto py-10">
                <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8">
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
{/if}
