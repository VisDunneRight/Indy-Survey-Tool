<script>
	import { Button, Modal, Heading, Dropdown, DropdownItem, P } from 'flowbite-svelte';
	import { ChevronDownSolid } from 'flowbite-svelte-icons';

	import surveys from './data/other-surveys.json';
	import AddEntry from './components/addEntry.svelte';
	let open = false;
	let menu;
	export let detailView;
	export let topView;
	export let freq;
</script>

<header class="top-bar flexy dark:bg-gray-900">
	<div class="survey-info">
		{#if topView.title}
			<Heading tag="h4">{topView.title}</Heading>
		{/if}
		{#if topView.description}
			<P class="survey-subtext dark:text-gray-400">
				{topView.description}
			</P>
		{/if}
		{#if topView.authors}
			<P class="survey-subtext dark:text-gray-400">{topView.authors}</P>
		{/if}
		
	</div>
	<div class="flex-end">
		<Modal title="Terms of Service" bind:open={open} autoclose size='lg'>
			<AddEntry {detailView} {freq} addEntryInfo={topView.addEntry}/>
		</Modal>
		<Button size="md" class="border-0 p-1" outline on:click={() => (open = true)}>
			Add Entry
		</Button>
		<div>
			<Button size="md" class="border-0 p-1" outline on:click={() =>(menu = true)}>
				Other Surveys
				<ChevronDownSolid class="w-3 h-3 ml-2 text-white dark:text-white" />
			</Button>
			<Dropdown bind:open={menu}>
				{#each surveys as survey}
					<DropdownItem href={survey.url} >
						{survey.name}
					</DropdownItem>
				{/each}
			</Dropdown>
		</div>
	</div>
</header>

<style>
	.close-button {
		position: absolute;
		top: 0px;
		right: 0px;
	}

	header {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		height: 80px;
		z-index: 2;
		
	}
	.top-bar {
		width: 100%;
		overflow: inherit;
		display: inline-block;
		align-items: center;
		border-bottom: 1px solid gray !important;
	}

	.flexy {
		display: flex;
		justify-content: space-between;
	}
	.flex-end {
		display: flex;
		justify-content: flex-end;
	}

	.survey-info {
		margin: -15px 5px;
		gap: 2px;
		flex-direction: column;
		align-content: flex-start;
	}

	.survey-title {
		margin: 2px 0px;
	}
	.survey-subtext {
		margin: 0px 0px;
	}
	.survey-list {
		margin: 6px 10px;
	}
	.survey-link {
		color: var(--mdc-text-button-label-text-color, var(--mdc-theme-primary, #ff3e00));
		text-decoration: none;
	}
</style>
