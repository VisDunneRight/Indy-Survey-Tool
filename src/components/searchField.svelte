<script>
	import { Input } from '@smui/textfield';
	import Paper from '@smui/paper';
	import Fab from '@smui/fab';
	import { Icon } from '@smui/common';
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();
	let searchText = '';

	function clearSearch() {
		searchText = '';
		dispatch('message', { text: '' });
	}
	function onSearch(event) {
		const text = event.target.value;
		if (text.length > 2) dispatch('message', { text: text });
	}
</script>

<div class="solo-container solo-container-prop">
	<Paper class="solo-paper" elevation={6}>
		<Icon class="material-icons">search</Icon>
		<Input bind:value={searchText} on:input={onSearch} placeholder="Search" class="solo-input" />
		<Icon class="material-icons clear" on:click={clearSearch}>clear</Icon>
	</Paper>
</div>

<style>
	.solo-container {
		padding: 12px 8px;
		background-color: var(--mdc-theme-background, #f8f8f8);
		border: 1px solid var(--mdc-theme-text-hint-on-background, rgba(0, 0, 0, 0.1));
		margin-right:2px;
	}

	.solo-container-prop {
		display: flex;
		justify-content: center;
		align-items: center;
	}
	* :global(.clear) {
		cursor: pointer;
	}
	* :global(.material-icons) {
		margin: 0px 0px 0px 0px !important;
	}
	* :global(.solo-paper) {
		display: flex;
		align-items: center;
		flex-grow: 1;
		max-width: 600px;
		margin: 0 12px;
		padding: 0 12px;
		height: 48px;
	}
	* :global(.solo-paper > *) {
		display: inline-block;
		margin: 0 12px;
	}
	* :global(.solo-input) {
		flex-grow: 1;
		color: var(--mdc-theme-on-surface, #000);
	}
	* :global(.solo-input::placeholder) {
		color: var(--mdc-theme-on-surface, #000);
		opacity: 0.6;
	}
	* :global(.solo-fab) {
		flex-shrink: 0;
	}
</style>
