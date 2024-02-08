<script lang="ts">
    import { Button } from "@/components/ui/button";
    import * as Card  from "@/components/ui/card";
    import { Input } from "@/components/ui/input";
    import { Label } from "@/components/ui/label";

    let phone = "";
    let code = "";
    let sent = false;


    async function verifyPhone(event: any) {
        event.preventDefault();
        const response = await fetch("http://127.0.0.1:8000/verification/send-code", {
            method: "POST",
            body: JSON.stringify({ "phone": phone + "-user" }),
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
            body: JSON.stringify({ "phone": phone + "-user", code }),
            headers: {
                "Content-Type": "application/json"
            }
        });
        if (response.ok) {
            console.log("ok");
            const data = await response.json();
            localStorage.setItem("token", data.token);
            register(event);
        }
    }

    async function register(event: any) {
        event.preventDefault();
        const response = await fetch("http://127.0.0.1:8000/user/register", {
            method: "POST",
            // body: JSON.stringify({ "token": localStorage.getItem("token") }),
            headers: {
                "Content-Type": "application/json",
                "X-Auth-Token": localStorage.getItem("token") as string
            }
        });
        if (response.ok) {
            console.log("ok");
            const data = await response.json();
            // redirect to profile page
            window.location.href = "/user/profile";
        } else {
            alert((response.json() as any)["message"]);
        }
    }
</script>

<div class="flex justify-center items-center h-screen">
    <form on:submit={(e) => sent ? verifyCode(e) : verifyPhone(e)}>
        <Card.Root class="w-[400px]">
            <Card.Header>
                <Card.Title>Sign Up</Card.Title>
                <Card.Description>Create your account and start today!</Card.Description>
            </Card.Header>
            <Card.Content>
                <div class="grid gap-4 w-full">
                    <div class="flex flex-col space-y-1.5">
                        <Label for="phone">{sent ? "Verification code" : "Phone"}</Label>
                        {#if sent}
                            <Input id="code" name="code" type="number" required placeholder="Enter the verification code" bind:value={code} />
                        {:else}
                            <Input id="phone" name="phone" pattern="^(0|\+98)9[0-9]{'{9}'}" required type="text" placeholder="Enter your number" bind:value={phone} />
                        {/if}
                    </div>
                </div>
            </Card.Content>
            <Card.Footer>
                <Button type="submit">{sent ? "Verify Code" : "Send Code"}</Button>
            </Card.Footer>
        </Card.Root>
    </form>
</div>
