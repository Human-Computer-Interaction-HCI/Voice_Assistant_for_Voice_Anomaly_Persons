"use server"

import { getModelInfo as _getModelInfo, ModelInfo, trainModel as _trainModel, ModelTrainInfo, getModelMetrics as _getModelMetrics } from "@/api/model";

export async function getModelInfo(): Promise<ModelInfo> {
    return await _getModelInfo();
}

export async function trainModel(): Promise<ModelTrainInfo> {
    return await _trainModel();
}

export async function getModelMetrics(task_id: string): Promise<any> {
    return await _getModelMetrics(task_id);
}
