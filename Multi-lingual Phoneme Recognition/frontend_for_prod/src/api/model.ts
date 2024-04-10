import { axiosInstance } from "."

export type ModelInfo = {
    id: number
}

export async function getModelInfo(): Promise<ModelInfo> {
    const response = await axiosInstance.get<ModelInfo>("/model/info")
    return response.data

}