<script lang="ts">
    import * as Card from '@/components/ui/card';

    export let data: any = {};
</script>

<Card.Root class="w-[400px] flex flex-col justify-start">
    <img src={data['primary_image']} alt="" class="w-[400px] h-[250px] object-cover rounded-md rounded-b-none mb-5" />
    <Card.Header>
        <Card.Title tag="h1" class="font-semibold">
            <a href="/ads/{data['id']}">{data['title']}</a>
        </Card.Title>
    </Card.Header>
    <Card.Content>
        <p>{data['description']}</p>
    </Card.Content>
    <Card.Footer class="flex flex-row justify-between mt-auto">
        {#if data['price'] != null}
            <span class="text-lg font-semibold">Price:</span>
            <span class="text-lg font-semibold">{data['price']}</span>
        {:else}
            <div>
                <span class="text-lg font-semibold">Rent: </span>
                <span class="text-lg font-semibold">{data['rent']}</span>
            </div>
            <div>
                <span class="text-lg font-semibold">Mortgage: </span>
                <span class="text-lg font-semibold">{data['mortgage']}</span>
            </div>
        {/if}
    </Card.Footer>
</Card.Root>