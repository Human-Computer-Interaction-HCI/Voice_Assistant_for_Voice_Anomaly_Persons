"use client";

import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import { useRouter } from "next/navigation";
import { useRef, useState } from "react";
import { register } from "./actions";

export default function Page() {
    const [message, setMessage] = useState<string | null>(null);
    const router = useRouter()
    const form = useRef<HTMLFormElement>(null)

    async function registerClick() {
        let result = await register(new FormData(form.current!))
        if (result) {
            router.push("/")
        } else {
            setMessage("Пользователь с таким именем уже существует")
        }
    }

    return <Box sx={{
        margin: 'auto',
        width: 'fit-content',
    }}>
        <Typography variant="h1">Регистрация</Typography>
        <form ref={form}>
            <TextField name="login" label="Логин" /><br />
            <TextField name="password" label="Пароль" type="password" /><br />
        </form>
        {message && <Typography color="error">{message}</Typography>}
        <Button type="submit" onClick={registerClick}>Регистрация</Button>
    </Box>
}