<script>
	import { copyText } from 'svelte-copy';
	import Multiselect from './multiselect.svelte';
	import { Toast, Button, Heading } from 'flowbite-svelte';
	import {CopySolid} from 'flowbite-svelte-icons';

	export let paper;
	export let detailView;
	export let meta;
	let toast = false;

</script>

<div class="detail-view">
	{#if paper.image}
		<div style={"padding-right:10px"}>
				<img src={paper.image ? paper.image : "/images/defaultImage.png"} 
						width="200" height=200
						alt={paper.altImage ? paper.altImage: "Image from the paper"}
						/>
		</div>
	{/if}
 	<div  class="paper-container">
		<Heading tag="h4" style="margin: 0 20px 0 0 ;">
			{paper.Name} ({paper.Year})
		</Heading>
		<Heading tag="h6" style="margin: 0 0 10px; color: #888;">
			by {paper.Authors}
		</Heading>
		{#each detailView.show as prop}
			{#if meta[prop].type === 'String'}
				<div class="string-select">
					<div><strong>{prop}:&nbsp;</strong></div>
					<div>{paper[prop]}</div>
				</div>
			{:else if meta[prop].type === 'MultiSelect'}
				<div class="multi-select">
					<div><strong>{prop}:&nbsp</strong></div>
					{#if paper[prop].length > 0 && paper[prop][0] !== ''}
						<Multiselect list={paper[prop]} />
					{/if}
				</div>
			{/if}
		{/each}
		<div class="url-link">URL: <a href={paper.DOI}>{paper.DOI}</a></div>
		<div class="paper-icon">
				<Button outline class="border-0" on:click={(e)=>{copyText(paper.Bibtex); toast=true;}}>
					<CopySolid class="w-4 h-4"/>
					<span>&nbsp Bibtex</span>
				</Button>
		</div>
	</div>
</div>
<div class="absolute flex justify-center items-center w-full p-2 bottom-2 z-10">
	<Toast dismissable={true} bind:open={toast} >
		<div>Copied bibtex.</div>
	</Toast>
</div>

<style>
	.url-link {
		padding-top: 5px;
		padding-bottom: 5px;
	}
	.multi-select {
		display: flex;
		align-items: center;
		justify-content: flex-start;
		flex-wrap: wrap;
		align-content: flex-start;
		padding: 2px 0px 2px 0px;
	}
	.string-select {
		height: 40px;
		display: flex;
		align-items: center;
		justify-content: flex-start;
		align-content: flex-start;
	}
	.paper-icon {
		padding-top: 5px;
		margin-left: -10px;
		display: flex;
		align-items: center;
		justify-content: flex-start;
		flex-wrap: wrap;
		align-content: flex-start;
	}
	.paper-container {
		display: flex;
		flex-direction: column;
	}
	.detail-view {
		display: flex;
	}
</style>
