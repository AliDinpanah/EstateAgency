<script lang="ts">
	import AdItem from '@/components/AdItem.svelte';
    import * as Card from '@/components/ui/card';
	import { Phone } from 'lucide-svelte';
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';

	let agency_id: string = '';
    let posts: any = writable([]);
    let agency: any = writable({});

	onMount(async () => {
		agency_id = window.location.pathname.split('/')[window.location.pathname.split('/').length - 1];
		const response = await fetch('http://127.0.0.1:8000/ads/search/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'agency_id': agency_id
            })
        });
        if (response.ok) {
            posts.set(await response.json());
        } else {
            alert("Something went wrong. Please try again later.")
        }

        const agency_response = await fetch('http://127.0.0.1:8000/agency/info/' + agency_id);
        if (agency_response.ok) {
            agency.set((await agency_response.json())['agency']);
        } else {
            alert("Something went wrong. Please try again later.")
        }
	});
</script>

<main class="flex justify-center">
    <div class="flex flex-col gap-8 items-center p-20 pt-0 mt-[-5px]">
        <Card.Root class="max-w-[800px] min-w-[800px] rounded-t-none">
            <Card.Header class="text-center">
                <Card.Title tag="h1" class="font-semibold">
                    {$agency['name']}
                </Card.Title>
            </Card.Header>
            <Card.Content class="flex flex-row justify-between">
                <p class="w-full text-left"><span class="font-semibold mr-3">Phone:</span><span>{$agency['phone'] || 'Unknown'}</span></p>
                <p class="w-full text-center"><span class="font-semibold mr-3">City:</span><span>{$agency['city']}</span></p>
                <p class="w-full text-right"><span class="font-semibold mr-3">Admin Name:</span><span>{$agency['admin_firstname'] + " " + $agency['admin_lastname']}</span></p>
            </Card.Content>
        </Card.Root>
        <secion class="flex flex-row flex-wrap justify-center gap-4 w-full">
            {#each $posts as post}
                <AdItem data={post}  />
            {/each}
        </secion> 
    </div>
</main>