<script>
	import { Card, Button, Modal } from 'flowbite-svelte';
	// @ts-ignore
	import {  LinkSolid, CopySolid, LockOpenSolid, LockSolid} from 'flowbite-svelte-icons';
	import { Toast } from 'flowbite-svelte';
	import { copyText } from 'svelte-copy';
	import PaperDetail from './paperDetail.svelte';
	// import Multiselect from './multiselect.svelte';
	import {onMount } from 'svelte';
	import {urlParams} from "../store"

	export let paper;
	export let summaryView;
	export let detailView;
	export let meta;
	let open = false;
	let toast = false;

	let params;
	urlParams.subscribe((value) => {
		params = value;
	});
    
	
	onMount(() => {
		if (params.get('paper') == paper.DOI){
			open = true;
			window.history.replaceState(null, null, '?paper=' + paper.DOI);
		} 
	});

	$: if (!open){
		window.history.replaceState(null, null, '/');
	} else {
		window.history.replaceState(null, null, '?paper=' + paper.DOI);
	} 
</script>

<div class="fixed flex justify-center items-center w-full p-5 bottom-2 z-10">
	<Toast dismissable={true} bind:open={toast} >
		<div>Copied bibtex.</div>
	</Toast>
</div>

<Modal title="Paper Details" size='lg' id='modal'  bind:open={open} outsideclose>
	<PaperDetail {paper} {detailView} {meta} />
</Modal>


<Card 
	on:click={() => {open = true; window.history.replaceState(null, null, '?paper=' + paper.DOI);}} 
	class="w-full m-1 relative dark:bg-[#212125] dark:border-slate-800 dark:shadow-xl"
	style="cursor: pointer;"
	padding="none">
	<!-- <img class="card-media-16x9" aspectRatio="16x9" style="background-image: url(/images/{paper.img ? paper.img : "defaultImage.png"}); height: 200px" alt={"Missing figure"} /> -->
	<h5 class="pl-1 pt-1 pr-1 text-md font-bold tracking-tight dark:text-white">{paper.Name}</h5>
	<p class="pl-1 mb-14 font-normal text-gray-400 leading-tight">{paper.Year}</p>
	<div class="menu-loc">
		<div>
		</div>
		<div>
			<Button on:click={(event) => {event.stopPropagation(); window.open('https://doi.org/' + paper.DOI);}} outline={true} size='xs' pill={true} class="!p-2 mb-2 mr-0.5 border-0"><LinkSolid class="w-4 h-4" /></Button>
			{#if paper["Open Access"] == "na"}
			<Button disabled outline={true} size='xs' pill={true} class="!p-2 mb-2  mr-0.5 border-0"><LockSolid class="w-4 h-4" /></Button>
			{:else}
			<Button on:click={(event) => {event.stopPropagation(); window.open(paper['Open Access']);}} outline={true} size='xs' pill={true} class="!p-2 mb-2  mr-0.5 border-0"><LockOpenSolid class="w-4 h-4" /></Button>
			{/if}
		 {#if paper.Bibtex}
				<Button on:click={(event) => {event.stopPropagation(); copyText(paper.Bibtex);toast=true;} } outline={true} size='xs' pill={true} class="!p-2 mb-2  mr-1 border-0"><CopySolid class="w-4 h-4" /></Button>
		 {/if}
		</div>
		</div>
</Card>




<style>
	.menu-loc{
		position: absolute;
		bottom: 0;
		width: 100%;
		display:flex;
		justify-content: space-between;
		align-items: center;
	}
	
</style>
