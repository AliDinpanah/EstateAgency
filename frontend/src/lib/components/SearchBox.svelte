<script lang="ts">
    import { Input } from "@/components/ui/input"
    import { Button } from "@/components/ui/button"
    import { Search } from 'lucide-svelte'
    import { FilterIcon } from "lucide-svelte"
    import * as Drawer from "$lib/components/ui/drawer";
    import * as Sheet from "$lib/components/ui/sheet";
    import FilterSearch from "@/components/FilterSearch.svelte"

    export let posts: any = undefined;

    let searchQuery: string;
    const searchFilters: any = {};


    async function search() {
        for (const key in searchFilters) {
            if (searchFilters[key] == 'all' || searchFilters[key] == '') {
                delete searchFilters[key];
            }
        }
        const response = await fetch('http://127.0.0.1:8000/ads/search/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'text': searchQuery,
                ...searchFilters
            })
        });
        if (response.ok) {
            posts.set(await response.json());
            document.getElementById("posts")?.scrollIntoView({ behavior: 'smooth' });
            console.log(posts);
        } else if(response.status == 404) {
            alert('No results found!');
        } else {
            alert('Something went wrong!');
        }
    }
</script>


<div class='w-8/12 text-center relative'>
    <Input id='test' class='rounded-full h-16 w-full font-sans text-lg font-bold px-5' bind:value={searchQuery} />
    <div class="absolute top-0 right-0 my-3 mx-3 flex gap-1">
        <Sheet.Root>
            <Sheet.Trigger><Button class="rounded-full bg-blue-600"><FilterIcon /></Button></Sheet.Trigger>
            <Sheet.Content class="flex items-center min-w-[600px] overflow-y-auto">
                <FilterSearch data={searchFilters} className="w-full p-5 overflow-y-auto" />
            </Sheet.Content>
        </Sheet.Root>
        
        <Button
        class='center px-5 py-2 rounded-full'
            on:click={search}>
            <span class="inline">Search</span><Search class='w-5 ml-2 inline' />
        </Button>
    </div>
</div>