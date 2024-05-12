"use server"

import { getModelInfo as _getModelInfo, ModelInfo, trainModel as _trainModel, ModelTrainInfo, getModelMetrics as _getModelMetrics, ModelMetrics, getCurrentMetrics as _getCurrentMetrics } from "@/api/model";
import { isAuthenticated } from "@/app/auth/login/actions";

export async function getModelInfo(): Promise<ModelInfo> {
    await isAuthenticated(false)
    return await _getModelInfo();
}

export async function trainModel(): Promise<ModelTrainInfo> {
    await isAuthenticated(false)
    return await _trainModel();
}

export async function getModelMetrics(task_id: string): Promise<any> {
    await isAuthenticated(false)
    return await _getModelMetrics(task_id);
}

export async function getCurrentMetrics(): Promise<ModelMetrics> {
    await isAuthenticated(false)
    return await _getCurrentMetrics()
}
