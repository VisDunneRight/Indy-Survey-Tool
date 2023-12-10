<script>
  import {Pane, Splitpanes} from 'svelte-splitpanes';
	import {P, Button} from 'flowbite-svelte';
	import {ChevronDoubleLeftOutline, ChevronDoubleRightOutline} from 'flowbite-svelte-icons'
	import PaperCard from './components/paperCard.svelte';
	import FilterPanel from './filterPanel.svelte';
	import SearchField from './components/searchField.svelte';
	import Timeline from './components/timeline.svelte';
  import Header from "./header.svelte";
  import Vis from "./vis.svelte";
	import structure from './data/survey-config.json';
	import dataMeta from './data/survey-data.json';
	import {searchFilter, timeFilters, filterBy} from './store';
  import filter from 'svelte-select/filter';

	let innerHeight = 0;
	let innerWidth = 0;

	let showVis = true;
	let filteredData = [];
	let meta = {};
	let freq = {};
	let filteredFreq = {};
	let selectTopics = [];

	//Restructuring parts of the data passed in
	dataMeta.meta.forEach((prop) => {
		meta[prop.name] = prop;
	});

	$filterBy = structure.filterBy;
	$filterBy.forEach((prop) => {
		if(prop.values){
			if (prop.name in meta && meta[prop.name].type === 'MultiSelect'){
				prop.selected = [];
			}
		} else {
			prop.categories.forEach((option) => {
				if (option.name in meta && meta[option.name].type === 'MultiSelect'){
					option.selected = [];
				}
			})
		}
		 
	});
	addMissingValues();

	function freqCount(prop, arrValue, freqDict) {
		if (prop in meta && meta[prop].type === 'MultiSelect') {
			if (arrValue.length == 1 && arrValue[0] === '') {
				return;
			}
			arrValue.forEach((value) => {
				if (prop in freq) {
					freqDict[prop][value] ? freqDict[prop][value]++ : (freqDict[prop][value] = 1);
				} else {
					freqDict[prop] = {};
					freqDict[prop][value] = 1;
				}
			});
		}
	}

	dataMeta.data.forEach((paper) => {
		Object.entries(paper).forEach(([prop, arrValue]) => {
			freqCount(prop, arrValue, freq);
		});
		paper['selected'] = false;
	});

	function addMissingValues(){
		$filterBy.forEach((group)=>{
			if("groupName" in group){
				group['categories'].forEach((cate)=>{
					if(!("values" in cate)){
						const topics = new Set();
						dataMeta.data.forEach((paper) => {
							if(cate['name'] in paper){
								paper[cate['name']].forEach((word)=>{
									topics.add(word);
								});
							}
						});
						cate['values'] = [...topics]
					}
				})

			} else {
				if(!("values" in group)){
					const topics = new Set();
					dataMeta.data.forEach((paper) => {
						if(group['name'] in paper){
							paper[group['name']].forEach((word)=>{
								topics.add(word);
							});
						}
					});
					group['values'] = [...topics]
				}
			}
		});
	}


	function applyFilters(searchFilter, timeFilters, filterBy) {
		console.log(filterBy);
		//This is a shallow copy, we only interested in the order
		let startingPoint = [...dataMeta.data];

		//Filter by search bar
		if (searchFilter !== '' && searchFilter.length > 2) {
			startingPoint = startingPoint.filter((paper) =>
				paper.Name.toLowerCase().includes(searchFilter.toLowerCase())
			);
		}
		if (timeFilters.start > 0)
			startingPoint = startingPoint.filter(
				(paper) => timeFilters.start <= +paper.Year && +paper.Year <= timeFilters.end
			);

			const re = new RegExp("([0-9]+)")

		//Filter by categories
		filterBy.forEach((group) => {
			if(group.values){
				if (group.selected && group.selected.length > 0) {
					const selected = group.selected.map((sel) => {
						return re.test(sel) ? sel.split(') ')[1]: sel;
					});
					let res = [];
					startingPoint.forEach((paper) => {
						let found = false;
						if (Array.isArray(paper[group.name])) {
							const listCate = paper[group.name];
							found = true;
							selected.forEach((prop) => {
								if (listCate.includes(prop) === false) {
									found = false;
									return;
								}
							});
						} else if (typeof paper[group.name] === 'string') {
							found = selected.includes(paper[group.name]);
						}

						if (found) {
							res.push(paper);
						}
					});
					startingPoint = res;
				}
			} else {
				group.categories.forEach((option)=>{
					if (option.selected && option.selected.length > 0) {
					const selected = option.selected.map((sel) => {
						return re.test(sel) ? sel.split(') ')[1]: sel;
					});
					let res = [];
					startingPoint.forEach((paper) => {
						let found = false;
						if (Array.isArray(paper[option.name])) {
							const listCate = paper[option.name];
							found = true;
							selected.forEach((prop) => {
								if (listCate.includes(prop) === false) {
									found = false;
									return;
								}
							});
						} else if (typeof paper[option.name] === 'string') {
							found = selected.includes(paper[option.name]);
						}
						if (found) {
							res.push(paper);
						}
					});
					startingPoint = res;
				}
				})
			}
		});
		Object.entries(startingPoint).forEach(([prop, arrValue]) => {
			freqCount(prop, arrValue, filteredFreq);
		});
		filteredData = startingPoint.sort((p1, p2) => {
			if(Number(p1.Year) < Number(p2.Year)){
				return 1;
			} else {
				return -1;
			}
		});
		console.log(selectTopics);
		selectTopics = [];
		filterBy.forEach((filter)=>{
			if('groupName' in filter){
				filter.categories.forEach((cate)=>{
					selectTopics = selectTopics.concat(cate.selected);
				})
			} else {
				selectTopics = selectTopics.concat(filter.selected);
			}
		})
		console.log(selectTopics);
		filterBy = [...filterBy];
	}

	function setVis() {
		showVis = !showVis;
	}


	$: applyFilters($searchFilter, $timeFilters, $filterBy)
</script>

<svelte:window bind:innerHeight bind:innerWidth />
<Header detailView={structure.detailView.show} topView={structure.topView} {freq} />
<body>
	<div class="left-panel dark:bg-gray-900">
		<div class="num-papers">
			<P>Number of papers:</P>
			<P>{filteredData.length}/{dataMeta.data.length}</P>
		</div>
		<SearchField/>
		<Timeline {filteredData} data={dataMeta.data} />
		<FilterPanel {freq} {filteredFreq} {selectTopics} />
	</div>
	<div class="main-view">
		<Splitpanes class="default-theme " style="height:{innerHeight - 80}px">
			<Pane>
				<div class="card-container dark:bg-gray-900">
					{#each filteredData as paper}
						<PaperCard
							{paper}
							summaryView={structure.summaryView}
							detailView={structure.detailView}
							{meta}
						/>
					{/each}
				</div>
				{#if !showVis}
					<div class="hide-button">
						<Button outline class="border-0 p-1" on:click={setVis}
							><ChevronDoubleLeftOutline/></Button
						>
					</div>
				{/if}
			</Pane>
			{#if showVis}
				<Pane>
					<div class="show-button">
						<Button outline class="border-0 p-1" on:click={setVis}>
							<ChevronDoubleRightOutline/>
						</Button>
					</div>
					<Vis data={dataMeta.data} />
				</Pane>
			{/if}
		</Splitpanes>
	</div>
</body>

<style>
	body {
		font-family: sans-serif;
		margin-top: 80px;
	}
	.container {
		display: flex; /* or inline-flex */
		align-items: center;
	}
	.left-panel {
		position: fixed;
		width: 300px;
		height: 100%;
		overflow-x: hidden;
		padding-right:8px;
	}
	.main-view {
		padding-left: 300px;
	}
	.card-container {
		display: flex;
		flex-direction: row;
		flex-wrap: wrap;
		column-gap: 10px;
	}
	.show-button {
		position: fixed;
		top: 80px;
		z-index: 1;
	}
	.hide-button {
		position: fixed;
		right: 0px;
		top: 80px;
	}
	.num-papers {
		padding: 15px 15px;
		display: flex;
		justify-content: space-between;
	}
</style>
