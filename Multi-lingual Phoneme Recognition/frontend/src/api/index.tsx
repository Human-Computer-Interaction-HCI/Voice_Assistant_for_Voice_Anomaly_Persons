import axios from "axios"
import { ResultResponse } from "./types"

const axiosInstance = axios.create({
    baseURL: 'http://localhost:8000'
})

export async function recognizePhonemes(file: Blob): Promise<ResultResponse> {
    const fd = new FormData()
    fd.append("file", file, "record.webm")
    return (await axiosInstance.post('/recognize/phonemes', fd)).data
}