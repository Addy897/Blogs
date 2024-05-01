

  
  <script>
	export let data;
	export let form;
	import { browser } from "$app/environment";
	import { enhance } from "$app/forms";
	import { goto } from "$app/navigation";
	import ShowLoading from "$lib/components/showLoading.svelte";
  
	let Pages = ["My Blogs", "New Blog",'Profile', "Logout"];
	if (data && data.extra) {
	  Pages = ["My Blogs", "New Blog", "For Review","Profile", "Logout"];
	}
  
	let currentPage = Pages[3];
	$: if(currentPage==="New Blog" && data.user.access_level !== "Read"){
		goto("/new")
	}
	function setoc(p) {
	  currentPage = p;
	}
  
	function getText(content) {
	  if (browser && window) {
		const el = window.document.createElement('html');
		el.innerHTML = content;
		return el.innerText;
	  }
	}
  
	function getColor(status) {
	  if (status === "Draft") {
		return "text-gray-600";
	  } else if (status === "InReview") {
		return "text-yellow-600";
	  } else {
		return "text-green-600";
	  }
	}
	let email=data.user.email || data.user.phone;
	let name=data.user.displayName;
	let pf_photo=data.user.pf_photo;
	let cover_photo=null;
	const handleCoverPhoto=(event)=>{
		cover_photo = event.target.files[0]; 
		if (cover_photo) {
			const reader = new FileReader();
			reader.onloadend = () => {
			pf_photo = reader.result; 
			};
			reader.readAsDataURL(cover_photo); 
		}

	}
	const save = async (e)=>{
		let formData = new FormData();
		formData.append('name',name);
		if(cover_photo){
		formData.append('profile',cover_photo)
		}
		await fetch("/dashboard?/saveProfile",{
            method:"POST",
            body:formData
        }).then(async (response)=>{
        	response = await response.json()
			if(!response.error){
				window.location.reload()
			}
            
            
        });
	}	
  </script>
  
 
  
  <style lang="postcss">
	
	body {
	  @apply font-sans bg-gray-100 text-gray-800;
	}
  
	
	.container {
	  @apply px-4 w-screen flex flex-col md:flex-row;
	}
  
	
	.navigation {
	  @apply flex flex-row flex-wrap md:flex-col items-center  gap-4 border-r border-gray-300 py-4;
	  @apply w-full max-w-xs;
	}
  
	.navigation-button {
	  @apply px-4 py-2 text-lg bg-blue-500 text-white rounded-md transition duration-300 ease-in-out;
	}
  
	.navigation-button:hover {
	  @apply bg-blue-600;
	}
  
	.navigation-button.active {
	  @apply bg-blue-600;
	}
  

	.content {
	  @apply flex flex-col  w-full items-center justify-center gap-8 py-8 md:pl-8;
	  @apply w-full;
	}
  
	.section {
	  @apply grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8;
	  @apply w-full max-w-7xl;
	}
  
	.card {
	  @apply bg-white shadow-md rounded-lg overflow-hidden transition-transform duration-300 ease-in-out;
	}
  
	.card:hover {
	  @apply transform translate-y-[-5px];
	}
  
	.card img {
	  @apply w-full h-auto rounded-t-lg;
	}
  
	.card-content {
	  @apply p-4 h-full;
	}
  
	.card-title {
	  @apply text-lg font-semibold mb-2;
	}
  
	.card-description {
	  @apply text-sm text-gray-600 mb-2;
	}
  
	.card-link {
	  @apply inline-block px-4 py-2 bg-blue-500 text-white rounded-md transition duration-300 ease-in-out;
	}
  
	.card-link:hover {
	  @apply bg-blue-600;
	}
  
	.card-status {
	  @apply text-sm font-semibold;
	}
  
	.status-draft {
	  @apply text-gray-700;
	}
  
	.status-inreview {
	  @apply text-yellow-600;
	}
  
	.status-published {
	  @apply text-green-600;
	}
  
	@media only screen and (max-width: 768px) {
	  .navigation {
		@apply max-w-full rounded-lg shadow-md py-2 px-4;
	  }
  	.navigation-button {
      @apply w-full text-center;
    }
	  .content {
		@apply justify-center;
	  }
	}
  </style>
  
 
  
  
  <div class="container">
	<div class="navigation">
	  {#each Pages as p }
		<button
		  class="navigation-button"
		  on:click={() => setoc(p)}
		>{p}</button>
	  {/each}
	</div>
  
	<div class="content">
	  {#if currentPage === Pages[0]}
		
		  {#await data.getdrafts}
			<ShowLoading/>
		  {:then d}
			{#if d.draft && d.draft !== "Empty"}
				<section class="section">
					{#each Object.entries(d.draft) as [key, draft]}
						<div class="card">
						<img src={draft.cover_photo} alt="">
						<div class="card-content">
							<h5 class="card-title">{draft.title}</h5>
							<p class="card-description  truncate">{draft.description}</p>
							<div class="card-status {getColor(draft.status)}">{draft.status}</div>
							<a href="dashboard/{draft.title}/?for=draft" class="card-link">Read more</a>
						</div>
						</div>
					{/each}
				</section>
			{:else}
			  <section>
			  <div class="card">
				<div class="card-content">
				  <div class="card-title">Empty</div>
				  <div>No drafts available.</div>
				  <button class="card-link" on:click={()=>{window.location.href="/new"}}>Write a blog</button>
				</div>
			  </div>
			</section>
			{/if}
		  {/await}
		
	  {:else if currentPage === 'Logout'}
		<section class="grid grid-cols-1">
		  <form
			action="/login?/logout"
			method="post"
			class="card"
		  >
			<div class="card-content">
			  <div>Are you sure you want to logout?</div>
			  <button type="submit" class="card-link">Log Me Out</button>
			</div>
		  </form>
		</section>
	  {:else if currentPage === 'New Blog' && data.user.access_level === "Read"}
		<section>
		  <div class="card">
			<div class="card-content">
			  <div class="card-title">Access Denied</div>
			  <div>You don't have permission to write blogs.</div>
			</div>
		  </div>
		</section>
	  	
	  {:else if currentPage === "For Review"}
		
		  {#if data.extra}
		  
			{#await data.extra}
			  <ShowLoading/>
			{:then d}
			  {#if d.draft && d.draft !== "Empty"}
			  <section class="section">
				{#each Object.entries(d.draft) as [key, draft]}
				  <div class="card">
					<img src={draft.cover_photo} alt="">
					<div class="card-content">
					  <h5 class="card-title">{draft.title}</h5>
					  <p class="card-description truncate ">{draft.description}</p>
					  <div class="card-status {getColor(draft.status)}">{draft.status}</div>
					  <a href="dashboard/{draft.title}" class="card-link">Read more</a>
					</div>
				  </div>
				{/each}
			</section>
			  {:else}
			  <section>
			  <div class="card">
				<div class="card-content">
				  <div class="card-title">Empty</div>
				  <div>No blogs to review.</div>
				</div>
			  </div>
			</section>
			  {/if}
			{:catch e}
			<section>
				<div class="card">
				  <div class="card-content">
					<div class="card-title">Error</div>
					<div>{e}</div>
				  </div>
				</div>
			  </section>
			{/await}
			{/if}
	  {:else if currentPage === "Profile"}
	 
		<section class="flex flex-col justify-center items-center w-full md:w1/2 lg:w-3/4">
			<form class="flex flex-col w-full gap-2" method="post"
			enctype="multipart/form-data"
			use:enhance
			>
				<div class="flex flex-row justify-center items-center gap-2" >
					<img src="{pf_photo}" class="rounded-full bg-gray-200 w-24 h-24" alt="pf_photo" />
					
						<label for="profile" class="cursor-pointer bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
						  Change Profile Image
						  <input type="file" id="profile" accept="image/*" class="hidden" on:change={handleCoverPhoto}>
						</label>          
					
				</div>	
				<div class="mb-6 pt-3 rounded bg-gray-200">
					<label class="block text-gray-700 text-sm font-bold mb-2 ml-3" for="phone">Name</label>
					<input type="text" id="name" name="name" bind:value={name} class="bg-gray-200 rounded w-full text-gray-700 focus:outline-none border-b-4 border-gray-300 focus:border-purple-600 transition duration-500 px-3 pb-3">
				</div>
				<div class="mb-3 pt-3 rounded bg-gray-200">
					<label class="block text-gray-700 text-sm font-bold mb-2 ml-3" for="email">Email or Phone</label>
					<input type="text" id="email" name="email" bind:value={email} class="bg-gray-200 rounded w-full text-gray-700 focus:outline-none border-b-4 border-gray-300 focus:border-purple-600 transition duration-500 px-3 pb-3" disabled>
				</div>
				
				
				<div class="flex justify-between">
					<a href="/" class="text-sm text-red-600 hover:text-red-700 hover:underline mb-6">Forgot your password?</a>
					{#if form?.serror}
						<div class="text-red-900">{form?.errormsg}</div>
					{/if}
				</div>
				
				<button class="bg-red-500 hover:bg-red-600 text-white font-bold py-2 rounded shadow-lg hover:shadow-xl transition duration-200" type="button" on:click={save}>Save</button>
				
			</form>
		</section>
	
	  {/if}
	</div>
  </div>
  
  


