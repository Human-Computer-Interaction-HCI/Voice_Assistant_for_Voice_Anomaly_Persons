import { axiosInstance } from "."
import { RecognitionResult } from "./types"

export type ModelInfo = {
    id: number
}

export type ModelTrainInfo = {
    task_id: string
}

export async function getModelInfo(): Promise<ModelInfo> {
    const response = await axiosInstance.get<ModelInfo>("/model/info")
    return response.data

}

export async function recognizeAudioById(requestId: string): Promise<string | undefined> {
    const response = await axiosInstance.get<RecognitionResult>('/predict', { 'params': { 'request_id': requestId } })
    return response.data.result
}

export async function trainModel() : Promise<ModelTrainInfo>{
    const resp = await axiosInstance.post<ModelTrainInfo>('/model/train')    
    return resp.data
}

export async function getModelMetrics(task_id: string): Promise<string[][]> {
    const response = await axiosInstance.get<string>('/model/metrics', { 'params': { 'task_id': task_id } })
    return response.data.split("\n").map(x => x.split(","))
}
