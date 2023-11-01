<script>
  import { onMount } from "svelte";
  import { AccordionItem, Button, P } from "flowbite-svelte";
	import { CheckOutline } from "flowbite-svelte-icons";

	import { filterBy } from "../store"

  export let name;
  export let selected;
  export let values;
  export let freqGroup;

  let listVal = [];
  const sShowCount = 10;
  let showCount = 10;

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
      return name;
    });
  };


  onMount(async () => {
    updateShowCount(showCount);
  });
</script>

<AccordionItem>
  <P weight="semibold" slot="header">
    {name}
    {#if selected !== undefined && selected.length}
      <span style="color:gray">
        ({selected.length})
      </span>
    {/if}
  </P>
  <div class="space-y-1 flex-col flex flex-shrink items-start">
    {#each listVal as value}
      <Button
        color="dark"
        size="xs"
        class="border-gray-200 dark:border-gray-700 divide-gray-200 dark:divide-gray-700 font-medium inline-flex items-center justify-center px-2.5 py-0.5 text-sm bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300 rounded"
        on:click={() => {
					if(!selected.includes(value)){
          	selected.push(value);
					} else {
						selected.splice(selected.indexOf(value), 1)
					}
					$filterBy = $filterBy;
        }}>
				{#if selected.includes(value)}
				<CheckOutline class="w-3 h-3 mr-1"/>
				{/if}
				{"(" + freqGroup[value] + ") " + value}
				</Button
      >
    {/each}
  </div>

  <div class="space-y-1" style="padding-top: 3px">
    {#if showCount > sShowCount}
      <Button
        outline
        class="border-0"
        size="xs"
        on:click={() => updateShowCount(showCount - 10)}
      >
        see less
      </Button>
    {/if}
    {#if showCount <= values.length}
      <Button
        outline
        class="border-0"
        size="xs"
        on:click={() => updateShowCount(showCount + 10)}
      >
        see more
      </Button>
    {/if}
  </div>
</AccordionItem>

<style>
</style>
