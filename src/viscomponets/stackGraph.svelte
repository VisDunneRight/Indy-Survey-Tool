<script>
  // @ts-nocheck
  import {
    blend_colors,
    spectralColorScheme,
    spectralColorSchemeText,
  } from "./util";
  import * as d3 from "d3";

  import { filterBy } from "../store";

  import {
    Checkbox,
    Button,
    Dropdown,
    DropdownItem,
    Search,
    Badge,
    Label,
  } from "flowbite-svelte";
  import { ChevronDownSolid, UserRemoveSolid } from "flowbite-svelte-icons";
  import { createEventDispatcher } from "svelte";
  import { timeFilters } from "../store";
  const dispatch = createEventDispatcher();

  const config = { height: 200, width: 600, size: 10, gap: 4 };
  const padding = { top: 30, right: 40, bottom: 10, left: 50 };

  export let data;
  export let selectedCate;
  $: startRange = $timeFilters.start;
  $: endRange = $timeFilters.end;
  $: stepSize = 2;
  let otherCheck = true;

  let w = 100,
    h = 100;
  function getDimInfo(selectedDim, filterBy) {
    let selectProp = undefined;
    let ind = -1;
    filterBy.forEach((prop, i) => {
      if ("groupName" in prop) {
        if (prop["groupName"] === selectedDim) {
          selectProp = prop;
          ind = i;
          return;
        }
      } else {
        if (prop["name"] === selectedDim) {
          selectProp = prop;
          ind = i;
          return;
        }
      }
    });
    //In the case the
    filterBy.forEach((prop, i) => {
      if ("groupName" in prop) {
        prop.categories.forEach((cate) => {
          if (cate["name"] === selectedDim) {
            selectProp = cate;
            ind = i;
            return;
          }
        });
      }
    });

    return selectProp;
  }

  function genData(
    data,
    cate,
    selectedTags,
    startRange,
    endRange,
    step,
    otherCheck
  ) {
    let dataset = {};
    let catePaths = {};
    let selectedCate = {};

    if ("groupName" in cate) {
      data.forEach((ele) => {
        const numYear = parseInt(ele.Year);
        if (numYear >= startRange) {
          const year =
            Math.floor((numYear - startRange) / step) * step + startRange;
          if (!(year in dataset)) {
            dataset[year] = {};
          }
          cate.categories.forEach((res) => {
            ele[res.name].forEach((tag) => {
              dataset[year][tag] = (dataset[year][tag] || 0) + 1;
            });
          });
        }
      });
      selectedTags.forEach((ele) => {
        selectedCate[ele] = { path: [], total: 0, name: ele, pathSum: [] };
      });

      cate.categories.forEach((res) => {
        res.values.forEach((tag) => {
          catePaths[tag] = { path: [], total: 0, name: tag, pathSum: [] };
          for (let i = startRange; i <= endRange; i += step) {
            const x = ((i - startRange) / step) * config.size;
            if (i in dataset && tag in dataset[i]) {
              const count = dataset[i][tag];
              catePaths[tag].path.push({
                x: x,
                y: count,
              });
              catePaths[tag].total += count;
            } else {
              catePaths[tag].path.push({ x: x, y: 0 });
            }
          }
        });
      });
    } else {
      data.forEach((ele) => {
        const numYear = parseInt(ele.Year);
        if (numYear >= startRange) {
          const year =
            Math.floor((numYear - startRange) / step) * step + startRange;
          if (!(year in dataset)) {
            dataset[year] = {};
          }
          ele[cate.name].forEach((tag) => {
            dataset[year][tag] = (dataset[year][tag] || 0) + 1;
          });
        }
      });

      selectedTags.forEach((ele) => {
        selectedCate[ele] = { path: [], total: 0, name: ele, pathSum: [] };
      });
      //Find the max path
      cate.values.forEach((tag) => {
        catePaths[tag] = { path: [], total: 0, name: tag, pathSum: [] };
        for (let i = startRange; i <= endRange; i += step) {
          const x = ((i - startRange) / step) * config.size;
          if (i in dataset && tag in dataset[i]) {
            const count = dataset[i][tag];
            catePaths[tag].path.push({
              x: x,
              y: count,
            });
            catePaths[tag].total += count;
          } else {
            catePaths[tag].path.push({ x: x, y: 0 });
          }
        }
      });
    }
    Object.values(catePaths).forEach((val) => {
      if (selectedTags.includes(val.name)) {
        selectedCate[val.name] = val;
      } else if (otherCheck) {
        selectedCate["Other"].total += val.total;
        val.path.forEach((point, idx) => {
          if (idx >= selectedCate["Other"].path.length) {
            selectedCate["Other"].path.push({ x: point.x, y: point.y });
          } else {
            selectedCate["Other"].path[idx].y += point.y;
          }
        });
      }
    });

    //Back of the visualization
    let arrayCate = Object.values(selectedCate);

    //Generate the frequence of the each tag
    let totalCount = [];
    const numElements = arrayCate[0]?.path.length;
    for (let i = 0; i < numElements; i += 1) {
      let count = 0;
      arrayCate.forEach((cate) => {
        count += cate.path[i].y;
        cate.pathSum.push({ x: cate.path[i].x, y: count });
      });
      totalCount.push(count);
    }
    arrayCate.forEach((cate) => {
      for (let i = 0; i < numElements; i += 1) {
        cate.pathSum[i].y = cate.pathSum[i].y / totalCount[i] || 0;
      }
    });

    //flip for rendering and return array
    return arrayCate.reverse();
  }

  function getListValues(cate) {
    let listValues = [];
    if (cate !== undefined) {
      if ("groupName" in cate) {
        cate.categories.forEach((res) => {
          listValues.push(...res.values);
        });
      } else {
        listValues = [...cate.values];
      }
    }
    return listValues;
  }

  function createXAxis(start, end) {
    let xTicks = [];
    for (let i = start; i <= end; i += stepSize) {
      xTicks.push(i);
    }
    return xTicks;
  }

  function changeTag(ele, name) {
    const checked = ele.target.checked;
    if (checked) {
      addTag(name);
    } else {
      removeTag(name);
    }
  }
  function addTag(name) {
    selected.push(name);
    selected = selected;
  }
  function removeTag(name) {
    selected = selected.filter((tag) => {
      return tag !== name;
    });
  }

  $: cate = getDimInfo(selectedCate, $filterBy);
  //comboBox for selecting tags

  $: listValues = getListValues(cate);
  $: selected = [];
  let prevSelectedCate = "";

  $: if (prevSelectedCate !== selectedCate) {
    selected = [];
    prevSelectedCate = selectedCate;
  }

  $: tags = listValues.map((name, i) => {
    let plus = 0;
    if (otherCheck) {
      plus = 1;
    }
    return {
      value: name,
      name: name,
      idx: i + plus,
    };
  });

  $: if (otherCheck) {
    if (selected.includes("Other") === false) {
      selected = ["Other", ...selected];
      selected = selected;
    }
  } else {
    selected = selected.filter((tag) => {
      return tag !== "Other";
    });
  }
  $: dataset = genData(
    data,
    cate,
    selected,
    startRange,
    endRange,
    stepSize,
    otherCheck
  );

  $: range = endRange - startRange;
  // $: console.log(dataset);
  $: y = d3
    .scaleLinear()
    .domain([0, 1])
    .range([config.height - padding.bottom, padding.top]);
  $: x = d3
    .scaleLinear()
    .domain([0, (range / stepSize) * config.size])
    .range([padding.left, config.width - padding.right]);

  $: if (dataset) {
    dataset.forEach((tag) => {
      tag.pathLine = `M${x(tag.pathSum[0].x)},${y(tag.pathSum[0].y)}`;
      console.log(tag.pathSum)
      for (let i = 0; i < tag.pathSum.length - 1; i++) {
        
        const cp = tag.pathSum[i];
        const np = tag.pathSum[i + 1];
        // tag.pathLine +=`L${x(cp.x)},${y(cp.y)} L${x(cp.x + config.size)},${y(cp.y/csp || 0)}`;
        tag.pathLine +=
          ` L${x(cp.x + config.size - config.gap)},${y(cp.y)}` +
          ` Q${x(cp.x + config.size)},${y(cp.y)}` +
          ` ${x(np.x)},${y((np.y + cp.y) / 2 || 0)}` +
          ` T${x(np.x + config.gap)},${y(np.y || 0)}`;
      }
      tag.pathLine += `L${x(
        tag.pathSum[tag.pathSum.length - 1].x + config.size
      )},${y(tag.pathSum[tag.pathSum.length - 1].y)}`;
    });
  }
  //yticks and xTicks
  let yTicks = [0, 0.2, 0.4, 0.6, 0.8, 1.0];
  $: xTicks = createXAxis($timeFilters.start, $timeFilters.end);
</script>

<div class="stack-container" bind:clientWidth={w} bind:clientHeight={h}>
  <Label>Add Tags:</Label>
  <Button
    >Dropdown search<ChevronDownSolid
      class="w-3 h-3 ms-2 text-white dark:text-white"
    /></Button
  >
  <Dropdown class="overflow-y-auto px-3 pb-3 text-sm h-44">
    <div slot="header" class="p-3">
      <Search size="md" />
    </div>
    {#each tags as tag}
      <li class="rounded p-2 hover:bg-gray-100 dark:hover:bg-gray-600">
        <Checkbox
          checked={selected.includes(tag.name)}
          on:click={(e) => changeTag(e, tag.name)}>{tag.name}</Checkbox
        >
      </li>
    {/each}
  </Dropdown>
  <Checkbox bind:checked={otherCheck} touch>Group Rest as Other</Checkbox>
  <div >
    {#each selected as sel, idx}
      <Badge
        style="color:{spectralColorSchemeText[
          idx % 11
        ]};background-color:{spectralColorScheme[idx % 11]};margin:2px;"
        dismissable
        on:close={(e) => removeTag(sel)}
      >
        {sel}
      </Badge>
    {/each}
  </div>

  <svg class="svg-container" viewBox="0 0 600 300">
    <g class="y-axis dark:fill-gray-300">
      <text
        x={x(0) + 50}
        y="12"
        text-anchor="end"
        font-weight="bold"
        alignment-baseline="middle">Frequency</text
      >
      {#each yTicks as tick}
        <g
          class="tick tick-{tick}"
          transform="translate({x(0) - 10}, {y(tick)})"
        >
          <text x="-3" alignment-baseline="middle" text-anchor="end"
            >{tick * 100}%</text
          >
          <line x1="-3" x2="5" stroke="black" stroke-width="2" />
        </g>
      {/each}
    </g>
    <g class="x-axis">
      {#each xTicks as tick, i}
        <text
          text-anchor="start"
          transform="translate({x(i * config.size + config.size / 2)}, {y(0) +
            10}) rotate(45)"
          alignment-baseline="middle"
          class="model-text dark:fill-gray-300">{tick}</text
        >
      {/each}
    </g>
    <g>
      {#each dataset as tags, ind}
        <path
          class="path-area"
          fill={spectralColorScheme[ind]}
          stroke={blend_colors(spectralColorScheme[ind], "#000000", 0.2)}
          d={tags.pathLine +
            `L${x((Math.floor(range / stepSize) + 1) * config.size)},${y(
              0
            )}L${x(0)},${y(0)}Z`}
        />
        <!-- <path style="z-index:{totalNumTags - ind}" stroke={defaultColors[ind]} class="path-line" d={tags.pathLine} /> -->
      {/each}
    </g>
  </svg>
</div>

<style>
  .path-line {
    fill: none;
    /* stroke: rgb(0, 100, 100); */
    stroke-linejoin: round;
    stroke-linecap: round;
    stroke-width: 3;
  }

  .model-text {
    font-weight: bold;
  }
  .path-area {
  }
  .stack-container {
    width: 100%;
    height: 100%;
    padding-top: 20px;
  }
</style>
