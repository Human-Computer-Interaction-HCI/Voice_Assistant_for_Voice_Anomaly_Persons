"use server"

import { getDatasetList, DatasetList } from "@/api/datasets"

export async function getDatasets() {
    return await getDatasetList()
}