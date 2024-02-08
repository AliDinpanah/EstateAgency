<script lang="ts">
    import { Button } from "@/components/ui/button";
    import * as Card from "@/components/ui/card";
    import { Input } from "@/components/ui/input";
    import { Label } from "@/components/ui/label";
    import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

    let sent: boolean = false;
    let verified: boolean = false;
    let data: any = {}

    async function verifyPhone(event: any) {
        event.preventDefault();
        const response = await fetch("http://127.0.0.1:8000/verification/send-code", {
            method: "POST",
            body: JSON.stringify({ "phone": data['admin-phone'] + "-agency" }),
            headers: {
                "Content-Type": "application/json"
            }
        });
        if (response.ok) {
            sent = true;
        }
    }

    async function verifyCode(event: any) {
        event.preventDefault();
        const response = await fetch("http://127.0.0.1:8000/verification/verify-code", {
            method: "POST",
            body: JSON.stringify({ "phone": data['admin-phone'] + "-agency", "code": data['code']}),
            headers: {
                "Content-Type": "application/json"
            }
        });
        if (response.ok) {
            console.log("ok");
            const data = await response.json();
            localStorage.setItem("token", data.token);
            verified = true;
            register(event);
        } else {
            alert("Verification failed!")
        }
    }

    async function register(event: any) {
        event.preventDefault();
        const response = await fetch("http://127.0.0.1:8000/agency/register", {
            method: "POST",
            body: JSON.stringify({
                "name": data['name'],
                "phone": data['phone'],
                "city": data['city'],
                "employees_count": data['employees-count'],
                "admin_firstname": data['admin-firstname'],
                "admin_lastname": data['admin-lastname'],
                "admin_password": data['admin-password']
            }),
            headers: {
                "Content-Type": "application/json",
                "X-Auth-Token": localStorage.getItem("token") as string
            }
        });

        if (response.ok) {
            console.log("ok");
            alert("Agency registered successfully!")
            window.location.href = "/";
            // TODO: redirect to dashboard
        } else {
            alert("Something went wrong!")
        }
    }

</script>

<div class="flex justify-center items-center h-screen">
    <form on:submit={(e) => sent ? (verified ? register(e): verifyCode(e)) : verifyPhone(e)}>
        <Card.Root class="w-[600px]">
            <Card.Header>
                <Card.Title tag="h1" class="text-2xl font-semibold">Register Agency</Card.Title>
                <Card.Description>Register your agency in 5 minutes!</Card.Description>
            </Card.Header>
            <Card.Content>
                <div class="flex w-full items-start gap-4">
                    <div class="flex-col grid gap-4 w-full">
                        <h2 class="font-bold">Agency Information</h2>
                        <div class="flex flex-col space-y-1.5">
                            <Label for="name">Name</Label>
                            <Input id="name" name="name" placeholder="Name of your agency" bind:value={data['name']} />
                        </div>
                        <div class="flex flex-col space-y-1.5">
                            <Label for="phone">Phone</Label>
                            <Input id="phone" name="phone" type="text" pattern="^(0|\+98)\d+" placeholder="Agency Phone Number"  bind:value={data['phone']} />
                        </div>
                        <div class="flex flex-col space-y-1.5">
                            <Label for="city">City</Label>
                            <Input id="city" name="city" placeholder="Working City" bind:value={data['city']}/>
                        </div>
                        <div class="flex flex-col space-y-1.5">
                            <Label for="numberOfEmployees">Number of Employees</Label>
                            <Select onSelectedChange={(e) => {data['employees-count'] = e?.value;}}>
                                <SelectTrigger id="numberOfEmployees">
                                    <SelectValue placeholder="Select" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="5">Up to 5</SelectItem>
                                    <SelectItem value="10">6 to 10</SelectItem>
                                    <SelectItem value="20">11 to 20</SelectItem>
                                    <SelectItem value="100">More than 20</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>
                    </div>

                    <div class="flex-col grid gap-4 w-full">
                        <h2 class="font-bold">Admin Information</h2>
                        <div class="flex flex-col space-y-1.5">
                            <Label for="firstname">First Name</Label>
                            <Input id="firstname" name="firstname" placeholder="Admin's First Name" bind:value={data['admin-firstname']} />
                        </div>
                        <div class="flex flex-col space-y-1.5">
                            <Label for="lastname">Last Name</Label>
                            <Input id="lastname" name="lastname" placeholder="Admin's Last Name" bind:value={data['admin-lastname']} />
                        </div>
                        <div class="flex flex-col space-y-1.5">
                            {#if sent}
                                <Label for="code">Code</Label>
                                <Input id="code" name="code" placeholder="Code" bind:value={data['code']} />
                            {:else}
                            <Label for="phoneNumber">Phone number</Label>
                            <Input id="phoneNumber" name="phoneNumber" pattern="^(0|\+98)9[0-9]{'{9}'}" placeholder="0912xxx2351" bind:value={data['admin-phone']} />
                            {/if}
                        </div>
                        <div class="flex flex-col space-y-1.5">
                            <Label for="password">Password</Label>
                            <Input id="password" type="password" name="password" placeholder="Enter your password" bind:value={data['admin-password']} />
                        </div>
                    </div>
                </div>
            </Card.Content>
            <Card.Footer class="flex justify-between">
                <Button variant="outline" on:click={(e) => {window.location.href = "/"}}>Cancel</Button>
                <Button type="submit">{sent ? "Register" : "Send Code" }</Button>
            </Card.Footer>
        </Card.Root>
    </form>
</div>
