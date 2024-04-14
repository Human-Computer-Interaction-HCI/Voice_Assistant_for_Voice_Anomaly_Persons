"use server"

import { axiosInstance } from "@/api"
import { recognizeAudioById } from "@/api/model"

export async function getLabel(recordingId: string) {
    return await recognizeAudioById(recordingId)
}