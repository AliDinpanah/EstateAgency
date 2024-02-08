<script lang="ts">
	import { Button } from '@/components/ui/button';
	import * as Card from '@/components/ui/card';
	import { Input } from '@/components/ui/input';
	import { Label } from '@/components/ui/label';
	import {
		Select,
		SelectContent,
		SelectItem,
		SelectTrigger,
		SelectValue
	} from '@/components/ui/select';
	import * as Accordion from '$lib/components/ui/accordion';
	import Textarea from '@/components/ui/textarea/textarea.svelte';
	import { PlusIcon } from 'lucide-svelte';
	import { onMount } from 'svelte';

	export let data: any = {};
	export let className: string = '';

	let ad_type: string = 'all';
	let property_type = 'all';
	let facilities: any = [];
	let conditions: any = [];

	let selectedFacilities: any = {};
	let selectedConditions: any = {};

	$: data['facilities'] = Object.keys(selectedFacilities).filter((key) => selectedFacilities[key]);
	$: data['conditions'] = Object.keys(selectedConditions).filter((key) => selectedConditions[key]);
	$: data['ad_type'] = ad_type;
	$: data['property_type'] = property_type;

	onMount(async () => {
		const response = await fetch('http://127.0.0.1:8000/ads/facilities/');
		if (response.ok) {
			const data = await response.json();
			facilities = data;
		}
		const response2 = await fetch('http://127.0.0.1:8000/ads/conditions/');
		if (response2.ok) {
			const data = await response2.json();
			conditions = data;
		}

		if (!(response.ok && response2.ok)) {
			alert('Something went wrong!');
		}

		for (let i = 0; i < facilities.length; i++) {
			selectedFacilities[facilities[i]['id']] = false;
		}
		for (let i = 0; i < conditions.length; i++) {
			selectedConditions[conditions[i]['id']] = false;
		}
	});
</script>

<form class="grid w-full flex-col gap-4 {className}">
		<div class="flex w-full flex-row gap-4">
            <Button class="w-full" variant={ad_type == 'all' ? 'default' : 'outline'} on:click={() => (ad_type = 'all')}
                >All</Button
            >
			<Button class="w-full" variant={ad_type == "sale" ? 'default' : 'outline'} on:click={() => (ad_type = "sale")}
				>For Sale</Button
			>
			<Button class="w-full" variant={ad_type == "rent" ? 'default' : 'outline'} on:click={() => (ad_type = "rent")}
				>For Rent</Button
			>
		</div>

		<div class="grid grid-cols-2 gap-4 {ad_type == "rent" ? 'hidden' : ''}">
			<div class="flex flex-col space-y-1.5">
				<Label for="min-price">Min Price</Label>
				<Input type="number" min="-1" id="min-price" bind:value={data['min_price']} />
			</div>
			<div class="flex flex-col space-y-1.5">
				<Label for="max-price">Max Price</Label>
				<Input type="number" min="-1" id="max-price" bind:value={data['max_price']} />
			</div>
		</div>

		<div class="grid grid-cols-4 gap-4 {ad_type == "sale" ? 'hidden' : ''}">
			<div class="flex flex-col space-y-1.5">
				<Label for="min-rent">Min Rent</Label>
				<Input type="number" min="-1" id="min-rent" bind:value={data['min_rent']} />
			</div>
			<div class="flex flex-col space-y-1.5">
				<Label for="max-rent">Max Rent</Label>
				<Input type="number" min="-1" id="max-rent" bind:value={data['max_rent']} />
			</div>

			<div class="flex flex-col space-y-1.5">
				<Label for="min-mortgage">Min Mortgage</Label>
				<Input type="number" min="-1" id="min-rent" bind:value={data['min_mortgage']} />
			</div>
			<div class="flex flex-col space-y-1.5">
				<Label for="max-mortgage">Max Mortgage</Label>
				<Input type="number" min="-1" id="max-mortgage" bind:value={data['max_mortgage']} />
			</div>
		</div>

		<div class="grid grid-cols-2 gap-4">
			<div class="flex flex-col space-y-1.5">
				<Label for="min-metrage">Min Metrage</Label>
				<Input type="number" min="50" id="min-metrage" bind:value={data['min_metrage']} />
			</div>
			<div class="flex flex-col space-y-1.5">
				<Label for="max-metrage">Max Metrage</Label>
				<Input type="number" min="50" id="max-metrage" bind:value={data['max_metrage']} />
			</div>
		</div>

        <div class="grid grid-cols-2 gap-4">
			<div class="flex flex-col space-y-1.5">
				<Label for="min-rooms-count">Min Number of Rooms</Label>
				<Input type="number" min="0" id="min-rooms-count" bind:value={data['min_rooms_count']} />
			</div>
			<div class="flex flex-col space-y-1.5">
				<Label for="max-rooms-count">Max Number of Rooms</Label>
				<Input type="number" min="0" id="max-rooms-count" bind:value={data['max_rooms_count']} />
			</div>
		</div>



		<div class="flex flex-col gap-4">
			<Label>Application</Label>
			<div class="flex flex-row justify-between gap-4">
				<Button
					class="w-full"
					variant={property_type == 'all' ? 'default' : 'outline'}
					on:click={() => (property_type = 'all')}>All</Button
				>
				<Button
					class="w-full"
					variant={property_type == 'residential' ? 'default' : 'outline'}
					on:click={() => (property_type = 'residential')}>Residential</Button
				>
				<Button
					class="w-full"
					variant={property_type == 'commercial' ? 'default' : 'outline'}
					on:click={() => (property_type = 'commercial')}>Commercial</Button
				>
				<Button
					class="w-full"
					variant={property_type == 'office' ? 'default' : 'outline'}
					on:click={() => (property_type = 'office')}>Office</Button
				>
				<Button
					class="w-full"
					variant={property_type == 'industrial' ? 'default' : 'outline'}
					on:click={() => (property_type = 'industrial')}>Industrial</Button
				>
			</div>
		</div>

		<Accordion.Root>
			<Accordion.Item value="facilities">
				<Accordion.Trigger>Facilities</Accordion.Trigger>
				<Accordion.Content>
					<div class="flex flex-wrap justify-start gap-2">
						{#each facilities as facility}
							<Button
								class=""
								variant={selectedFacilities[facility['id']] ? 'default' : 'outline'}
								on:click={() =>
									(selectedFacilities[facility['id']] = !selectedFacilities[facility['id']])}
								>{facility['name']}</Button
							>
						{/each}
					</div>
				</Accordion.Content>
			</Accordion.Item>

			<Accordion.Item value="conditions">
				<Accordion.Trigger>Conditions</Accordion.Trigger>
				<Accordion.Content>
					<div class="flex flex-wrap justify-start gap-2">
						{#each conditions as condition}
							<Button
								class=""
								variant={selectedConditions[condition['id']] ? 'default' : 'outline'}
								on:click={() =>
									(selectedConditions[condition['id']] = !selectedConditions[condition['id']])}
								>{condition['name']}</Button
							>
						{/each}
					</div>
				</Accordion.Content>
			</Accordion.Item>
		</Accordion.Root>
</form>
