<script>
	import { goto } from '$app/navigation';
	import { browser } from '$app/environment';
	export let comments;
	export let uid;
	let isOpen = false;
	let items = [];
	function manage(command, cid, cuid) {
		if (cuid === null) {
			goto('/login');
		}
            fetch('?/remove', {
				method: 'POST',
				body: JSON.stringify({
					cid: cid,
					cuid: cuid
				})
			});
			if (browser) {
				window.location.reload();
			}
		
		
	}
	if (comments.uid === uid) {
		items = ['Remove'];
	}
</script>

<article
	class="p-6 text-base bg-white border-t border-gray-200 dark:border-gray-700 dark:bg-gray-900"
>
	<footer class="flex justify-between items-center">
		<div class="flex items-center">
			<p class="inline-flex items-center mr-3 text-sm text-gray-900 dark:text-white font-semibold">
				<img
					class="mr-2 w-6 h-6 rounded-full"
					src={comments.pfPhoto}
					alt={comments.name}
				/>{comments.name}
			</p>
			<p class="text-sm text-gray-600 dark:text-gray-400 truncate">
				<time pubdate datetime="2022-06-23" title="June 23rd, 2022">{comments.date}</time>
			</p>
		</div>
		{#if items}
			<div class="flex flex-row justify-start items-start">
				<div class="relative right-[600%]">
					{#if isOpen}
						<div class="absolute left-0 w-48 bg-white rounded-lg shadow-xl">
							{#each items as item (item)}
								<button
									on:click={(e) => {
										manage(item, comments.cid, uid);
									}}
									class="block w-full px-4 py-2 text-gray-800 hover:bg-indigo-500 hover:text-white"
								>
									{item}
								</button>
							{/each}
						</div>
					{/if}
				</div>
				<button
					id="dropdownComment4Button"
					data-dropdown-toggle="dropdownComment4"
					class="inline-flex items-center p-2 text-sm font-medium text-center text-gray-500 dark:text-gray-40 bg-white rounded-lg hover:bg-gray-100 focus:ring-4 focus:outline-none focus:ring-gray-50 dark:bg-gray-900 dark:hover:bg-gray-700 dark:focus:ring-gray-600"
					on:click={() => (isOpen = !isOpen)}
					type="button"
				>
					<svg
						class="w-4 h-4"
						aria-hidden="true"
						xmlns="http://www.w3.org/2000/svg"
						fill="currentColor"
						viewBox="0 0 16 3"
					>
						<path
							d="M2 0a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3Zm6.041 0a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM14 0a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3Z"
						/>
					</svg>
				</button>
			</div>
		{/if}
	</footer>
	<p class="text-gray-500 dark:text-gray-400">{comments.comment}</p>
</article>
