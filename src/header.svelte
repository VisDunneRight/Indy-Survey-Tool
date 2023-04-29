<script>
	import Button, { Label } from '@smui/button';
	import IconButton, { Icon } from '@smui/icon-button';
	import Dialog, { Content } from '@smui/dialog';
	import Menu from '@smui/menu';
	import List, { Item, Separator, Text } from '@smui/list';
	import surveys from './data/other-surveys.json';
	import AddEntry from './components/addEntry.svelte';
	let menu;
	let open = false;
	export let detailView;
	export let topView;
	export let freq;
</script>

<header class="top-bar flexy">
	<div class="survey-info">
		{#if topView.title}
			<h2 class="survey-title">{topView.title}</h2>
		{/if}
		{#if topView.description}
			<p class="survey-subtext">
				{topView.description}
			</p>
		{/if}
		{#if topView.authors}
			<p class="survey-subtext">{topView.authors}</p>
		{/if}
		
	</div>
	<div class="flex-end">
		<Dialog bind:open fullscreen aria-describedby="sheet-content" style="z-index:10">
			<Content id="sheet-content">
				<AddEntry {detailView} {freq} addEntryInfo={topView.addEntry}/>
				<div class="close-button">
					<IconButton on:click={() => (open = false)} class="material-icons">close</IconButton>
				</div>
			</Content>
		</Dialog>
		<Button on:click={() => (open = true)}>
			<Label>Add Entry</Label>
		</Button>
		<div>
			<Button on:click={() => menu.setOpen(true)}>
				<Label>Other Surveys</Label>
			</Button>
			<Menu style={'overflow-x:hidden; padding-right:10px'} bind:this={menu} >
				<List style="width:300px;">
					{#each surveys as survey}
						<li class="survey-list">
							<a class="survey-link" href={survey.url} style="mdc-typography--body1"
								>{survey.name}</a
							>
						</li>
					{/each}
				</List>
			</Menu>
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
		border: 1px solid var(--mdc-theme-text-hint-on-background, rgba(0, 0, 0, 0.1));
		background-color: var(--mdc-theme-background, #212125);
		overflow: inherit;
		display: inline-block;
		align-items: center;
	}

	.flexy {
		display: flex;
		flex-wrap: wrap;
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
