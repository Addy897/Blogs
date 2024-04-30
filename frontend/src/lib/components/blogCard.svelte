<script>
    export let draft;
    export let user;
    import { browser } from "$app/environment"
    import check from "$lib/images/check-circle.svg"

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

<div class="bg-white flex flex-col rounded-lg shadow-md overflow-hidden transition-transform duration-500 transform hover:scale-105 gap-2 p-2">
    
    <a href="{draft.link}">
        <img src={draft.coverPhoto} alt="{draft.title}" class="h-48 w-full object-cover rounded-xl">
    </a>
    <div class="flex flex-row gap-4">
    <div class=" rounded-full p-1 px-4  text-center text-green-500 border-2 border-green-500 flex flex-row justify-center items-center gap-2" >
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M13.4167 6.46334C13.4167 6.14117 13.1555 5.88 12.8333 5.88C12.5112 5.88 12.25 6.14117 12.25 6.46334H13.4167ZM12.8333 7L13.4167 7.00034V7H12.8333ZM9.13676 2.20117C9.43103 2.33229 9.77589 2.20003 9.90701 1.90575C10.0381 1.61148 9.90587 1.26662 9.61159 1.1355L9.13676 2.20117ZM13.246 2.74561C13.4737 2.51769 13.4735 2.14834 13.2456 1.92065C13.0177 1.69296 12.6483 1.69314 12.4207 1.92106L13.246 2.74561ZM7.00001 8.1725L6.58753 8.58498C6.69696 8.69441 6.84539 8.75588 7.00015 8.75584C7.15491 8.7558 7.30332 8.69426 7.41269 8.58478L7.00001 8.1725ZM5.66249 6.01002C5.43468 5.78222 5.06534 5.78222 4.83753 6.01002C4.60972 6.23783 4.60972 6.60718 4.83753 6.83498L5.66249 6.01002ZM12.25 6.46334V7H13.4167V6.46334H12.25ZM12.25 6.99967C12.2494 8.13179 11.8828 9.23337 11.2049 10.1401L12.1393 10.8387C12.9678 9.73042 13.4159 8.38404 13.4167 7.00034L12.25 6.99967ZM11.2049 10.1401C10.527 11.0469 9.57423 11.7102 8.48857 12.0312L8.81936 13.15C10.1463 12.7577 11.3108 11.9469 12.1393 10.8387L11.2049 10.1401ZM8.48857 12.0312C7.40291 12.3522 6.24257 12.3137 5.1806 11.9213L4.77629 13.0157C6.07425 13.4952 7.49244 13.5423 8.81936 13.15L8.48857 12.0312ZM5.1806 11.9213C4.11864 11.529 3.21195 10.8039 2.59576 9.85413L1.61704 10.4891C2.37016 11.6499 3.47833 12.5362 4.77629 13.0157L5.1806 11.9213ZM2.59576 9.85413C1.97957 8.90439 1.6869 7.7809 1.76139 6.65123L0.597247 6.57447C0.506204 7.95518 0.863917 9.32833 1.61704 10.4891L2.59576 9.85413ZM1.76139 6.65123C1.83588 5.52157 2.27354 4.44624 3.0091 3.58563L2.12223 2.82762C1.22321 3.87948 0.688291 5.19377 0.597247 6.57447L1.76139 6.65123ZM3.0091 3.58563C3.74467 2.72502 4.73872 2.12524 5.84301 1.87575L5.58589 0.737763C4.23621 1.04271 3.02126 1.77577 2.12223 2.82762L3.0091 3.58563ZM5.84301 1.87575C6.94729 1.62625 8.10265 1.7404 9.13676 2.20117L9.61159 1.1355C8.34768 0.572335 6.93558 0.432819 5.58589 0.737763L5.84301 1.87575ZM12.4207 1.92106L6.58732 7.76023L7.41269 8.58478L13.246 2.74561L12.4207 1.92106ZM7.41249 7.76002L5.66249 6.01002L4.83753 6.83498L6.58753 8.58498L7.41249 7.76002Z" fill="#027A48"/>
        </svg> 
        Verfied
    </div>
    <div class=" rounded-full p-1 px-4 text-center text-nowrap text-gray-500 border-2 border-gray-500 flex flex-row justify-center items-center gap-2" >
        Case-Study
    </div></div>
    <div class="p-4">
        <a href="{draft.link}" class="text-gray-900 font-bold text-xl md:text-2xl lg:text-3xl mb-2 hover:text-blue-700 transition duration-300">{draft.title}</a>
        <p class="text-gray-700 mb-4 line-clamp-3">{getText(draft.content)}</p>
      <div class="flex flex-col">
        <div class="flex flex-row gap-2">
            {draft.views} Impressions
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M13.75 5.625H18.125V10" stroke="#666666" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M1.875 14.375L6.61602 9.63398C6.73209 9.51788 6.8699 9.42578 7.02158 9.36294C7.17326 9.30011 7.33582 9.26777 7.5 9.26777C7.66418 9.26777 7.82674 9.30011 7.97842 9.36294C8.1301 9.42578 8.26791 9.51788 8.38398 9.63398L10.366 11.616C10.4821 11.7321 10.6199 11.8242 10.7716 11.8871C10.9233 11.9499 11.0858 11.9822 11.25 11.9822C11.4142 11.9822 11.5767 11.9499 11.7284 11.8871C11.8801 11.8242 12.0179 11.7321 12.134 11.616L17.5 6.25" stroke="#595959" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        
        </div>
        <div>
            {new Date(draft.date).toDateString()}
        </div>
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
</div>
