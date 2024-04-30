

  
  <script>
	export let data;
	import { browser } from "$app/environment";
	import { goto } from "$app/navigation";
	import ShowLoading from "$lib/components/showLoading.svelte";
  
	let Pages = ["My Blogs", "New Blog", "Logout"];
	if (data && data.extra) {
	  Pages = ["My Blogs", "New Blog", "For Review", "Logout"];
	}
  
	let currentPage = Pages[0];
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
  
	function getImg(content) {
	  let html;
	  if (browser) {
		html = document.createElement('html');
		html.innerHTML = content;
		const imgs = html.getElementsByTagName("img");
		return imgs.length ? imgs[0].src : "https://flowbite.com/docs/images/blog/image-1.jpg";
	  }
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
						<img src={draft.coverPhoto} alt="">
						<div class="card-content">
							<h5 class="card-title">{draft.title}</h5>
							<p class="card-description">{getText(draft.content)}</p>
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
	  {:else if currentPage === 'New Blog' && data.user.access_level !== "Read"}
	  	<div class="hidden">{goto("/new")}</div>
	  {:else if currentPage === "For Review"}
		
		  {#if data.extra}
		  
			{#await data.extra}
			  <ShowLoading/>
			{:then d}
			  {#if d.draft && d.draft !== "Empty"}
			  <section class="section">
				{#each Object.entries(d.draft) as [key, draft]}
				  <div class="card">
					<img src={getImg(draft.content)} alt="">
					<div class="card-content">
					  <h5 class="card-title">{draft.title}</h5>
					  <p class="card-description">{getText(draft.content)}</p>
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
			{/await}
		  {/if}
		
	  {/if}
	</div>
  </div>
  
  


