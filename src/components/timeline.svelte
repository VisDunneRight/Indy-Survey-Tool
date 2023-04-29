<script>
	import Slider from '@smui/slider';
	import Tooltip, { Wrapper } from '@smui/tooltip';
	import { createEventDispatcher } from 'svelte';
	import * as d3 from 'd3';

	const dispatch = createEventDispatcher();

	export let data;
	export let filteredData;
	let minYear;
	let maxYear;
	$: valueStart = minYear;
	$: valueEnd = maxYear;
	const padding = {top:3, bottom:3, left:3, right:3};
	const gap = 1;

	function onRangeUpdate() {
		dispatch('message', { start: valueStart, end: valueEnd });
	}

	[minYear, maxYear] = d3.extent(data, (d) => {
		if (d.Year && +d.Year) return Number(d.Year);
	});

	const width = 250, height = 50;
 
	const convertData = (data, min, max) => {
		let res = {};
		for (var i = min; i <= max; i++) {
			res[i] = 0;
		}
		data.forEach((entry) => {
			if (+entry.Year) res[+entry.Year] += 1;
		});
		return Object.values(res);
	};
	let binData = convertData(data, minYear, maxYear);
	$:filterBinData = convertData(filteredData, minYear, maxYear);
	var x = d3.scaleLinear().domain([minYear, maxYear]).range([0, width]);
	var y = d3
		.scaleLinear()
		.domain([0, d3.max(binData)])
		.range([height - padding.top - padding.bottom, 0]);
	const bandWidth = (1.0 / binData.length) * (width - padding.left - padding.right) - gap;
	$: color = (i) => {
		let year = i + minYear;
		if (year < valueStart || year > valueEnd) {
			return '#808080';
		} else {
			return '#69B3A2';
		}
	};
</script>

<div class="timeline-container">
	<div class="title"><strong>Time Filter:</strong></div>
	<div class="date-range">
		<div>{valueStart}</div>
		<div>{valueEnd}</div>
	</div>
	<Slider
		range
		bind:start={valueStart}
		bind:end={valueEnd}
		min={minYear}
		max={maxYear}
		step={1}
		input$aria-label="Timeline"
		on:MDCSlider:change={() => onRangeUpdate()}
	/>

	<div class="chart">
		<svg width={width} height={height}>
			<g>
				{#each binData as d, i}
					<Wrapper>
						<rect
							x={i * (bandWidth + gap) + padding.left} 
							y={y(filterBinData[i]) + padding.bottom}
							width={bandWidth}
							height={height - y(filterBinData[i])  - padding.bottom - padding.top}
							fill={color(i)}/>
						<rect
							x={i * (bandWidth + gap) + padding.left}
							y={y(d) + padding.bottom}
							width={bandWidth}
							height={height - y(d) - padding.bottom - padding.top}
							stroke={"black"}
							stroke-width="{gap}px"
							fill={'none'}
						/>
						<Tooltip>Year:{minYear + i} Total:{filterBinData[i]}</Tooltip>
					</Wrapper>
				{/each}
			</g>
		</svg>
	</div>
</div>

<style>
	.title {
		padding-top: 5px;
		padding-left: 5px;
	}
	.timeline-container {
		height: 150px;
		background-color: var(--mdc-theme-surface, #f8f8f8);
	}
	.date-range {
		padding-left: 10px;
		padding-right: 10px;
		display: flex;
		justify-content: space-between;
	}
	.chart {
		padding-left: 20px;
	}
</style>
