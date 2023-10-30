<script>
	import MultiCombo from './multiCombo.svelte';
	import { Textarea, Button, FloatingLabelInput, Heading } from 'flowbite-svelte';
	import { copyText} from 'svelte-copy';

	let stitle = '';
	let title = '';
	let authors = '';
	let bibtex = '';
	let year = 2023;
	let doi = '';
	let json = '';
	export let detailView = [];
	export let freq = {};
	export let addEntryInfo;
	let categories = [];

	detailView.forEach((cate) => {
		if (cate in freq) {
			const temp = { name: cate, value: [] };
			let items = [];
			Object.keys(freq[cate]).forEach((prop) => {
				items.push({ value: prop, label: prop });
			});
			temp['choices'] = items;
			categories.push(temp);
		} else {
			categories.push({ name: cate, value: '' });
		}
	});

	const reset = () => {
		stitle = '';
		title = '';
		authors = '';
		bibtex = '';
		year = 2023;
		doi = '';
		json = '';
		categories.forEach((cate) => {
			if (Array.isArray(cate.value)) {
				cate.value = [];
			} else {
				cate.value = '';
			}
		});
	};

	const generateJson = () => {
		const paper = {
			shortTitle: stitle,
			title: title,
			authors: authors,
			bibtex: bibtex,
			year: year
		};
		categories.forEach((cate) => {
			if (Array.isArray(cate.value)) {
				let lst = [];
				cate.value.forEach((entry) => {
					lst.push(entry.value);
				});
				paper[cate.name] = lst;
			} else {
				paper[cate.name] = cate.value;
			}
		});
		json = JSON.stringify(paper);
	};

	const updateCategory = (res) => {
		categories.forEach((cate) => {
			if (cate.name === res.detail.name) {
				cate.value = res.detail.prop;
				return;
			}
		});
		generateJson();
	};
</script>

<div>
	<Heading tag="h3">Add Entry</Heading>
	{#each addEntryInfo.description as para}
		<p class="mdc-typography--body1">
			{para}
		</p>
	{/each}
	<p class="mdc-typography--body1">
		<strong>Note:</strong> if you would like to update an entry, click on the 3 dots found on the entry
		you wish to update.
	</p>
	<div class="entry-content">
		<div class="entry-row">
			<div class="title-text mdc-typography--body1"><strong>Short Title:</strong></div>
			<div class="text-field">
				<FloatingLabelInput
					size ="small"
					style="outlined"
					id="short_title"
					name="short_title"
					on:change={generateJson}
					bind:value={stitle}
					type="text"
				>
				e.g., ex-Short Title
				</FloatingLabelInput>
			</div>
		</div>
		<div class="entry-row">
			<div class="title-text mdc-typography--body1"><strong>Title:</strong></div>
			<div class="text-field">
				<FloatingLabelInput
					size ="small"
					style="outlined"
					id="title"
					name="title"
					on:change={generateJson}
					bind:value={title}
					type="text"
				>
				e.g., Longest Title of a Paper: The Story
				</FloatingLabelInput>
			</div>
		</div>
		<div class="entry-row">
			<div class="title-text mdc-typography--body1"><strong>Year:</strong></div>
			<div class="text-field">
				<FloatingLabelInput
					size ="small"
					style="outlined"
					id="year"
					name="year"
					on:change={generateJson}
					bind:value={year}
					type="text"
				>
				e.g., 2023
				</FloatingLabelInput>
			</div>
		</div>
		<div class="entry-row">
			<div class="title-text mdc-typography--body1"><strong>Authors:</strong></div>
			<div class="text-field">
				<FloatingLabelInput
					size ="small"
					style="outlined"
					id="authors"
					name="authors"
					on:change={generateJson}
					bind:value={authors}
					type="text"
				>
				e.g., John Doe, Jane Doe, Jack Doe
				</FloatingLabelInput>
			</div>
		</div>
		<div class="entry-row">
			<div class="title-text mdc-typography--body1"><strong>Categories:</strong></div>
			<div class="catagory-field">
				{#each categories as category}
					<div class="title-cate mdc-typography--body1">
						<strong>{category.name}:</strong>
						{#if 'choices' in category}
							<MultiCombo
								items={category.choices}
								name={category.name}
								on:message={updateCategory}
							/>
						{:else}
								<Textarea
									style="width: 100%; height:40px"
									rows="2"
									on:change={generateJson}
									bind:value={category.value}
									placeholder={category.label}
								/>
						{/if}
					</div>
				{/each}
			</div>
		</div>
		<div class="entry-row">
			<div class="title-text mdc-typography--body1"><strong>BibTex:</strong></div>
				<Textarea
					style="width: 100%;"
					rows="2"
					on:change={generateJson}
					bind:value={bibtex}
					placeholder="copy and paste bibtex"
				/>
		</div>
		<div class="entry-row">
			<div class="title-text mdc-typography--body1"><strong>DOI:</strong></div>
			<div class="text-field">
				<FloatingLabelInput
					size ="small"
					style="outlined"
					id="doi"
					name="doi"
					on:change={generateJson}
					bind:value={doi}
					type="text"
				>
				e.g., https://doi.org/0
				</FloatingLabelInput>
			</div>
		</div>
	</div>
	<div style="display:flex; justify-content:space-between; ">
		<div>
			<Button on:click={reset}>
				Reset
			</Button>
		</div>
		<div>

			<Button on:click={() => {copyText(json);}}>
				Copy to Clipboard
			</Button>
			{#if addEntryInfo.github}
				<Button on:click={() => window.open(addEntryInfo.github, '_blank')}>
					Open Issue
				</Button>
			{:else if addEntryInfo.email}
				<Button on:click={() => window.open(addEntryInfo.email, '_blank')}>
					Open email
				</Button>
			{/if}
			
		</div>
	</div>
</div>

<style>
	.title-cate {
		padding: 5px 10px;
	}
	.catagory-field {
		height: 300px;
		width: 100%;
		border: lightgray solid 1px;
		border-radius: 5px;
		overflow-y: scroll;
	}
	.title-text {
		width: 100px;
		text-align: right;
		padding-right: 10px;
	}
	.entry-row {
		display: flex;
		flex-direction: row;
		padding: 10px 10px 10px 0px;
		align-items: center;
		width: 100%;
	}
	.text-field {
		width: 100%;
		height: 40px;
	}
</style>
