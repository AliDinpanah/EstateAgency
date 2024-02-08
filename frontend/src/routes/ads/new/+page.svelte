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

	const data: any = {};
	let images_url: any = [];
	let images_input: any;
	let rent = true;
	let property_type = 'residential';
	let formData = new FormData();
	let facilities: any = [];
	let conditions: any = [];

	let selectedFacilities: any = {}
	let selectedConditions: any = {}

	onMount(async () => {
		const response = await fetch('http://127.0.0.1:8000/ads/facilities/');
		if(response.ok){
			const data = await response.json();
			facilities = data;
		}
		const response2 = await fetch('http://127.0.0.1:8000/ads/conditions/');
		if(response2.ok){
			const data = await response2.json();
			conditions = data;
		}

		if(!(response.ok && response2.ok)){
			alert("Something went wrong!")
		}

		for(let i = 0; i < facilities.length; i++){
			selectedFacilities[facilities[i]['id']] = false;
		}
		for(let i = 0; i < conditions.length; i++){
			selectedConditions[conditions[i]['id']] = false;
		}
	})

	async function displayImages(e: any){
		formData.set("file", e.target.files[0]);
		const response = await fetch('http://127.0.0.1:8000/files/upload/', {
			method: 'POST',
			body: formData
		})
		if(response.ok){
			const data = await response.json();
			images_url = [...images_url, data['filename']];
		} else {
			alert(JSON.stringify(await response.json()))
		}
	}

	async function submit(event: any) {
		event.preventDefault();
		if(rent){
			data['price'] = null;
		} else {
			data['rent'] = null;
			data['mortgage'] = null;
		}
		if(images_url.length == 0){
			alert("Please upload at least one image!")
			return;
		}
		const response = await fetch('http://127.0.0.1:8000/ads/add/', {
			method: 'POST',
			body: JSON.stringify({
				...data,
				'facilities': Object.keys(selectedFacilities).filter((key) => selectedFacilities[key]),
				'conditions': Object.keys(selectedConditions).filter((key) => selectedConditions[key]),
				'images': images_url,
				'primary_image': images_url[0],
				'property_type': property_type,
				'ad_type': rent ? 'rent' : 'sell'
			}),
			headers: {
				'Content-Type': 'application/json',
				'X-Auth-Token': localStorage.getItem('token') as string
			}
		});

		if (response.ok) {
			console.log('ok');
			alert('Ad added successfully!');
		} else {
			alert((await response.json())['message']);
		}
	}
</script>

<div class="flex min-h-screen items-center justify-center">
	<form on:submit={submit}>
		<Card.Root class="my-5 w-[600px]">
			<Card.Header>
				<Card.Title tag="h1" class="text-2xl font-semibold">New Ad</Card.Title>
				<!-- <Card.Description>Submit a new ad</Card.Description> -->
			</Card.Header>
			<Card.Content>
				<div class="flex w-full items-start gap-4">
					<div class="grid w-full flex-col gap-4">
						<div class="flex flex-row gap-4">
							<div class="flex w-full flex-col space-y-1.5">
								<Label for="city">City</Label>
								<Input id="city" name="city" placeholder="e.g. Tehran" bind:value={data['city']} />
							</div>
							<div class="flex w-full flex-col space-y-1.5">
								<Label for="district">District</Label>
								<Input
									id="district"
									name="district"
									placeholder="e.g. Tajrish"
									bind:value={data['district']}
								/>
							</div>
						</div>

						<div class="flex flex-row gap-4">
							<div class="flex w-full flex-row">
								<div class="flex w-full flex-col">
									<Label class="pb-2">Ad Type</Label>
									<div class="flex w-full flex-row gap-4">
										<Button
											class="w-full"
											variant={rent ? 'outline' : 'default'}
											on:click={() => (rent = false)}>Sell</Button
										>
										<Button
											class="w-full"
											variant={rent ? 'default' : 'outline'}
											on:click={() => (rent = true)}>Rent</Button
										>
									</div>
								</div>
							</div>
							<div class="flex w-full flex-row gap-4">
								<div class="flex w-full flex-col space-y-1.5 {rent ? 'hidden' : ''}">
									<Label for="price">Price</Label>
									<Input id="price" name="price" type="number" min="-1" placeholder="200,000" bind:value={data['price']} />
								</div>
								<div class="flex w-full flex-col space-y-1.5 {rent ? '' : 'hidden'}">
									<Label for="mortgage">Mortgage</Label>
									<Input
										id="mortgage"
										name="mortgage"
										type="number"
										min="-1"
										placeholder="1000"
										bind:value={data['mortgage']}
									/>
								</div>
								<div class="flex w-full flex-col space-y-1.5 {rent ? '' : 'hidden'}">
									<Label for="rent">Rent</Label>
									<Input id="rent" type="number" min="-1" name="rent" placeholder="1000" bind:value={data['rent']} />
								</div>
							</div>
						</div>

						<div class="flex flex-row gap-4">
							<div class="flex w-full flex-col space-y-1.5">
								<Label for="metrage">Metrage</Label>
								<Input
									id="metrage"
									name="metrage"
									type="number"
									min="50"
									placeholder="e.g. 150"
									bind:value={data['metrage']}
								/>
							</div>
							<div class="flex w-full flex-col space-y-1.5">
								<Label for="rooms-count">Number of Rooms</Label>
								<Input
									id="rooms-count"
									name="rooms-count"
									type="number"
									min="0"
									placeholder="e.g. 3"
									bind:value={data['rooms_count']}
								/>
							</div>
						</div>

						<div class="flex flex-col gap-4">
							<Label>Application</Label>
							<div class="flex flex-row justify-between gap-4">
								<Button
									class="w-full"
									variant={property_type == 'residential' ? 'default' : 'outline'}
									on:click={() => (property_type = 'residential')}>Residential</Button
								>
								<Button
									class="w-full"
									variant={property_type == 'commerical' ? 'default' : 'outline'}
									on:click={() => (property_type = 'commerical')}>Commercial</Button
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
                                                on:click={() => selectedFacilities[facility['id']] = !selectedFacilities[facility['id']]}>{facility["name"]}</Button
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
                                                on:click={() => selectedConditions[condition['id']] = !selectedConditions[condition['id']]}>{condition["name"]}</Button
                                            >
                                        {/each}
                                    </div>
								</Accordion.Content>
							</Accordion.Item>
						</Accordion.Root>

                        <div class="flex w-full flex-col space-y-1.5">
                            <Label for="title">Title</Label>
                            <Input
                                id="title"
                                name="title"
                                placeholder="Ener the ad's title"
                                bind:value={data['title']}
                            />
                        </div>

                        <div class="flex w-full flex-col space-y-1.5">
                            <Label for="description">Description</Label>
                            <Textarea
                                id="description"
                                name="description"
                                placeholder="Ener the ad's desctiption"
                                bind:value={data['description']}
                            />
                        </div>

                        <div class="flex flex-col gap-4">
							<Label>Images</Label>
							<input class="hidden" accept="image/png, image/jpeg" id="many" type="file" bind:this={images_input} on:change={displayImages} />
							<div class="flex flex-row justify-start gap-2 flex-wrap">
								<Button class="w-[100px] h-[100px]" variant="outline" on:click={images_input.click()}><PlusIcon /></Button>
								{#each images_url as image_url}
									<img class="w-[100px] h-[100px]" src={"http://127.0.0.1:8000/files/" + image_url} alt="" />
								{/each}
							</div>
						</div>
					</div>
				</div>
			</Card.Content>
			<Card.Footer class="flex justify-between">
				<Button variant="outline" on:click={() => window.location.href = "/"}>Cancel</Button>
				<Button type="submit">Submit</Button>
			</Card.Footer>
		</Card.Root>
	</form>
</div>
