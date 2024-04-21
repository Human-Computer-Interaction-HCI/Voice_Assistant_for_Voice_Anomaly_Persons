"use server"

import { getModelInfo as _getModelInfo, ModelInfo, trainModel as _trainModel, ModelTrainInfo } from "@/api/model";

export async function getModelInfo(): Promise<ModelInfo> {
    return await _getModelInfo();
}

export async function trainModel(): Promise<ModelTrainInfo> {
    return await _trainModel();
}
