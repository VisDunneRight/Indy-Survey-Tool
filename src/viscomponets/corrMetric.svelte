<script>
  import { blend_colors, defaultColors } from './util';
  import * as d3 from 'd3';
  import Slider from '@smui/slider';
  import ZoomSvg from '@svelte-parts/zoom/svg'
  import { createEventDispatcher } from 'svelte';
	const dispatch = createEventDispatcher();

  const config = {boxSize:25, minAmount:10, gap: 6,
                 lineThickiness:5, strokeArray: 8};
  const padding = { top:200, right:150, bottom: 200, left:250};

  export let data;
  export let filterBy;
  export let selectedDimX;
  export let selectedDimY;
  let maxColorValue = 10;
  let maxPaperValue = 100;
  let minCutoff = 0;

  let horBarId = -1;
  let verBarId = -1;
  //finds the correct metadata based on selected Dim
  function getDimInfo(selectedDim, filterBy){
    let selectProp = undefined;
    let ind = -1;
    filterBy.forEach((prop, i)=>{
      if('groupName' in prop){
        if(prop['groupName'] === selectedDim){
          selectProp = prop;
          ind = i;
          return;
        }
      } else {
        if(prop['name'] === selectedDim){
          selectProp = prop;
          ind = i;
          return
        }
      }
    })
    if(selectProp !== undefined){
      if(selectProp && selectProp.color === undefined){
      const colorInd = ind < defaultColors.length ? ind : ind % defaultColors.length;
      selectProp.color = defaultColors[colorInd]
    }
      return selectProp;
    }
    //In the case the
    filterBy.forEach((prop, i)=>{
      if('groupName' in prop){
        prop.categories.forEach((cate)=>{
          if(cate['name'] === selectedDim){
            selectProp = cate;
            ind = i;
            return
          }
        });
      }
    });
    if(selectProp && selectProp.color === undefined){
      const colorInd = ind < defaultColors.length ? ind : ind % defaultColors.length;
      selectProp.color = defaultColors[colorInd]
    }
    return selectProp;
  }
  $:dimX = getDimInfo(selectedDimX, filterBy);
  $:dimY = getDimInfo(selectedDimY, filterBy);
  let visInit = {xAxis:[], yAxis:[], matrix:[], 
                 cateSepX:[], cateSepY:[],
                 paperCountX:[], paperCountY:[]}
  $:visData = visInit;
  function getValues(cate, color){
    let values = [];
    cate.values.forEach((value)=>{
      values.push({cateName: cate.name, 
                   value: value, color: color, 
                   selected: cate.selected.includes(value)})
    })
    return values;
  }

  function countFreq(xCateories, yCateories, data, visData){
    xCateories.forEach((xCate, i)=> {
      visData.matrix.push(new Array(yCateories.length).fill(0))
      if (typeof xCate === 'string')
        return
      yCateories.forEach((yCate, j)=> {
        if (typeof yCate === 'string')
          return
        data.forEach((paper)=>{
          if(paper[xCate.cateName].includes(xCate.value) &&
              paper[yCate.cateName].includes(yCate.value)){
                visData.matrix[i][j] += 1
              }
        })
      })
    })

    visData.paperCountX = new Array(xCateories.length).fill(0)
    visData.paperCountY = new Array(yCateories.length).fill(0)
    xCateories.forEach((xCate, i)=> {
      if (typeof xCate === 'string')
        return
      data.forEach((paper)=>{
        if(paper[xCate.cateName].includes(xCate.value)){
              visData.paperCountX[i] += 1
            }
      })
    });
    yCateories.forEach((yCate, j)=> {
      if (typeof yCate === 'string')
        return
      data.forEach((paper)=>{
        if(paper[yCate.cateName].includes(yCate.value)){
          visData.paperCountY[j] += 1
        }
      })
    });

    visData.xAxis = xCateories;
    visData.yAxis = yCateories;
  }

  //Generate the needed data
  $: if(dimX && dimY){
    visData.cateSepX = [];
    visData.cateSepY = [];
    visData.matrix = [];
    visData.paperCountX = []; 
    visData.paperCountY = [];
    visData.xAxis = [];
    visData.yAxis = [];
    if("groupName" in dimX){
      let xValues = [];
      let yValues = [];
      dimX.categories.forEach((cateX)=>{
        let line = [xValues.length - 1, 0];
        xValues = xValues.concat(getValues(cateX, dimX.color))
        line[1] = xValues.length - 1;
        //Add spacer
        xValues.push("---")
        visData.cateSepX.push({groupName: cateX.name, line:line})
      })
      
      dimY.categories.forEach((cateY)=>{  
        let line = [yValues.length - 1, 0];
        yValues = yValues.concat(getValues(cateY, dimY.color))
        line[1] = yValues.length - 1;
        //Add Spacer
        yValues.push("---")
        visData.cateSepY.push({groupName: cateY.name, line:line})
      })
      countFreq(xValues, yValues, data, visData);
      visData = visData;
      visData.matrix = visData.matrix;
    } else{
      countFreq(getValues(dimX, dimX.color),
        getValues(dimY, dimY.color), data, visData);

      visData.cateSepX.push({groupName: dimX.name, line:[-1, dimX.values.length - 1]})
      visData.cateSepY.push({groupName: dimY.name, line:[-1, dimY.values.length - 1]})
      visData = visData;
    }
  }
  //Helper functions
  function columnSpacing(i){
    return padding.left
          + (i) * (config.boxSize + config.gap);
  }
  function modelRow(j){
    return (j) * (config.boxSize + config.gap) + padding.top;
  }
  function hightlight(event, hor, ver){
      horBarId = hor;
      verBarId = ver;
      event.preventDefault();
  }
  function addSelection(selectedCate){
    filterBy.forEach((filter)=>{
      if('groupName' in filter){
        filter.categories.forEach((cate)=>{
          if(cate.name === selectedCate.cateName){
            if(!cate.selected.includes(selectedCate.value))
              cate.selected.push(selectedCate.value);
            return;
          }
        })
      } else {
        if(filter.name === selectedCate.cateName){
          if(!filter.selected.includes(selectedCate.value))
            filter.selected.push(selectedCate.value);
          return;
        }
      }
    })
  }
  function mouseClick(selectedCate){
    addSelection(selectedCate);
    dispatch('message', { text: "updating" });
  }
  function crossClick(selectedCate1, selectedCate2){
    addSelection(selectedCate1);
    addSelection(selectedCate2);
    dispatch('message', { text: "updating" });
  }
  function getLineColor(axis, pac){
    const midPoint = Math.floor((pac.line[1] + pac.line[0])/2);
    return axis[midPoint] !== undefined ? axis[midPoint].color: '#000';
  }

  function getMaxCount(vData){
    if(vData === undefined){
      return 100;
    }
    return Math.max(...vData.paperCountX, ...vData.paperCountY);
  }
  
  $:maxPaperValue = getMaxCount(visData);
  $:maxColorValue = maxPaperValue
  
// width="{columnSpacing(visData.xAxis.length + 2) + padding.right}"
// height="{modelRow(visData.yAxis.length + 2) + padding.bottom}"
let w = 100, h = 100;
</script>

<div class="corr-container" bind:clientWidth={w} bind:clientHeight={h}>
  <div class="corr-menu">
    <span style={"padding-left:26px"}>Max Color Value: {maxColorValue}</span>
    <div>
      <Slider
      bind:value={maxColorValue}
      min={0}
      max={maxPaperValue}
      step={1}
      discrete
      input$aria-label="Discrete slider"
    />
    
  </div>
</div>
  <ZoomSvg 
      viewBox="0 0 
        {w}
        {h}"
      class="svg-container" >
    <g class="x-axis">
      {#each visData.xAxis as cate, i}
        {#if typeof cate !== 'string'}
          <text
            on:mousedown={(e)=> mouseClick(cate)}
            on:mouseover={(e) => hightlight(e,-1,i)}
            on:focus={(e) => hightlight(e,-1,i)}
            on:mouseout={(e) => hightlight(e,-1,-1)}
            on:blur={(e) => hightlight(e,-1,-1)}
            text-anchor="end"
            transform="translate({columnSpacing(i)}, {modelRow(-1) - config.boxSize/2}) rotate(45)"
            alignment-baseline="middle"
            font-weight = "{cate.selected ? "bold" : "normal"}"
            class="model-text">{cate.value}</text>   
        {:else if i != visData.xAxis.length - 1}
          <line
            x1="{columnSpacing(i)}"
            y1="{modelRow(-1)}"
            x2="{columnSpacing(i)}"
            y2="{modelRow(visData.yAxis.length-1)}"
            stroke-width="{config.lineThickiness}"
            stroke-dasharray="{config.strokeArray}"
            class="dash-line"
          >
          </line>
        {/if}
      {/each}      
      {#each visData.cateSepX as pac}
        <line
          x1="{columnSpacing(pac.line[0]) + config.boxSize/2 + config.gap}"
          y1="{modelRow(-1)}"
          x2="{columnSpacing(pac.line[1]) + config.boxSize/2}"
          y2="{modelRow(-1)}"
          stroke-width="{config.lineThickiness}"
          class="topic-line"
          stroke="{getLineColor(visData.xAxis, pac)}"
        >
        </line>
        <line
          x1="{columnSpacing(pac.line[0]) + config.boxSize/2 + config.gap}"
          y1="{modelRow(visData.yAxis.length)}"
          x2="{columnSpacing(pac.line[1]) + config.boxSize/2}"
          y2="{modelRow(visData.yAxis.length)}"
          stroke-width="{config.lineThickiness}"
          class="end-line"
        >
        </line>
        {/each}
    </g>
    <g class="y-axis">
      {#each visData.yAxis as cate, j}
        {#if typeof cate !== 'string'}
          <g class="y-label">
            <text
                on:mousedown={(e)=> mouseClick(cate)}
                on:mouseover={(e) => hightlight(e,j,-1)}
                on:focus={(e) => hightlight(e,j,-1)}
                on:mouseout={(e) => hightlight(e,-1,-1)}
                on:blur={(e) => hightlight(e,-1,-1)}
                x="{columnSpacing(-1) - config.boxSize/2}"
                y="{modelRow(j)}"
                text-anchor="end"
                alignment-baseline="middle"
                font-weight = "{cate.selected ? "bold" : "normal"}"
                class="model-text">{cate.value}</text>
          </g>
        {:else if j != visData.yAxis.length - 1}
          <line
            x1="{columnSpacing(-1)}"
            y1="{modelRow(j)}"
            x2="{columnSpacing(visData.xAxis.length - 1)}"
            y2="{modelRow(j)}"
            stroke-width="{config.lineThickiness}"
            stroke-dasharray="{config.strokeArray}"
            class="dash-line"
          >
          </line>
        {/if}
      {/each}
      
      {#each visData.cateSepY as pac}  
        <line
          x1="{columnSpacing(-1)}"
          y1="{modelRow(pac.line[0]) + config.boxSize/2 + config.gap}"
          x2="{columnSpacing(-1)}"
          y2="{modelRow(pac.line[1]) + config.boxSize/2}"
          stroke-width="{config.lineThickiness}"
          class="topic-line"
          stroke="{getLineColor(visData.yAxis, pac)}"
        >
        </line>
        <line
          x1="{columnSpacing(visData.xAxis.length)}"
          y1="{modelRow(pac.line[0]) + config.boxSize/2 + config.gap}"
          x2="{columnSpacing(visData.xAxis.length)}"
          y2="{modelRow(pac.line[1]) + config.boxSize/2}"
          stroke-width="{config.lineThickiness}"
          class="end-line"
        >
        </line>
      {/each}
    </g>
    <g class="matrix">
      {#each visData.matrix as row, i}
        {#if typeof visData.xAxis[i] !== 'string'}
          {#each row as col, j}
            {#if typeof visData.yAxis[j] !== 'string'}
            <g
              on:mousedown={(e)=> crossClick(visData.xAxis[i], visData.yAxis[j])}
              on:mouseover={(e) => hightlight(e,j,i)}
              on:focus={(e) => hightlight(e,j,i)}
              on:mouseout= {(e) => hightlight(e, -1, -1)}
              on:blur={(e) => hightlight(e, -1, -1)}
              >
              <rect
                x="{columnSpacing(i) - config.boxSize/2}"
                y="{modelRow(j) - config.boxSize/2}"
                width="{config.boxSize}"
                height="{config.boxSize}"
                fill="{blend_colors(visData.xAxis[i].color, visData.yAxis[j].color, 0.7)}"
                opacity="{col === 0 ? 0 : col/maxColorValue}"
              ></rect>
              <text
              on:mouseover={(e) => hightlight(e,j,i)}
              on:focus={(e) => hightlight(e,j,i)}
                x="{columnSpacing(i)}"
                y="{modelRow(j)}"
                text-anchor="middle"
                dominant-baseline="central"
                class="cross-count"
                fill={col/maxColorValue > 0.5 ? "white": "black"}
                >{col}</text>
              </g>
            {/if}
          {/each}
        {/if}
      {/each}
    </g>
    <g class="total-x">
      {#each visData.cateSepX as pac}
        <line
          x1="{columnSpacing(pac.line[0]) + config.gap}"
          y1="{modelRow(visData.yAxis.length + 1) + config.boxSize/2}"
          x2="{columnSpacing(pac.line[1]) + config.boxSize}"
          y2="{modelRow(visData.yAxis.length + 1) + config.boxSize/2}"
          stroke-width="{config.lineThickiness}"
          class="cate-line"
        >
        </line>
        <line
          x1="{columnSpacing(pac.line[0]) + config.gap}"
          y1="{modelRow(visData.yAxis.length + 1)}"
          x2="{columnSpacing(pac.line[0]) + config.gap}"
          y2="{modelRow(visData.yAxis.length + 1) + config.boxSize/2}"
          stroke-width="{config.lineThickiness}"
          class="cate-line"
        >
        </line>
        <line
          x1="{columnSpacing(pac.line[1]) + config.boxSize}"
          y1="{modelRow(visData.yAxis.length + 1)}"
          x2="{columnSpacing(pac.line[1]) + config.boxSize}"
          y2="{modelRow(visData.yAxis.length + 1) + config.boxSize/2}"
          stroke-width="{config.lineThickiness}"
          class="cate-line"
        >
        </line>

        <text
          x="{columnSpacing((pac.line[0] + pac.line[1])/2 + .5) }"
          y="{modelRow(visData.yAxis.length + 2)}"
          text-anchor="middle"
          class="category-label">{pac.groupName}</text>
      {/each}
        <g>
          <text
              x="{columnSpacing(visData.xAxis.length + 1)+ config.boxSize/2}"
              y="{modelRow(-2) + config.boxSize/2}"
              text-anchor="middle"
              dominant-baseline="central"
              class="total-count">Paper Count:</text>

          {#each visData.paperCountX as num, i}
            {#if typeof visData.xAxis[i] !== 'string'}
              <text
                x="{columnSpacing(i)}"
                y="{modelRow(visData.yAxis.length + 1) - config.gap}"
                text-anchor="middle"
                dominant-baseline="central"
                class="total-count">{num}</text>
            {/if}
          {/each}
        </g>
      </g>
    <g class="total-y">
      {#each visData.cateSepY as pac}
        <line
          x1="{columnSpacing(visData.xAxis.length + 1) + config.boxSize}"
          y1="{modelRow(pac.line[0]) + config.gap}"
          x2="{columnSpacing(visData.xAxis.length + 1) + config.boxSize}"
          y2="{modelRow(pac.line[1]) + config.boxSize }"
          stroke-width="{config.lineThickiness}"
          class="cate-line"
        >
        </line>
        <line
          x1="{columnSpacing(visData.xAxis.length + 1) }"
          y1="{modelRow(pac.line[0]) + config.gap}"
          x2="{columnSpacing(visData.xAxis.length + 1) + config.boxSize}"
          y2="{modelRow(pac.line[0]) + config.gap}"
          stroke-width="{config.lineThickiness}"
          class="cate-line"
        >
        </line>
        <line
          x1="{columnSpacing(visData.xAxis.length + 1)}"
          y1="{modelRow(pac.line[1]) + config.boxSize}"
          x2="{columnSpacing(visData.xAxis.length + 1) + config.boxSize}"
          y2="{modelRow(pac.line[1]) + config.boxSize}"
          stroke-width="{config.lineThickiness}"
          class="cate-line"
        >
        </line>

        <text
          x="{columnSpacing(visData.xAxis.length + 2) }"
          y="{modelRow((pac.line[0] + pac.line[1])/2 + .5)}"
          text-anchor="left"
          class="category-label">{pac.groupName}</text>

      {/each}
        <g>
          <text
              x="{columnSpacing(-1) - config.boxSize/2}"
              y="{modelRow(visData.yAxis.length) + config.boxSize}"
              text-anchor="end"
              dominant-baseline="central"
              class="total-count">Paper Count:</text>

          {#each visData.paperCountY as num, j}
            {#if typeof visData.yAxis[j] !== 'string'}
              <text
                x="{columnSpacing(visData.xAxis.length + 1)}"
                y="{modelRow(j)}"
                text-anchor="middle"
                dominant-baseline="central"
                class="total-count">{num}</text>
            {/if}
          {/each}
        </g>
    </g>
    {#if verBarId !== -1}
      <rect
        x="{columnSpacing(verBarId) - config.boxSize/2}"
        y="{padding.top - config.boxSize/2}"
        width="{config.boxSize}"
        height="{modelRow(visData.yAxis.length + 1) - padding.top - config.gap*2}"
        fill="#666"
        opacity=".6"
        class="hightlight"
      ></rect>
    {/if}
    {#if horBarId !== -1}
      <rect
        x="{padding.left - config.boxSize/2}"
        y="{modelRow(horBarId) - config.boxSize/2}"
        width="{columnSpacing(visData.xAxis.length-1) - padding.top - config.gap +  config.boxSize/2}"
        height="{config.boxSize}"
        fill="#666"
        opacity=".6"
        class="hightlight"
      ></rect>
    {/if}
  </ZoomSvg>
</div>

<style>
  .corr-menu{
    padding-top:10px;
    width:200px;
  }
  .model-text{
    cursor:pointer;
  }
  .corr-container {
    width: 100%;
    height: 100%;
  }
  .category-label{
    fill:#666;
  }
  .end-line {
    stroke:#e0dcdc;
    stroke-linecap: round;
  }
  .dash-line{
    stroke:#a9a8a8;
  }

  .topic-line{
    stroke-linecap: round;
  }

  .cate-line{
    stroke:#ccc;
    stroke-linecap: square;
  }
  .matrix {
    cursor:pointer;
  }
  .hightlight{
    pointer-events : none;
  }
  .topic-label{

  }
  .total-count {
    fill:#666;
  }
  .cross-count {

  }
</style>