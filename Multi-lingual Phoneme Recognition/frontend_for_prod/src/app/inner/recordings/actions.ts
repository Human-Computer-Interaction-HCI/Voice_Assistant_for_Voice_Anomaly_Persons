"use server"

import { getDatasetList, getDataset as _getDataset } from "@/api/datasets"

export async function getDatasets() {
    return await getDatasetList()
}

export async function getDataset(id: string = "default") {
    return await _getDataset(id)
}
