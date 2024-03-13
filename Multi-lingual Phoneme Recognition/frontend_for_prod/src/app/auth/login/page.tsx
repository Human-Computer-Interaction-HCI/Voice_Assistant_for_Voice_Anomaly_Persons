'use client'

import { useRef, useState } from "react";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import { login } from "./actions";
import Typography from "@mui/material/Typography";
import { useRouter } from "next/navigation";
import Box from "@mui/material/Box";

export default function Page() {
    const [message, setMessage] = useState<string | null>(null);
    const router = useRouter();
    let form = useRef<HTMLFormElement>(null);
    async function loginClick() {
        let result = await login(new FormData(form.current!));
        if (result) {
            router.push('/')
        } else {
            setMessage("Неверный логин или пароль");
        }
    }
    return <Box sx={{
        margin: 'auto',
        width: 'fit-content'
    }}>
        <Typography variant="h1">Вход</Typography>
    <form ref={form}>
        <TextField label="Login" name="username" />
        <br/>
        <TextField label="Password" name="password" type="password" />
        <br/>
        
    </form>
    {message && <Typography color="error">{message}</Typography>}
    <Button type="submit" variant="contained" onClick={loginClick}>Login</Button>
    </Box>
  }