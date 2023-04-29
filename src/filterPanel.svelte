<script>
	import Accordion, { Panel } from '@smui-extra/accordion';
	import FilterGroup from './components/filterGroup.svelte';
	import IconButton, { Icon } from '@smui/icon-button';
	import Chip, { Set, TrailingAction, Text } from '@smui/chips';
	import { createEventDispatcher } from 'svelte';
	const dispatch = createEventDispatcher();
	export let freq = [];
	export let filteredFreq = [];
	export let filterBy = [];
	export let selectTopics = [];
	const clearSelections = () => {
		filterBy.forEach((prop) => {
			if (prop.values){
				prop.selected = [];
			} else {
				prop.categories.forEach((option)=>{
					option.selected = [];
				})
			}
			
		});
		filterBy = filterBy;
		dispatch('message', { text: 'Clear all filter selection.' });
	};

	const removeSelection = (select) =>{
		filterBy.forEach((prop) => {
			if (prop.values){
				let idx = prop.selected.indexOf(select)
				if(idx > 0){
					prop.selected = prop.selected.filter((topic)=> topic !== select)
				}
			} else {
				prop.categories.forEach((option)=>{
					let idx = option.selected.indexOf(select)
					if(idx >= 0){
						option.selected = option.selected.filter((topic)=> topic !== select)
					}
				});
			}
		});
		filterBy = filterBy;
		dispatch('message', { text: 'Remove one topic' });
	}

</script>

<div class="accordion-container">
	<div class="fliter-papers">
		<div class="mdc-typography--headline4">Filters:</div>
		<IconButton class="material-icons" on:click={clearSelections} title="reset Selection"
			>replay</IconButton
		>
	</div>
	<div>
		<Set chips={selectTopics} let:chip input >
			<Chip {chip} >
				<Text>{chip}</Text>
				<TrailingAction icon$class="material-icons" on:click={(e) => removeSelection(chip)}>cancel</TrailingAction>
			</Chip>
		</Set>
	</div>
	<div style="padding-bottom:60px">
		<Accordion multiple style=" padding-left:3px; padding-right: 5px;">
			{#each filterBy as prop}
				<!-- <Panel square extend style="padding-bottom: 30px; padding-left:10px"> -->
					
					{#if prop.values && prop.values.length > 0}
						<Panel square extend>
							<FilterGroup
								{...prop}
								freqGroup={freq[prop.name]}
								on:message
							/>
						</Panel>
					{:else}
						<div class="mdc-typography--headline6 group" >{prop.groupName}</div>
						{#each prop.categories as option}
						<Panel square extend>
							<FilterGroup
								{...option}
								freqGroup={freq[option.name]}
								on:message
							/>
						</Panel>
						{/each}
					{/if}
			{/each}
		</Accordion>
	</div>
</div>

<style>
	.fliter-papers {
		padding: 0px 0px 0px 0px;
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
	.group {
		padding: 10px 0px 10px 0px;
	}
	.accordion-container{
		padding-bottom: 30px;
	}
</style>
