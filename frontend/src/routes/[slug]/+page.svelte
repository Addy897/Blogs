<script>
	import CommentBox from "$lib/components/commentBox.svelte";

	export let data;
	export let form;
    let blog=data.blog
    let showComments=false;
</script>


<section class="flex flex-col justify-center items-center w-full gap-5 pt-24">
    {#if blog && typeof(blog)==='object'}

        <h1>{blog.title}</h1>
        <div class="flex flex-col justify-center items-center"><p class=" text-lg  font-bold flex flex-row gap-2 items-center"><span class="font-light">By:&nbsp</span>{blog.name}<img
            class="rounded-full h-7"
            src={blog.pfPhoto}
            alt=""
            referrerpolicy="no-referrer"
        /><span class="inline-flex font-normal text-sm">Premium{blog.level}</span></p><p>Published On:&nbsp{new Date(blog.date).toUTCString()}</p></div>
        {@html blog.content}
        <button on:click={()=>{showComments=!showComments}}>{showComments?"Hide Comments \u2191":"Show Comments \u2193"}</button>
        {#if showComments}
            <section class="bg-white dark:bg-gray-900 py-8 lg:py-16 antialiased">
  <div class="flex flex-col w-[90vw] px-5">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-lg lg:text-2xl font-bold text-gray-900 dark:text-white">Discussion ({blog.comments.length})</h2>
    </div>
    <form class="mb-6" action="?/addComment" method="POST">
        <div class="py-2 px-4 mb-4 bg-white rounded-lg rounded-t-lg border border-gray-200 dark:bg-gray-800 dark:border-gray-700">
            <label for="comment" class="sr-only">Your comment</label>
            <textarea id="comment" rows="6" name="comment"
                class="px-0 w-full text-sm text-gray-900 border-0 focus:ring-0 focus:outline-none dark:text-white dark:placeholder-gray-400 dark:bg-gray-800"
                placeholder="Write a comment..." required></textarea>
        </div>
        {#if data && data.user}
        <button type="submit"
            class="inline-flex items-center py-2.5 px-4 text-xs font-medium text-center text-white bg-primary-700 rounded-lg focus:ring-4 focus:ring-primary-200 dark:focus:ring-primary-900 hover:bg-primary-800">
            Post comment
        </button>
        {#if form?.error}
        <p class="inline text-red-500">{form?.errorMessage}</p>
        {/if}
        {:else}
        <p class="inline-flex items-center py-2.5 px-4 text-xs font-medium text-center text-white bg-primary-700 rounded-lg focus:ring-4 focus:ring-primary-200 dark:focus:ring-primary-900 hover:bg-primary-800"
            >Login To Comment</p>
        {/if}
    </form>
  </div>
  {#each blog.comments as cmt }
  {#if data && data.user}
  <CommentBox comments={cmt} uid={data.user.uid}/>
  {:else}
  <CommentBox comments={cmt} uid={null}/>

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
</section>
