<script>
	export let data;
	import BlogCard from '$lib/components/blogCard.svelte';
	import ShowLoading from '$lib/components/showLoading.svelte';
	import { onMount } from 'svelte';
	import Faq from '../lib/components/faq.svelte';
	import { browser } from '$app/environment';
	let loading = false;
	let loadedTranslate = false;
	let search = '';
	onMount(() => {
		loadTranslate();
		setTimeout(function () {
			googleTranslateInit();
		}, 3000);
	});
	function googleTranslateInit() {
		const checkIfGoogleLoaded = setInterval(() => {
			if (google != null && google.translate != null && google.translate.TranslateElement != null) {
				clearInterval(checkIfGoogleLoaded);

				googleTranslateElementInit();
			}
		}, 1000);
	}

	function googleTranslateElementInit() {
		try {
			new google.translate.TranslateElement({ pageLanguage: 'en' }, 'google_translate_element');
			let doc = document.getElementById('google_translate_element').childNodes[0];

			if (doc) {
				doc = doc.childNodes;
				doc[1].remove();
				doc[1].remove();
			}
		} catch (e) {}
	}

	function loadTranslate() {
		loading = true;
		if (browser) {
			const domElement = document.createElement('script');
			domElement.setAttribute('src', '//translate.google.com/translate_a/element.js');
			domElement.onload = () => {
				loadedTranslate = true;
			};
			document.body.appendChild(domElement);
		}
	}
	let isSelected = null;
	let tags = ['All', 'Mens', 'Female', 'LGBTQ'];
	let tag = tags[0];
	$: onSelected = (item) => {
		if (isSelected !== item) {
			isSelected = item;
		} else {
			isSelected = null;
		}
	};
	let ldraft;
</script>

<svelte:head>
	<script
		type="text/javascript"
		src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"
	></script>
</svelte:head>

{#if data.drafts}
	<section class="container flex flex-col mx-auto py-10 gap-4">
		<div class="flex flex-row w-full justify-center">
			<div class="flex">
				<input
					type="text"
					placeholder="Search"
					name="keyword"
					bind:value={search}
					class="bg-[#FEFFAC] font-mono text-black border-2 shadow-md rounded-xl px-6 py-1 focus:outline-none text-center w-full"
				/>
			</div>
		</div>

		<div
			class="flex text-2xl md:text-4xl font-extrabold text-center leading-[72px] items-center justify-center w-full"
		>
			Explore Some Health Gyan
		</div>

		<div class="flex flex-row w-full justify-center items-center">
			<div id="google_translate_element" class="rounded-xl p-2 shadow-md text-nowrap"></div>
		</div>
		<div class="flex flex-row justify-center items-center w-full">
			<div class="flex flex-row md:w-3/4 justify-evenly py-2 bg-gray-200 rounded-full">
				<button
					class="{isSelected === 'Topic 1' ? 'bg-white' : ' bg-transparent'} p-1 px-4 rounded-full"
					on:click={() => {
						onSelected('Topic 1');
					}}>Topic 1</button
				>
				<button
					class="{isSelected === 'Topic 2' ? 'bg-white' : ' bg-transparent'} p-1 px-4 rounded-full"
					on:click={() => {
						onSelected('Topic 2');
					}}>Topic 2</button
				>
				<button
					class="{isSelected === 'Topic 3' ? 'bg-white' : ' bg-transparent'} p-1 px-4 rounded-full"
					on:click={() => {
						onSelected('Topic 3');
					}}>Topic 3</button
				>
			</div>
		</div>
		<div class="flex flex-row justify-center">
			<select class="bg-white" id="topic" bind:value={tag} required>
				{#each Object.entries(tags) as [index, value]}
					{#if index === 0}
						<option {value} selected="selected">{value}</option>
					{:else}
						<option {value}>{value}</option>
					{/if}
				{/each}
			</select>
		</div>
		{#await data.drafts}
			{#if browser && localStorage.getItem('draft')}
				<div class="hidden" data={(ldraft = JSON.parse(localStorage.getItem('draft')))}></div>
				{#if ldraft && typeof ldraft === 'object' && ldraft.length > 0}
					<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
						{#each ldraft as draft}
							{#if (search !== '' && search !== null && String(draft.title).includes(search)) || (search === '' && (tag === tags[0] || tag === draft.tag) && (!isSelected || draft.topic === isSelected))}
								<BlogCard {draft} user={data.user} />
							{/if}
						{/each}
					</div>
				{:else}
					<section class="container mx-auto flex justify-center items-center h-60">
						<div class="text-lg text-gray-600">No blogs found.</div>
					</section>
				{/if}
			{:else}
				<ShowLoading />
			{/if}
		{:then drafts}
			<div class="hidden" data={localStorage.setItem('draft', JSON.stringify(drafts))}></div>
			{#if drafts && typeof drafts === 'object' && drafts.length > 0}
				<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
					{#each drafts as draft}
						{#if (search !== '' && search !== null && String(draft.title).includes(search)) || (search === '' && (tag === tags[0] || tag === draft.tag) && (!isSelected || draft.topic === isSelected))}
							<BlogCard {draft} user={data.user} />
						{/if}
					{/each}
				</div>
			{:else}
				<section class="container mx-auto flex justify-center items-center h-60">
					<div class="text-lg text-gray-600">No blogs found.</div>
				</section>
			{/if}
		{:catch error}
			<div class="container mx-auto text-red-600">{error}</div>
		{/await}
	</section>
	<Faq />
{/if}

<style>
	* {
		font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial,
			sans-serif, monospace;
	}
</style>
