<script>
	import Header from './Header.svelte';
	import "../app.css";
	import Footer from './Footer.svelte';
</script>

<div>
	<Header />

	<main>
		<slot />
	</main>

	<Footer/>
	
	
</div>


