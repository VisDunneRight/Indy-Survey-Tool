<script>
  import { Button, P } from "flowbite-svelte";
  import CorrMetric from "./viscomponets/corrMetric.svelte";
  import { filterBy } from "./store"
  export let data;
  let choicesDim = [];

  //Get the list of dimension to visualize
  $filterBy.forEach((prop) => {
    //This contains two levels of grouping
    if ("groupName" in prop) {
      choicesDim.push(prop.groupName);
    } else {
      //One level deep
      choicesDim.push(prop.name);
    }
  });
  $: selectedDimX = choicesDim[0];
  $: selectedDimY = choicesDim[0];
  $: console.log(selectedDimX, selectedDimY);
</script>

<div class="vis-panel dark:bg-gray-900">
  <div class="flexy">
    <div class="flex flex-wrap space-x-1 pb-3 items-center">
      <P style="padding-left:20px">Dimension X-Axis:</P>
      {#each choicesDim as dim}
        <Button
          size="sm"
          outline
          class='p-1 {dim === selectedDimX
            ? "dark:bg-gray-400 dark:text-primary-200"
            : "cursor-pointer"}'
          on:click={() => {
            selectedDimX = dim;
          }}>{dim}</Button
        >
      {/each}
    </div>
    <div class="flex flex-wrap space-x-1 items-center">
      <P style="padding-left:20px">Dimension Y-Axis:</P>
      {#each choicesDim as dim}
        <Button
          outline
          size="sm"
          class='p-1 {dim === selectedDimY
            ? "dark:bg-gray-400 dark:text-primary-200"
            : "cursor-pointer"}'
          on:click={() => {
            selectedDimY = dim;
          }}>{dim}</Button
        >
      {/each}
    </div>
  </div>

  <!-- Create the visualization -->
  <CorrMetric {data} {selectedDimX} {selectedDimY} on:message />
</div>

<style>
  .vis-panel {
    padding: 10px 5px;
    height: 100%;
    width: 100%;
    position: fixed;
  }
</style>
