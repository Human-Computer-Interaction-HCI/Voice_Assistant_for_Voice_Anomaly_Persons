import { axiosInstance } from ".";

export type UserDataset = {
    label: string
}

export type DatasetList = {
    datasets: UserDataset[]
}

export async function getDatasetList(): Promise<DatasetList> {
    const response = await axiosInstance.get<DatasetList>('/datasets/list');
    return response.data;

}
