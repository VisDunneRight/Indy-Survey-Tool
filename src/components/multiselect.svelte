<script>
	import Chip, { Set, Text } from '@smui/chips';
	export let list = [];
</script>

<Set chips={list} let:chip nonInteractive style="padding:0px">
	<Chip {chip}>
		<Text>{chip}</Text>
	</Chip>
</Set>

<style>
</style>
