<script>
import Chip, { Set, Text } from '@smui/chips';
import CorrMetric from './viscomponets/corrMetric.svelte';
export let data
export let filterBy 
let choicesDim = [];

//Get the list of dimension to visualize
filterBy.forEach((prop)=>{
  //This contains two levels of grouping
  if("groupName" in prop){
    choicesDim.push(prop.groupName);
  } else { //One level deep
    choicesDim.push(prop.name)
  }
})
$:selectedDimX = choicesDim[0];
$:selectedDimY = choicesDim[0];
$:console.log(selectedDimX, selectedDimY)
</script>
<div class="vis-panel">
  <Text style="padding-left:40px">Dimension X-Axis:</Text>
  <Set chips={choicesDim} let:chip choice bind:selected={selectedDimX}>
    <Chip {chip}>
      <Text>{chip}</Text>
    </Chip>
  </Set>
  <Text style="padding-left:40px">Dimension Y-Axis:</Text>
  <Set style={"border-bottom: 1px solid gray"} chips={choicesDim} let:chip choice bind:selected={selectedDimY}>
    <Chip {chip}>
      <Text>{chip}</Text>
    </Chip>
  </Set>
  <!-- Create the visualization -->
  <CorrMetric 
    data={data} 
    filterBy={filterBy} 
    selectedDimX={selectedDimX}
    selectedDimY={selectedDimY}
    on:message
    />
</div>
<style>
  .vis-panel{
    padding:10px 5px;
    height: 100%;
    width: 100%;
    position:fixed;
    background-color: var(--mdc-theme-background, #fff);
  }
</style>
