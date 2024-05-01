<script>
	import { marked } from 'marked';
	import { browser } from '$app/environment';
	import EditBlog from '$lib/components/editBlog.svelte';
	import ShowLoading from '../../../lib/components/showLoading.svelte';
	import BlogView from '../../../lib/components/blogView.svelte';

	export let data;
	let loading =false;
	let markdownTitle = '';
	let markdownContent = null;
	let markdownMode = false;
	let blog = null;
	let review = null;
	$: if (data.blog) {
		blog = data.blog[0];
		markdownTitle = blog.title;
	} else if (data.review) {
		review = data.review;
        markdownTitle = review.title;
	}
	let error=null;
	

	async function allowEdit() {
		let md=null
		await fetch('?/getMD', {
			method: 'POST',
			body: 'NUll'
		}).then(async (response) => {
			let r = await response.json();

			if (r.data) {
				md = JSON.parse(r.data)[0];

				markdownMode = true;
			}
		}).catch((err)=>{
				error=err
		});
        return md
	}
	function save(e) {
		blog.content = marked(markdownContent);
		fetch('?/setMD', {
			method: 'POST',
			body: JSON.stringify({
				md: markdownContent,
				ref_id: blog.ref_id
			})
		});
		if (browser) {
			window.location.reload();
		}
	}
	const pub = (e) => {
        save(e)
		fetch('?/pub', {
			method: 'POST',
			body: JSON.stringify({
				ref_id: blog.ref_id
			})
		});
		Edit = false;
		if (browser) {
			window.location.href = '/dashboard';
		}
	};
	const rpub = (e) => {
		fetch('?/rpub', {
			method: 'POST',
			body: JSON.stringify({
				ref_id: review.ref_id
			})
		});

		if (browser) {
			window.location.href = '/dashboard';
		}
	};
	const  setMarkdown=(md)=>{
		if(!markdownContent){
			markdownContent=md;
		}
	}
</script>

{#if loading}
	<ShowLoading/>
{:else if blog && typeof blog === 'object'}
	{#await allowEdit()}
	<ShowLoading/>
		
	{:then md}
	<div class="hidden">{setMarkdown(md)}</div>
	<EditBlog bind:markdownContent bind:markdownTitle bind:markdownMode cover_photo={blog.cover_photo} markdownDescription={blog.markdownDescription} />
	<section class="flex flex-col justify-center items-center w-full gap-5 pt-24">
		{#if markdownMode}
			<form class="flex flex-col items-center w-full p-4">
				<div class="flex justify-between w-full sm:w-auto mb-10">
					{#if md!==markdownContent || blog.status==="Draft"}
						<button
							type="button"
							class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded mt-4 mr-2"
							on:click={pub}>Publish</button
						>
					{/if}
					{#if md!==markdownContent}
					<button
						type="button"
						class="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded mt-4 ml-2"
						on:click={save}>Save as Draft</button
					>
					{/if}
				</div>
			</form>
		{/if}
	</section>
	{/await}
{:else if review && typeof review === 'object'}
	<section class="flex flex-col justify-center items-center w-full gap-5 py-5">
		<BlogView blog={review}/>

		{#if review.status === 'InReview'}
        <button
        type="button"
        class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded mt-4 mr-2"
        on:click={rpub}>Publish</button
    >
		{/if}
	</section>
	
{:else}
	<section class="flex flex-col justify-center items-center w-full gap-5 pt-24">
		<div class="flex flex-col justify-center items-center w-full h-screen">
			<div>
				<img src="https://i.ibb.co/G9DC8S0/404-2.png" alt="404" />
			</div>
			<div class=" text-3xl font-mono">Not Found</div>
		</div>
	</section>
{/if}
