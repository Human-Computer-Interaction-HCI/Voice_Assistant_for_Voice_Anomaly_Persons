"use server"

import { getModelInfo as _getModelInfo, ModelInfo, trainModel as _trainModel } from "@/api/model";

export async function getModelInfo(): Promise<ModelInfo> {
    return await _getModelInfo();
}

export async function trainModel(): Promise<void> {
    return await _trainModel();
}
