"use server"

import { axiosInstance } from "@/api"


export type RecognitionResult = {
    result: string,
    request_id: string
}

export async function recognizeAction(fd: FormData): Promise<RecognitionResult> {
    let resp = await axiosInstance.post("predict", fd)
    return resp.data;
}

export async function sendCorrectedText(request_id: string, label: string) {
    let resp = await axiosInstance.post("label", {
        request_id: request_id, label: label
    })
    return resp.data;
}
