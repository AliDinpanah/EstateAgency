<script lang="ts">
    import { Button } from "@/components/ui/button";
    import * as Card  from "@/components/ui/card";
    import { Input } from "@/components/ui/input";
    import { Label } from "@/components/ui/label";
    import { onMount } from "svelte";

    const data: any = {};
    
    onMount(async () => {
        await fetch("http://127.0.0.1:8000/user/me", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "X-Auth-Token": localStorage.getItem("token") as string
            }
        }).then(response => response.json()).then(json => {
            data['first_name'] = json['user']['first_name'];
            data['last_name'] = json['user']['last_name'];
            data['email'] = json['user']['email'];
        });
    });

    async function submit(event: any) {
        event.preventDefault();
        const response = await fetch("http://127.0.0.1:8000/user/update", {
            method: "PUT",
            body: JSON.stringify({...data}),
            headers: {
                "Content-Type": "application/json",
                "X-Auth-Token": localStorage.getItem("token") as string
            }
        });
        if (response.ok) {
            console.log("ok");
            alert("Profile updated successfully!")
        } else {
            alert("Something went wrong!")
        }
    }
</script>

<div class="flex justify-center items-center h-screen">
    <form on:submit={submit}>
        <Card.Root class="w-[400px]">
            <Card.Header>
                <Card.Title>Edit your profile</Card.Title>
            </Card.Header>
            <Card.Content>
                <div class="grid gap-4 w-full">
                    <div class="flex flex-col space-y-1.5">
                        <Label for="firstname">First Name</Label>
                        <Input id="firstname" name="firstname" placeholder="Enter your firstname" bind:value={data['first_name']} />
                    </div>
                    <div class="flex flex-col space-y-1.5">
                        <Label for="lastname">Last Name</Label>
                        <Input id="lastname" name="lastname" placeholder="Enter your lastname" bind:value={data['last_name']} />
                    </div>
                    <div class="flex flex-col space-y-1.5">
                        <Label for="email">Email</Label>
                        <Input id="email" name="email" type="email" placeholder="Enter a valid email address" bind:value={data['email']} />
                    </div>
                    <div class="flex flex-col space-y-1.5">
                        <Label for="Password">Password</Label>
                        <Input id="password" name="password" type="password" placeholder="********" bind:value={data['password']} />
                    </div>  
                </div>
            </Card.Content>
            <Card.Footer class="flex flex-row justify-between">
                <Button variant="outline" on:click={() => window.location.href = "/"}>Cancel</Button>
                <Button type="submit">Edit</Button>
            </Card.Footer>
        </Card.Root>
    </form>
</div>