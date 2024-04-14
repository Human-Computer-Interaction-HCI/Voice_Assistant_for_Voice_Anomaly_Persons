import { axiosInstance } from "."
import { RecognitionResult } from "./types"

export type ModelInfo = {
    id: number
}

export async function getModelInfo(): Promise<ModelInfo> {
    const response = await axiosInstance.get<ModelInfo>("/model/info")
    return response.data

}

export async function recognizeAudioById(requestId: string): Promise<string | undefined> {
    const response = await axiosInstance.get<RecognitionResult>('/predict', { 'params': { 'request_id': requestId } })
    return response.data.result
}

export async function trainModel() {
    await axiosInstance.post('/model/train')    
}
