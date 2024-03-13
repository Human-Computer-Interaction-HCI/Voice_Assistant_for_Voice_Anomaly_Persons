"use server"

import { axiosInstance } from "@/api"
import { cookies } from "next/headers"

type TokenPair = {
    access_token: string
    refresh_token: string
}

export async function login(fd: FormData): Promise<boolean> {
    let resp = await axiosInstance.post<TokenPair>("/auth/token", fd)
    if (resp.status === 200) {
        cookies().set({
            name: 'access_token', value: resp.data.access_token, httpOnly: true, secure: true
        })
        cookies().set({
            name: 'refresh_token', value: resp.data.refresh_token, httpOnly: true, secure: true
        })
        return true
    }
    return false
}

export async function isAuthenticated(): Promise<boolean> {
    return cookies().get('access_token')!== undefined
}
