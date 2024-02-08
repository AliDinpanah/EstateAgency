<script lang="ts">
	import SearchBox from '@/components/SearchBox.svelte';
	import { Building, UserPlus, LogInIcon, LogOutIcon, SquarePenIcon, UserCogIcon } from 'lucide-svelte';
	import AdItem from '@/components/AdItem.svelte';
	import { writable } from 'svelte/store';
	import Button from '@/components/ui/button/button.svelte';
	import { onMount } from 'svelte';

	const posts: any = writable([]);

	let loggedIn: boolean = false;
	let role: string = '';

	onMount(async () => {
		const response = await fetch('http://127.0.0.1:8000/ads/search/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				'text': '',
				'ad_type': 'all',
				'property_type': 'all',
				'facilities': [],
				'conditions': []
			})
		});
		if (response.ok) {
			posts.set(await response.json());
		} else {
			alert('Something went wrong!');
		}

		loggedIn = localStorage.getItem('token') !== null;
		role = localStorage.getItem('token')?.split(":")[1].split("-")[1] || "";
	});


	async function logout() {
		localStorage.removeItem('token');
		window.location.href = '/';
	}

</script>

<main class="flex h-full min-h-screen flex-col items-center justify-center p-24" dir="ltr">
	<h1 class="m-10 inline text-4xl font-bold">Looking for a home? Choose your neighbor...</h1>
	<SearchBox posts={posts} />
	<div class="flex gap-2 py-10">		
		{#if loggedIn}
			{#if role === 'agency'}
				<a href="/ads/new" class="flex gap-1 rounded-full bg-zinc-100 px-5 py-2 hover:bg-zinc-300"
					><SquarePenIcon className="inline" /><span class="inline">Post a New Ad</span></a
				>
			{:else} 
				<a href="/user/profile" class="flex gap-1 rounded-full bg-zinc-100 px-5 py-2 hover:bg-zinc-300"
					><UserCogIcon className="inline" /><span class="inline">Edit Profile</span></a
				>
			{/if}
			<Button on:click={logout} class="flex gap-1 rounded-full bg-zinc-100 px-5 py-2 text-black hover:bg-zinc-300"
				><LogOutIcon className="inline" /><span class="inline">Log out</span></Button
			>
		{:else}
			<a href="/agency/register" class="flex gap-1 rounded-full bg-zinc-100 px-5 py-2 hover:bg-zinc-300"
				><Building className="inline" /><span class="inline">Register Your Agency</span></a
			>
			<a href="/user/signup" class="flex gap-1 rounded-full bg-zinc-100 px-5 py-2 hover:bg-zinc-300"
				><UserPlus className="inline" /><span class="inline">Create an account</span></a
			>
			<a href="/user/login" class="flex gap-1 rounded-full bg-zinc-100 px-5 py-2 hover:bg-zinc-300"
				><LogInIcon className="inline" /><span class="inline">Log in</span></a
			>
		{/if}
	</div>
</main>
<div id="posts" class="flex flex-row min-h-screen flex-wrap justify-center gap-8 bg-gray-100 p-10">
	{#each $posts as post}
		<AdItem
			data={post}
		/>
	{/each}
</div>
