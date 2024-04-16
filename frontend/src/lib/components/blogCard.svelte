<script>
    export let draft;
    export let user;
    import { browser } from "$app/environment"


    function getImg(el) {
        let html;
        if (browser) {
            html = document.createElement('html');
            html.innerHTML = el;
            let imgs = html.getElementsByTagName("img");
            if (imgs.length) {
                return String(imgs[0].src);
            } else {
                return "https://flowbite.com/docs/images/blog/image-1.jpg";
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
    }

    function getText(content) {
        if (browser && window) {
            var el = window.document.createElement('html');
            el.innerHTML = content;
            return el.innerText;
        }
    }
    draft.link="/"+draft.title;
</script>
<style lang="postcss">
    a{
        cursor: pointer;
    }
</style>

<div class="bg-white rounded-lg shadow-md overflow-hidden transition-transform duration-500 transform hover:scale-105">
    <a href="{draft.link}">
        <img src={getImg(draft.content)} alt="{draft.title}" class="h-48 w-full object-cover">
    </a>
    <div class="p-4">
        <a href="{draft.link}" class="text-gray-900 font-bold text-xl md:text-2xl lg:text-3xl mb-2 hover:text-blue-700 transition duration-300">{draft.title}</a>
        <p class="text-gray-700 mb-4 line-clamp-3">{getText(draft.content)}</p>
        <div class="flex justify-between items-center">
            <a href="{draft.link}" class="text-blue-700 hover:text-blue-800 font-medium transition duration-300">Read more</a>
            <button
                class="flex items-center text-gray-700 hover:text-red-500 focus:outline-none transition duration-300"
                on:click={(e) => {
                    draft.likes = like(e, draft.likes, draft.refId);
                }}
                aria-label="Like"
            >
                <i class={user && user.likedPosts.includes(draft.refId) ? "fa fa-heart text-red-500" : "fa-regular fa-heart"}></i>
                <span class="ml-1">{draft.likes}</span>
            </button>
        </div>
    </div>
</div>
