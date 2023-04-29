<script>
	import Card, {
		Content,
		PrimaryAction,
		Media,
		MediaContent,
		Actions,
		ActionButtons,
		ActionIcons
	} from '@smui/card';
	import Snackbar, {  Label } from '@smui/snackbar';
	import IconButton from '@smui/icon-button';
	import Button, { Icon } from '@smui/button';
	import List, { Item, Separator, Text } from '@smui/list';
	import Clipboard from 'svelte-clipboard';
	import Menu from '@smui/menu';
	import Dialog from '@smui/dialog';
	import PaperDetail from './paperDetail.svelte';
	

	export let paper;
	export let summaryView;
	export let detailView;
	export let meta;
	export let showImg;
	let menu;
	let open = false;
	let snackbarWithClose;
</script>

<div>
	<Snackbar bind:this={snackbarWithClose}>
		<Label>Copied bibtex.</Label>
		<Actions>
			<IconButton class="material-icons" title="Dismiss">close</IconButton>
		</Actions>
	</Snackbar>
	<Dialog bind:open fullscreen aria-describedby="sheet-content" style="z-index:5">
		<Content id="sheet-content">
			<PaperDetail {paper} {detailView} {meta} />
			<div class="close-button">
				<IconButton on:click={() => (open = false)} class="material-icons">close</IconButton>
			</div>
		</Content>
	</Dialog>
	
	<Card class={showImg === true ? 'card-image' : 'card-text'}>
		<PrimaryAction on:click={() => (open = true)}>
			{#if showImg}
				<Media class="card-media-square" aspectRatio="square" />
			{/if}
			<Content class="mdc-typography--body5">
				<h2 class="mdc-typography--headline6" style="margin: 0;">{paper.Name} ({paper.Year})</h2>
				<h3 class="mdc-typography--subtitle2" style="margin: 0 0 10px; color: #888;">
					by {paper.Authors}
				</h3>
			</Content>
		</PrimaryAction>
		<Actions style="padding-left:15px">
			<!-- Added by: Tarik Crnovrsanin. -->
			<ActionButtons>
				<!-- <Button on:click={() => clicked++}>
					<Label>new Window</Label>
				</Button> -->
			</ActionButtons>
			<ActionIcons>
				<IconButton class="material-icons" on:click={() => menu.setOpen(true)} title="More options"
					>more_vert</IconButton
				>
				<div>
					<Menu bind:this={menu}>
						<List>
							<Clipboard
										text={paper.Bibtex}
										let:copy
										on:copy={() => {
											snackbarWithClose.open();
										}}
									>
								<Item on:SMUI:action={copy}>
								<Icon class="material-icons">download</Icon>
								<Text>BibTex</Text>
								</Item>
							</Clipboard>
							
							<Item on:SMUI:action={() => console.log("work in progress")}>
								<Text>Update Entry</Text>
							</Item>
						</List>
					</Menu>
				</div>
			</ActionIcons>
		</Actions>
	</Card>
	
</div>

<style>
	.close-button {
		position: absolute;
		top: 0px;
		right: 0px;
	}
	* :global(.card-image) {
		width: 400px;
		margin: 4px;
	}
	* :global(.card-text) {
		margin: 10px;
	}

	* :global(.card-media-square) {
		background-image: url(https://place-hold.it/320x320?text=square&fontsize=23);
	}
</style>
