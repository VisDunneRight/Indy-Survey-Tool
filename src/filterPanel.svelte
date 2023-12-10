<script>
  import FilterGroup from "./components/filterGroup.svelte";
  import { Accordion, Badge, Heading } from 'flowbite-svelte';

  import { Button } from "flowbite-svelte";
  import { ReplyOutline } from "flowbite-svelte-icons";
  import { filterBy } from "./store"

  export let freq = [];
  export let filteredFreq = [];
  export let selectTopics = [];
  $:topics = selectTopics
  const clearSelections = () => {
    $filterBy.forEach((prop) => {
      if (prop.values) {
        prop.selected = [];
      } else {
        prop.categories.forEach((option) => {
          option.selected = [];
        });
      }
    });
    $filterBy = $filterBy;
  };

  const removeSelection = (select) => {
    $filterBy.forEach((prop) => {
      if (prop.values) {
        let idx = prop.selected.indexOf(select);
        if (idx > 0) {
          prop.selected = prop.selected.filter((topic) => topic !== select);
        }
      } else {
        prop.categories.forEach((option) => {
          let idx = option.selected.indexOf(select);
          if (idx >= 0) {
            option.selected = option.selected.filter(
              (topic) => topic !== select
            );
          }
        });
      }
    });
    $filterBy = $filterBy;
  };
</script>

<div class="accordion-container">
  <div class="fliter-papers">
    <Heading class="text-2xl">Filters:</Heading>
    <Button
      pill={true}
      outline
      class="!p-1 border-0"
      size="xs"
      on:click={clearSelections}
    >
      <ReplyOutline class="w-6 h-6" />
    </Button>
  </div>
  <div>
		{#each topics as topic }
			<Badge class="p-2 h-5 ml-1" large on:close={(e) => removeSelection(topic)}>{topic}</Badge>
		{/each}
  </div>
  <div style="padding-bottom:60px">
    <Accordion multiple style=" padding-left:3px; padding-right: 5px;">
      {#each $filterBy as prop}
        <!-- <Panel square extend style="padding-bottom: 30px; padding-left:10px"> -->

        {#if prop.values && prop.values.length > 0}
            <FilterGroup {...prop} freqGroup={freq[prop.name]} on:message />
        {:else}
          <Heading tag="h6">{prop.groupName}</Heading>
          {#each prop.categories as option}
              <FilterGroup
                {...option}
                freqGroup={freq[option.name]}
                on:message
              />
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
  .accordion-container {
    padding-bottom: 30px;
  }
</style>
