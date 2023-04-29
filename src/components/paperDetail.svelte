<script>
	import Snackbar, { Actions, Label } from '@smui/snackbar';
	import Button, { Icon } from '@smui/button';
	import Clipboard from 'svelte-clipboard';
	import IconButton from '@smui/icon-button';
	import Multiselect from './multiselect.svelte';

	export let paper;
	export let detailView;
	export let meta;

	let snackbarWithClose;
</script>

<Snackbar bind:this={snackbarWithClose}>
	<Label>Copied bibtex.</Label>
	<Actions>
		<IconButton class="material-icons" title="Dismiss">close</IconButton>
	</Actions>
</Snackbar>
<div class="paper-container">
	<h2 class="mdc-typography--headline6" style="margin: 0 20px 0 0 ;">
		{paper.Name} ({paper.Year})
	</h2>
	<h3 class="mdc-typography--subtitle2" style="margin: 0 0 10px; color: #888;">
		by {paper.Authors}
	</h3>
	{#each detailView.show as prop}
		{#if meta[prop].type === 'String'}
			<div class="string-select">
				<div class="mdc-typography--body1"><strong>{prop}:&nbsp;</strong></div>
				<div class="mdc-typography--body1">{paper[prop]}</div>
			</div>
		{:else if meta[prop].type === 'MultiSelect'}
			<div class="multi-select">
				<div class="mdc-typography--body1"><strong>{prop}:</strong></div>
				{#if paper[prop].length > 0 && paper[prop][0] !== ''}
					<Multiselect list={paper[prop]} />
				{/if}
			</div>
		{/if}
	{/each}
	<div class="url-link">URL: <a href={paper.DOI}>{paper.DOI}</a></div>
	<div class="paper-icon">
		<Clipboard
			text={paper.Bibtex}
			let:copy
			on:copy={() => {
				snackbarWithClose.open();
			}}
		>
			<Button color="secondary" on:click={copy}>
				<Icon class="material-icons">download</Icon>
				<Label>Bibtex</Label>
			</Button>
		</Clipboard>
	</div>
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
</style>
