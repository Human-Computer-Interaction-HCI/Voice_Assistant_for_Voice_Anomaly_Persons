import { axiosInstance } from ".";

export type UserDataset = {
    label: string
}

export type DatasetList = {
    datasets: UserDataset[]
}

export type DatasetRecording = {
    dataset_id: number
    label?: string
    recording_id: string
}

export type UserDatasetContent = {
    recordings: DatasetRecording[]
}

export async function getDatasetList(): Promise<DatasetList> {
    const response = await axiosInstance.get<DatasetList>('/datasets/list');
    return response.data;

}

export async function getDataset(datasetLabel: string = "default"): Promise<DatasetRecording[]> {
    const response = await axiosInstance.get<UserDatasetContent>(`/datasets/ds`, { params: { label: datasetLabel } });
    return response.data.recordings
}
