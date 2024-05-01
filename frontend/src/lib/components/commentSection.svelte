<script>
	import CommentBox from "./commentBox.svelte";
    export let comments;
    export let uid;
    export let form;
    let showComments = false;

</script>

<section class="bg-white px-2 w-full flex flex-col justify-center items-center py-8 lg:py-16 antialiased">
				<button
            on:click={() => {
                showComments = !showComments;
            }}>{showComments ? 'Hide Comments \u2191' : 'Show Comments \u2193'}</button
        >
				{#if showComments}
					
						<main class="w-full md:w-1/2">
							<div class="flex justify-center items-center mb-6">
								<h2 class="text-lg lg:text-2xl font-bold text-gray-900">
									Discussion ({comments.length})
								</h2>
							</div>
							<form class="mb-6" action="?/addComment" method="POST">
								<div class="py-2 px-4 mb-4 bg-white rounded-lg rounded-t-lg border border-gray-200">
									<label for="comment" class="sr-only">Your comment</label>
									<textarea
										id="comment"
										rows="6"
										name="comment"
										class="px-0 w-full text-sm text-gray-900 border-0 focus:ring-0 focus:outline-none"
										placeholder="Write a comment..."
										required
									></textarea>
								</div>
								{#if uid}
									<button
										type="submit"
										class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-3 py-2 text-center inline-flex items-center"
									>
										Post comment
									</button>
									{#if form?.error}
										<p class="inline text-red-500">{form?.errorMessage}</p>
									{/if}
								{:else}
									<p
										class="inline-flex items-center py-2.5 px-4 text-xs font-medium text-center text-white bg-blue-700 rounded-lg focus:ring-4 focus:ring-blue-200 hover:bg-blue-800"
									>
										Login To Comment
									</p>
								{/if}
							</form>

							{#each comments as cmt}
								{#if uid}
									<CommentBox comments={cmt} uid={uid} />
								{:else}
									<CommentBox comments={cmt} uid={null} />
								{/if}
							{/each}
						</main>
				{/if}
			</section>