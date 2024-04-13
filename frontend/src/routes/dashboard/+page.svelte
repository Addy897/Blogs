<script>
	export let data;
	import { browser } from "$app/environment"
	import { goto } from "$app/navigation"
	import ShowLoading from "$lib/components/showLoading.svelte";	
	let Pages=["My Blogs","New Blog","Logout"];
	if(data && data.extra){
		Pages=["My Blogs","New Blog","For Review","Logout"]
	}
	function setoc(p){
		currentPage=p;
	}
	$: if(currentPage==="New Blog" && data.user.access_level!=="Read"){
		goto("/new");
	}
function getText(content){
		
			if( browser && window){
			var el = window.document.createElement( 'html' );
			el.innerHTML = content ;
			return el.innerText
			}
		
		}
	function getColor(st){
		if(st==="Draft"){
			return "text-grey-600";
		}else if(st==="InReview"){
			return "text-yellow-600";
		}
		else{
			return "text-green-600";
		}
	}
	$: currentPage = Pages[0];
			let files;
	function getImg(el){
        let html;
        if(browser){
            html=document.createElement('html')
            html.innerHTML=el
            let imgs = html.getElementsByTagName("img")
            if(imgs.length){
                return String(imgs[0].src)
            }
            else{
                return "https://flowbite.com/docs/images/blog/image-1.jpg"
            }
        }
    }
	$:if(files){
				let total=0;
				for(let i=0;i<files.length;i++){
					total+=files[i].size;
				}
				if(total>2048*files.length){
					console.log("Greater")
					files=[]
				}
	
			}
</script>

<div class="flex md:flex-row w-full flex-col md:pt-5">
	<div
		class="border-black flex md:flex-col justify-center md:justify-start flex-row md:border-r-2 md:w-1/4 w-full gap-4"
	>
		{#each Pages as p }
		<button
		key="{p}"
		class="p-2 text-[4vw] md:text-xl hover:bg-black hover:text-white"
		on:click={(e) => {
			setoc(p)
		}}>{p}</button
	>
		{/each}
		
		
	</div>
	<div class="w-full md:w-3/4">
		{#if currentPage === Pages[0]}
			
			<section class=" grid w-full grid-flow-cols md:grid-flow-cols grid-rows-2  sm:p-20 justify-center items-center gap-5">
				{#await data.getdrafts}
					<ShowLoading/>
				{:then d} 
					{#if d.draft && d.draft!=="Empty"}
						{#each Object.entries(d.draft) as [key,draft]}
				
						<div class="max-w-lg mx-auto">
							<div class="bg-white shadow-md border border-gray-200 rounded-lg max-w-sm mb-5">
								<a href=" ">
									<img class="rounded-t-lg" src={getImg(draft.content)} alt="">
								</a>
								<div class="p-5 h-full">
									<a href=" ">
										<h5 class="text-gray-900 font-bold text-2xl tracking-tight mb-2">{draft.title}</h5>
									</a>
									
									<p class="font-normal text-gray-700 mb-3 truncate text-wrap h-[10vh]">{getText(draft.content)}</p>
									<div class="flex flex-row w-full gap-5 justify-center items-center">
									<a class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-3 py-2 text-center inline-flex items-center" href="dashboard/{draft.title}/?for=draft">
										Read more
										
									</a>
									<p class=" font-bold font-mono text-black">Status: <span class={getColor(draft.status)}>{draft.status}</span></p></div>
								</div>
							</div>
							
						</div>
						{/each}
					{:else}
						<div>Nothing in Draft</div>
				
					{/if}
				{/await}
				
				
			</section>
		{:else if currentPage === 'Logout'}
			<section class="flex w-full flex-col sm:p-20 justify-center items-center gap-5">
				<form
					class="p-24 flex flex-col justify-center border-2 backdrop-blur-xl bg-blue-600 gap-5 text-white text-xl font-mono"
					action="/login?/logout"
					method="post"
				>
					<div>Are you sure you want to logout?</div>
					<button type="submit" class="hover:text-yellow-300">Log Me Out</button>
				</form>
			</section>
		
		
			
		{:else if currentPage === 'New Blog' && data.user.access_level!=="Read"}
			<section class="flex w-full flex-col sm:p-20 justify-center items-center gap-5">
				<div class="font-mono text-4xl">You don't have access to write blogs.Please Contact Admin for more.</div>
			</section>
		{:else if currentPage=== "For Review"}
		<section class=" grid w-full grid-flow-cols md:grid-flow-cols grid-rows-2  sm:p-20 justify-center items-center gap-5">
			{#if data.extra}
				{#await data.extra}
					<ShowLoading/>
				{:then d} 
					{#if d.draft && d.draft!=="Empty"}
						{#each Object.entries(d.draft) as [key,draft]}
				
						<div class="max-w-lg mx-auto">
							<div class="bg-white shadow-md border border-gray-200 rounded-lg max-w-sm mb-5">
								<a href=" ">
									<img class="rounded-t-lg" src={getImg(draft.content)} alt="">
								</a>
								<div class="p-5 h-full">
									<a href=" ">
										<h5 class="text-gray-900 font-bold text-2xl tracking-tight mb-2">{draft.title}</h5>
									</a>
									
									<p class="font-normal text-gray-700 mb-3 truncate text-wrap h-[10vh]">{getText(draft.content)}</p>
									<div class="flex flex-row w-full gap-5 justify-center items-center">
									<a class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-3 py-2 text-center inline-flex items-center" href="dashboard/{draft.title}">
										Read more
										
									</a>
									<p class=" font-bold font-mono text-black">Status: <span class={getColor(draft.status)}>{draft.status}</span></p></div>
								</div>
							</div>
							
						</div>
						{/each}
					{:else}
						<div>Nothing To Review</div>
					{/if}
				{/await}
			{/if}
			
		</section>
		{/if}
	</div>
</div>

