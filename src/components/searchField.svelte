<script>
	import { Input, CloseButton } from 'flowbite-svelte'
	import { SearchOutline } from 'flowbite-svelte-icons'
	import { searchFilter } from '../store';


	function clearSearch() {
		$searchFilter = '';
	}
</script>

<div class="solo-container solo-container-prop">
		<Input bind:value={$searchFilter}  placeholder="Search" size="lg">
			<SearchOutline slot="left"/>
			<CloseButton slot="right" on:click={clearSearch} />
		</Input>
</div>


<style>
	.solo-container {
		padding: 12px 8px;
		margin-right:2px;
	}

	.solo-container-prop {
		display: flex;
		justify-content: center;
		align-items: center;
	}

</style>
