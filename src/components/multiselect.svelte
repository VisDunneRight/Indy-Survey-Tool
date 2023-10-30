<script>
	import {Badge} from 'flowbite-svelte'
	export let list = [];
</script>
<div class="flex space-x-1">
{#each list as item }
	<Badge large color="indigo" rounded>{item}</Badge>
{/each}
</div>
<style>
</style>
