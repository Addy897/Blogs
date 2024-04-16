<script>
    import { browser } from "$app/environment"

    export let draft;
    export let user;
    
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
    const like = (e, l, refId) => {
        if (user) {
            fetch("/?/like", {
                method: "POST",
                body: JSON.stringify({
                    refId: String(refId),
                }),
            });
            if (e.srcElement.className.includes("fa-regular")) {
                e.srcElement.className = "fa fa-heart text-red-500 ";
                l++;
            } else {
                e.srcElement.className = "fa-regular fa-heart";
                if (l > 0) {
                    l--;
                }
            }
            return l;
        } else {
            goto("/login");
            return l;
        }
    };
    function getText(content) {
		if (browser && window) {
			var el = window.document.createElement('html');
			el.innerHTML = content;
			return el.innerText;
		}
	}
</script>


<div class="flex flex-col justify-center w-[90%]">
    <div class="flex flex-col justify-center bg-white shadow-md border border-gray-200 rounded-lg">
        <a class=" flex justify-center" href=" ">
            <img
                class="rounded-t-lg"
                style="height: 200px;"
                src={getImg(draft.content)}
                alt=""
            />
        </a>
        <div class="w-full flex flex-col justify-center items-center p-2 h-full">
            <a href=" ">
                <div class="text-gray-900 font-bold tracking-tight text-[3vh] md:text-[2vw]">{draft.title}</div>
            </a>

            <span class="font-normal text-gray-700 px-6 truncate w-screen md:w-full text-wrap h-[12vh] overflow-hidden ">
                {getText(draft.content)}...
            </span>
            <div class="flex flex-row w-full gap-x-5 justify-center items-center">
                <a
                    class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-3 py-2 text-center inline-flex items-center"
                    href="{draft.title}"
                >
                    Read more
                </a>
                {#if user}
                                <i
                                    class={(user.likedPosts.includes(
                                        draft.refId,
                                    )
                                        ? "fa fa-heart text-red-500 "
                                        : "fa-regular fa-heart")}
                                    on:click={(e) => {
                                        draft.likes = like(
                                            e,
                                            draft.likes,
                                            draft.refId,
                                        );
                            
                                    }}
                                    on:keydown={like}
                                    tabindex="-1"
                                    role="button"
                                    aria-pressed="false"
                                    ><p class="text-black inline">&nbsp{draft.likes}</p></i
                                >
                            {:else}
                                <i
                                    class={"fa-regular fa-heart"}
                                    on:click={(e) => {
                                        draft.likes = like(
                                            e,
                                            draft.likes,
                                            draft.refId,
    
                                        );
                                    }}
                                    on:keydown={like}
                                    tabindex="-1"
                                    role="button"
                                    aria-pressed="false"
                                    >
                            <p class="text-black inline">&nbsp{draft.likes}</p></i
                >
                {/if}
            </div>
        </div>
    </div>
</div>

