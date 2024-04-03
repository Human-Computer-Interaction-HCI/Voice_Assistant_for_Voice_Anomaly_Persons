"use server"

import { axiosInstance } from "@/api"
import { checkToken } from "@/api/auth"
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
        axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${resp.data.access_token}`
        return true
    }
    return false
}

export async function isAuthenticated(): Promise<boolean> {
    const token = cookies().get('access_token')
    if (!token) return false
    axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
    return await checkToken()
}
