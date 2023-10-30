<script>
	import { createEventDispatcher } from 'svelte';
	import { onMount } from 'svelte';
	
	import { AccordionItem, Button, Badge, P } from 'flowbite-svelte';
	import { categoryFilters } from '../store';
	import diffence from 'lodash/difference';
	const dispatch = createEventDispatcher();

	export let name;
	export let selected;
	export let values;
	export let freqGroup;
	
	let listVal = [];
	const sShowCount = 10;
	let showCount = 10;
	let listSelected = [''];

	const updateShowCount = (newCount) => {
		const temp = values.sort((a, b) => {
			return freqGroup[b] - freqGroup[a];
		});
		if (newCount > 0) {
			showCount = newCount;
		} else {
			showCount = sShowCount;
		}
		const data = values.slice(0, showCount);
		listVal = data.map((name) => {
			return '(' + freqGroup[name] + ') ' + name;
		});
	};

	listSelected = [...selected];

	onMount(async () => {
		updateShowCount(showCount);
	});
	
	selected = $categoryFilters;
</script>
<AccordionItem>
	<P weight="semibold" slot="header" >
			{name}
			{#if listSelected !== undefined && listSelected.length}
				<span style="color:gray">
					({listSelected.length})
				</span>
			{/if}
	</P>
	<div class="space-y-1 flex-col flex flex-shrink items-start">
		{#each listVal as value}
			<Badge large color="dark" class="cursor-pointer" >{value}</Badge>	
		{/each}
	</div>
	
	<div class="space-y-1" style="padding-top: 3px">
		{#if showCount > sShowCount}
			<Button outline class="border-0" size="xs" on:click={() => updateShowCount(showCount - 10)}>
				see less
			</Button>
		{/if}
		{#if showCount <= values.length}
			<Button outline class="border-0" size="xs" on:click={() => updateShowCount(showCount + 10)}>
				see more
			</Button>
		{/if}
	</div>

</AccordionItem>

<style>

</style>
