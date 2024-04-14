"use server"

import { axiosInstance } from "@/api";
import { login } from "../login/actions";

export async function register(fd: FormData): Promise<boolean> {
    const resp = await axiosInstance.post("/auth/register", {
        "login": fd.get("login"), "password": fd.get("password")
    });
    if (resp.status == 200) {
        fd.set("username", fd.get("login") as string)
        fd.delete("login")
        console.debug(fd)
        await login(fd)
        return true
    }
    return false
}