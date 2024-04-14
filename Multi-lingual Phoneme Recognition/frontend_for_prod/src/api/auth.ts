import { axiosInstance } from ".";

export async function getAuthInfo() {
    return await axiosInstance.get('/auth/me')
}

export async function checkToken() {
    try {
        await axiosInstance.get('/auth/me')
        return true
    } catch (e) {
        return false
    }
}