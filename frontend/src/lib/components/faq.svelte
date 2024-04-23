<script>
    let answers=["EJY Health is establishing a global platform where doctors, nurses, patients, and the general public can seamlessly interact and benefit from one another's expertise. We're addressing gaps in the Health & wellness industry on a large scale, connecting people from diverse backgrounds and professions to foster collective growth and learning.","","","At EJY health, we believe that access to reliable health information should not be a privilege, but a right, that is accessible with just one click – for free.",""]
    let currentAns=answers[0];
    let active=0;
    const setAns=(inp)=>{
        currentAns=answers[inp];
        active=inp;
    };

</script>

<div class="flex flex-col justify-center items-center p-10 w-full" >
    <div class="text-center">
    <h1 class=" font-extrabold">FAQs</h1>
    <p>Got Quries? We're armed with answers</p>
    </div>
    <div class="w-full lg:w-1/2 shadow-lg flex flex-row flex-wrap md:flex-nowrap p-8 gap-8 rounded-xl">
        <div class="lg:w-1/2  flex flex-col gap-4">
            <button class="w-full border-2 rounded-lg p-4 text-start {active!==0?"":"bg-black text-white"}" on:click={()=>{setAns(0)}}>Why EJY Health?</button>
            <button class="w-full border-2 rounded-lg p-4 text-start {active!==1?"":"bg-black text-white"}" on:click={()=>{setAns(1)}}>Benefits of joining waitlist?</button>
            <button class="w-full border-2 rounded-lg p-4 text-start {active!==2?"":"bg-black text-white"}" on:click={()=>{setAns(2)}}>How do I connect?</button>
            <button class="w-full border-2 rounded-lg p-4 text-start {active!==3?"":"bg-black text-white"}" on:click={()=>{setAns(3)}}>Is it a paid platform?</button>
            <button class="w-full border-2 rounded-lg p-4 text-start {active!==4?"":"bg-black text-white"}" on:click={()=>{setAns(4)}}>How to download the app?</button>
        </div>
        <div class="lg:w-1/2 border-2 rounded-lg p-4">
                {currentAns}
        </div>

    </div>
</div>