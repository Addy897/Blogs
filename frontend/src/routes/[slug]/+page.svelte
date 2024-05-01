<script>
	import BlogCard from '$lib/components/blogCard.svelte';
	import BlogView from '$lib/components/blogView.svelte';
	import CommentSection from '$lib/components/commentSection.svelte';
	import ShowLoading from '$lib/components/showLoading.svelte';

	export let data;
</script>

<main class="pt-8 pb-16 lg:pt-16 lg:pb-24 bg-white">
	{#if data.blog}
		{#await data.blog}
			<ShowLoading />
		{:then blog}
			{#if blog}
				<BlogView blog={blog}/>
				<CommentSection comments={blog.comments} uid={data&&data.user?data.user.uid:null}/>

				<div class="flex mx-auto max-w-screen-xl px-2 m-2">

					<div class="mx-auto w-full max-w-3xl">
						<div class="text-3xl font-extrabold text-black">Related Articles</div>
						{#await data.blogs}
							<ShowLoading/>
						{:then drafts} 
						<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-8">
							{#each drafts as draft}
								{#if draft.topic===blog.topic && draft.title!==blog.title}
								<BlogCard draft={draft} user={data.user} />
								{/if}
		
							{/each}
						</div>
						{/await}
						

				</div>
				</div>
			{:else}
				<div class="flex flex-col justify-center items-center w-full h-screen">
					<div>
						<img src="https://i.ibb.co/G9DC8S0/404-2.png" alt="404" />
					</div>
					<div class=" text-3xl font-mono">Not Found</div>
				</div>
			{/if}
		{/await}
	{/if}
</main>
