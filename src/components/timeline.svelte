<script>
// @ts-nocheck

	import RangeSlider from 'svelte-range-slider-pips'
	import {Heading, P} from "flowbite-svelte";
	import { timeFilters } from "../store"
	import * as d3 from 'd3';

	export let data;
	export let filteredData;
	let minYear;
	let maxYear;
	$: value = [minYear, maxYear];
	const padding = {top:3, bottom:3, left:3, right:3};
	const gap = 1;

	function onRangeUpdate() {
		timeFilters.set({start:value[0], end:value[1]})
	}

	[minYear, maxYear] = d3.extent(data, (d) => {
		if (d.Year && +d.Year) return Number(d.Year);
	});

	timeFilters.set({start:minYear, end:maxYear})
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
		if (year < value[0] || year > value[1]) {
			return '#808080';
		} else {
			return '#69B3A2';
		}
	};
</script>

<div class="timeline-container">
	<Heading tag="h4"><strong>Time Filter:</strong></Heading>
	<div class="date-range">
		<P>{value[0]}</P>
		<P>{value[1]}</P>
	</div>
	<RangeSlider
	 	range
		bind:values={value}
		min={minYear}
		max={maxYear}
		step={1}
		pushy
		on:stop={() => onRangeUpdate()}
	/>

	<div class="chart">
		<svg width={width} height={height}>
			<g>
				{#each binData as d, i}
					<g >
						<rect id="rect-{i}"
							x={i * (bandWidth + gap) + padding.left} 
							y={y(filterBinData[i]) + padding.bottom}
							width={bandWidth}
							height={height - y(filterBinData[i])  - padding.bottom - padding.top}
							fill={color(i)}>
							<title>Year:{minYear + i} Total:{filterBinData[i]}</title>		
					</rect>
						<rect
							x={i * (bandWidth + gap) + padding.left}
							y={y(d) + padding.bottom}
							width={bandWidth}
							height={height - y(d) - padding.bottom - padding.top}
							stroke={"black"}
							stroke-width="{gap}px"
							fill={'none'}

						>
						<title>Year:{minYear + i} Total:{filterBinData[i]}</title>
						</rect>
					</g>					
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
