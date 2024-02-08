<script lang="ts">
	import * as Card from '@/components/ui/card';
	import * as Carousel from '$lib/components/ui/carousel/index.js';
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';

	let ad_uid: string = '';
	let ad_info: any = writable({"images": [], "facilities": [], "conditions": [], "details": {"": ""}});

	onMount(async () => {
		ad_uid = window.location.pathname.split('/')[window.location.pathname.split('/').length - 1];
		const response = await fetch(`http://127.0.0.1:8000/ads/get/${ad_uid}`, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json'
			}
		});
		if (response.ok) {
			console.log('ok');
			$ad_info = await response.json();
		} else {
			alert('Something went wrong!');
			console.log(await response.json());
		}
	});
</script>

<div class="flex flex-col items-center justify-center py-5">
	<Carousel.Root class="w-[800px]">
		<Carousel.Content>
            {#each $ad_info["images"] as image_url}
                <Carousel.Item>
                    <img src={image_url} alt="" class="w-[800px] h-[400px] object-cover rounded-md mb-5" />
                </Carousel.Item>
            {/each}
		</Carousel.Content>
		<Carousel.Previous />
		<Carousel.Next />
	</Carousel.Root>

	<Card.Root class="w-[800px]">
		<Card.Header>
			<Card.Title tag="h1" class="font-semibold">
				{$ad_info['title']}
			</Card.Title>
		</Card.Header>
		<Card.Content>
			<p>{$ad_info['description']}</p>
		</Card.Content>
		<Card.Footer class="flex flex-col items-start">
            <h2 class="text-l font-semibold mb-2">Facilities</h2>
            <div class="flex items-start flex-wrap gap-2 mb-5">
                {#each $ad_info["facilities"] as facility}
                    <span class="border-2 py-1 px-4 border-sky-500 text-sky-500 hover:text-white hover:bg-sky-500 cursor-pointer rounded-full font-semibold text-sm">{facility["name"]}</span>
                {/each}
            </div>

            <h2 class="text-l font-semibold mb-2">Conditions</h2>
            <div class="flex items-start flex-wrap gap-2 mb-5">
                {#each $ad_info["conditions"] as condition}
                    <span class="border-2 py-1 px-4 border-sky-500 text-sky-500 hover:text-white hover:bg-sky-500 cursor-pointer rounded-full font-semibold text-sm">{condition["name"]}</span>
                {/each}
            </div>
        </Card.Footer>
	</Card.Root>

    <Card.Root class="w-[800px] mt-5">
        <Card.Header>
            <Card.Title tag="h2" class="font-bold">
                Details
            </Card.Title>
        </Card.Header>

        <Card.Content class="flex flex-col gap-2">
            {#each Object.entries($ad_info["details"]) as [key, value]}
				{#if key == "Agency"}
                <a href="/agency/{$ad_info['agency_id']}" class="flex flex-row justify-between "><span class="font-semibold">{key}</span><span>{value}</span></a>
				{:else}
                <p class="flex flex-row justify-between "><span class="font-semibold">{key}</span><span>{value}</span></p>
				{/if}
			{/each}
        </Card.Content>
    </Card.Root>
</div>
