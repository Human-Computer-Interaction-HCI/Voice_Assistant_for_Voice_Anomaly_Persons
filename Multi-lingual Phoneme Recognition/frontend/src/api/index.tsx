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

export async function fineTune(text: string, phonemes: string) {
    return (await axiosInstance.post('/recognize/fine_tune', {
        text: text, phonemes: phonemes
    })).data
}

export async function phonemesToText(phonemes: string) {
    return (await axiosInstance.post('/recognize/phonemes_to_text', {
        phonemes: phonemes
    })).data
}
