<script>
	import { marked } from 'marked';
	import { browser } from '$app/environment';
	import EditBlog from '$lib/components/editBlog.svelte';
	import ShowLoading from '../../../lib/components/showLoading.svelte';
	import BlogView from '../../../lib/components/blogView.svelte';
	import { addToast } from '../../../lib/components/toast/store';
	import Toasts from '../../../lib/components/toast/Toasts.svelte';
	export let data;
	let loading =false;
	let blogTitle;
	let delta;
	let preview = true;
	let blog = null;
	let review = null;
	let changed=false;

	let show=false
  	let message = null;
  	let type = "success";
  	let dismissible = true;
  	let timeout = 0;
    $:if(show){
      addToast({message, type, dismissible, timeout })
      show=false;
    }

	if (data.blog) {
		blog = data.blog;
		blogTitle = blog.title;

		delta=blog.delta
	} else if (data.review) {
		review = data.review;
        blogTitle = review.title;

	}

	
	async function save(e) {
		await fetch('?/setMD', {
			method: 'POST',
			body: JSON.stringify({
				delta: delta,
				ref_id: blog.ref_id
			})
		});
		if(e!=="re"){
			if(browser){
				window.location.reload()
			}
		}
	}
	const pub = async (e) => {
		loading =true;
		if(changed){
        await save("re")
		}
		let resp=await fetch('?/pub', {
			method: 'POST',
			body: JSON.stringify({
				ref_id: blog.ref_id
			})
		});
		let response=await resp.json() ;
		
		 response=JSON.parse(response.data)
		
		if(response!==-1 && response[0].error){
			message=response[response[0].error]||"Unknown Error"
			type="error"
			show=true
		}else{
			message="Published"
			type="success"
			show=true
			blog.status="InReview"
		}
		loading = false
		
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
	
</script>

{#if loading}
	<ShowLoading/>
{:else if blog && typeof blog === 'object'}	
	<Toasts/>		
	<EditBlog bind:delta bind:blogTitle bind:preview cover_photo={blog.cover_photo} blogDescription={blog.description} bind:changed />
	<section class="flex flex-col justify-center items-center w-full gap-5 pt-24">
		{#if preview}
			<form class="flex flex-col items-center w-full p-4">
				<div class="flex justify-between w-full sm:w-auto mb-10">
					{#if changed || blog.status==="Draft"}
						<button
							type="button"
							class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded mt-4 mr-2"
							on:click={pub}>Publish</button
						>
					{/if}
					{#if changed}
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
