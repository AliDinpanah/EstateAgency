<script lang="ts">
    import { Button } from "@/components/ui/button";
    import * as Card  from "@/components/ui/card";
    import { Input } from "@/components/ui/input";
    import { Label } from "@/components/ui/label";
    import { Select, SelectValue, SelectTrigger, SelectItem, SelectContent} from "@/components/ui/select";

    let phone: string;
    let password: string;
    let sent: boolean = false;
    let role: string = "user";

    async function login(e: any){
        e.preventDefault();
        const response = await fetch(`http://127.0.0.1:8000/${role}/login`, {
            method: "POST",
            body: JSON.stringify({ "phone": phone + "-" + role, "password": password }),
            headers: {
                "Content-Type": "application/json"
            }
        });
        if (response.ok) {
            console.log("ok");
            const data = await response.json();
            localStorage.setItem("token", data.token);
            if(role == "user") window.location.href = "/user/profile";
            else window.location.href = "/";
        } else {
            alert((response.json() as any)["message"]);
        }
    }

    async function sendCode(event: any) {
        event.preventDefault();
        const response = await fetch("http://127.0.0.1:8000/verification/send-code", {
            method: "POST",
            body: JSON.stringify({ "phone": phone }),
            headers: {
                "Content-Type": "application/json"
            }
        });
        if (response.ok) {
            sent = true;
        } else {
            alert((response.json() as any)["message"]);
        }
    }

    async function verifyCode(event: any) {
        event.preventDefault();
        const response = await fetch("http://127.0.0.1:8000/verification/verify-code", {
            method: "POST",
            body: JSON.stringify({ "phone": phone + "-" + role, "code": password }),
            headers: {
                "Content-Type": "application/json"
            }
        });
        if (response.ok) {
            console.log("ok");
            const data = await response.json();
            localStorage.setItem("token", data.token);
            if(role == "user") window.location.href = "/user/profile";
            else window.location.href = "/";
        } else {
            alert((response.json() as any)["message"]);
        }
    }
</script>


<div class="flex justify-center items-center h-screen">
    <form on:submit={(e) => sent ? verifyCode(e) : login(e)}>
        <Card.Root class="w-[400px]">
            <Card.Header>
                <Card.Title>Sign In</Card.Title>
            </Card.Header>
            <Card.Content>
                <div class="grid gap-4 w-full">
                    <div class="flex flex-col space-y-1.5">
                        <Label for="phone">Phone</Label>
                        <Input id="phone" name="phone" type="text" pattern="^(0|\+98)9[0-9]{'{9}'}" required placeholder="Enter your phone number" bind:value={phone} />
                    </div>
                    <div class="flex flex-col space-y-1.5">
                        <Label for="password">{sent ? "Verification Code" : "Password"}</Label>
                        <Input id="password" name="password" type="password" placeholder={sent ? "Enter the code" : "Enter your password"} bind:value={password} />
                    </div>
                    <div class="flex flex-col space-y-1.5">
                        <Label for="role">Role</Label>
                        <Select onSelectedChange={(e) => {role = typeof e?.value === 'string' ? e?.value : "user"; }}>
                            <SelectTrigger id="role">
                                <SelectValue placeholder="User" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="user">User</SelectItem>
                                <SelectItem value="agency">Agency</SelectItem>
                            </SelectContent>
                        </Select>
                </div>
            </Card.Content>
            <Card.Footer class="flex justify-between">
                <Button on:click={sendCode} variant="outline" disabled={sent}>Send Code</Button>
                <Button type="submit">Login</Button>
            </Card.Footer>
        </Card.Root>
    </form>
</div>