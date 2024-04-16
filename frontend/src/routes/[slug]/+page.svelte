<script>
	import CommentBox from '$lib/components/commentBox.svelte';

	export let data;
	export let form;
	let blog = data.blog;
	let showComments = false;
</script>

<main class="pt-8 pb-16 lg:pt-16 lg:pb-24 bg-white">
	{#if blog && typeof blog === 'object'}
		<div class="flex justify-between px-4 mx-auto max-w-screen-xl">
			<article
				class="mx-auto w-full max-w-2xl format format-sm sm:format-base lg:format-lg format-blue"
			>
				<header class="mb-4 lg:mb-6 not-format">
					<address class="flex items-center mb-6 not-italic">
						<div class="inline-flex items-center mr-3 text-sm text-gray-900 dark:text-white">
							<img class="mr-4 w-16 h-16 rounded-full" src={blog.pfPhoto} alt="Profile_Photo" referrerpolicy="no-referrer" />
							<div>
								<a href=" " rel="author" class="text-xl font-bold text-gray-900">{blog.name}</a>
								<p class="text-base text-gray-500">Premium{blog.level}</p>
								<p class="text-base text-gray-500">
									<time pubdate datetime="2022-02-08" title="February 8th, 2022"
										>{new Date(blog.date).toDateString()}&nbsp{new Date(
											blog.date
										).toLocaleTimeString()}</time
									>
								</p>
							</div>
						</div>
					</address>
					<h1 class="mb-4 text-3xl font-extrabold leading-tight text-gray-900 lg:mb-6 lg:text-4xl">
						{blog.title}
					</h1>
				</header>

				{@html blog.content}
				<button
					on:click={() => {
						showComments = !showComments;
					}}>{showComments ? 'Hide Comments \u2191' : 'Show Comments \u2193'}</button
				>
			</article>
		</div>
		{#if showComments}
			<section class="bg-white  py-8 lg:py-16 antialiased">
				
                <div class="flex justify-between items-center mb-6">
                    <h2 class="text-lg lg:text-2xl font-bold text-gray-900">Discussion ({blog.comments.length})</h2>
                </div>
					<form class="mb-6" action="?/addComment" method="POST">
						<div
							class="py-2 px-4 mb-4 bg-white rounded-lg rounded-t-lg border border-gray-200 "
						>
							<label for="comment" class="sr-only">Your comment</label>
							<textarea
								id="comment"
								rows="6"
								name="comment"
								class="px-0 w-full text-sm text-gray-900 border-0 focus:ring-0 focus:outline-none "
								placeholder="Write a comment..."
								required
							></textarea>
						</div>
						{#if data && data.user}
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
								class="inline-flex items-center py-2.5 px-4 text-xs font-medium text-center text-white bg-blue-700 rounded-lg focus:ring-4 focus:ring-blue-200  hover:bg-blue-800"
							>
								Login To Comment
							</p>
						{/if}
					</form>
				
				{#each blog.comments as cmt}
					{#if data && data.user}
						<CommentBox comments={cmt} uid={data.user.uid} />
					{:else}
						<CommentBox comments={cmt} uid={null} />
					{/if}
				{/each}
			</section>
		{/if}
	{:else}
		<div class="flex flex-col justify-center items-center w-full h-screen">
			<div>
				<img src="https://i.ibb.co/G9DC8S0/404-2.png" alt="404" />
			</div>
			<div class=" text-3xl font-mono">Not Found</div>
		</div>
	{/if}
</main>
