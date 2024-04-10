"use server"

import { getModelInfo as _getModelInfo, ModelInfo } from "@/api/model";

export async function getModelInfo(): Promise<ModelInfo> {
    return await _getModelInfo();
}