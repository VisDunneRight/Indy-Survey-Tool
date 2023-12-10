<script>
  import { Button, P } from "flowbite-svelte";
  import { AccordionItem, Accordion } from "flowbite-svelte";
  import StackGraph from "./viscomponets/stackGraph.svelte";
  import CorrMetric from "./viscomponets/corrMetric.svelte";
  import { filterBy } from "./store";
  export let data;
   let width;
  let choicesDim = [];

  //Get the list of dimension to visualize
  $filterBy.forEach((prop, i) => {
    //This contains two levels of grouping
    if ("groupName" in prop) {
      choicesDim.push({ name: prop.groupName, index: i });
    } else {
      //One level deep
      choicesDim.push({ name: prop.name, index: i });
    }
  });
  $: selectedDimX = choicesDim[0];
  $: selectedDimY = choicesDim[0];
  $: selectedCate = choicesDim[0];
  $: selectedSubCate = choicesDim[0];
  $: subCates = [];
  $: if ("groupName" in $filterBy[selectedCate.index]) {
    subCates = [];
    subCates.push("All");
    $filterBy[selectedCate.index].categories.forEach((cate) => {
      subCates.push(cate.name);
    });
    selectedSubCate = "All";
  } else {
    selectedSubCate = selectedCate;
  }
$:console.log(width)
</script>
<svelte:window bind:innerWidth={width} />
<div class="vis-panel dark:bg-gray-900">
  <Accordion>
    <AccordionItem>
      <span slot="header">Correlations Matrix</span>
      <div class="flexy">
        <div class="flex flex-wrap space-x-1 pb-3 items-center">
          <P style="padding-left:20px">Dimension X-Axis:</P>
          {#each choicesDim as dim}
            <Button
              size="sm"
              outline
              class="p-1 {dim.name === selectedDimX.name
                ? 'dark:bg-gray-400 dark:text-primary-200'
                : 'cursor-pointer'}"
              on:click={() => {
                selectedDimX = dim;
              }}>{dim.name}</Button
            >
          {/each}
        </div>
        <div class="flex flex-wrap space-x-1 items-center">
          <P style="padding-left:20px">Dimension Y-Axis:</P>
          {#each choicesDim as dim}
            <Button
              outline
              size="sm"
              class="p-1 {dim.name === selectedDimY.name
                ? 'dark:bg-gray-400 dark:text-primary-200'
                : 'cursor-pointer'}"
              on:click={() => {
                selectedDimY = dim;
              }}>{dim.name}</Button
            >
          {/each}
        </div>
      </div>

      <!-- Create the visualization -->
      <CorrMetric
        {data}
        selectedDimX={selectedDimX["name"]}
        selectedDimY={selectedDimY.name}
        on:message
      />
    </AccordionItem>
    <AccordionItem>
      <span slot="header">Over the Years</span>

      <div class="flexy">
        <div class="flex flex-wrap space-x-1 pb-3 items-center">
          <P style="padding-left:20px">Categories:</P>
          {#each choicesDim as dim}
            <Button
              size="sm"
              outline
              class="p-1 {dim.name === selectedCate.name
                ? 'dark:bg-gray-400 dark:text-primary-200'
                : 'cursor-pointer'}"
              on:click={() => {
                selectedCate = dim;
              }}>{dim.name}</Button
            >
          {/each}
        </div>
        {#if subCates.length > 0}
          <div class="flex flex-wrap space-x-1 pb-3 items-center">
            <P style="padding-left:20px">Sub-Catagories:</P>
            {#each subCates as subcate}
              <Button
                size="sm"
                outline
                class="p-1 {subcate === selectedSubCate
                  ? 'dark:bg-gray-400 dark:text-primary-200'
                  : 'cursor-pointer'}"
                on:click={() => {
                  selectedSubCate = subcate;
                }}>{subcate}</Button
              >
            {/each}
          </div>
        {/if}

        <StackGraph
          {data}
          selectedCate={selectedSubCate === "All"
            ? selectedCate.name
            : selectedSubCate}
          on:message
        />
      </div>
    </AccordionItem>
  </Accordion>
</div>

<style>
  .vis-panel {
    padding: 10px 5px;
    height: 100%;
    width: 100%;
    position: relative;
  }
</style>
