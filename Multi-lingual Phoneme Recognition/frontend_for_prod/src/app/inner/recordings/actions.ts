"use server"

import { getDatasetList, getDataset as _getDataset } from "@/api/datasets"
import { isAuthenticated } from "@/app/auth/login/actions"

export async function getDatasets() {
    await isAuthenticated(false)
    return await getDatasetList()
}

export async function getDataset(id: string = "default") {
    await isAuthenticated(false)
    return await _getDataset(id)
}
