'use client'

import { useRef, useState } from "react";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import { login } from "./actions";
import Typography from "@mui/material/Typography";

export default function Page() {
    const [message, setMessage] = useState<string | null>(null);
    let form = useRef<HTMLFormElement>(null);
    async function loginClick() {
        let result = await login(new FormData(form.current!));
        if (result) {

        } else {
            setMessage("Неверный логин или пароль");
        }
    }
    return <>
    <form ref={form}>
        <TextField label="Login" name="username" />
        <br/>
        <TextField label="Password" name="password" type="password" />
        <br/>
        
    </form>
    {message && <Typography color="error">{message}</Typography>}
    <Button type="submit" variant="contained" onClick={loginClick}>Login</Button>
    </>
  }