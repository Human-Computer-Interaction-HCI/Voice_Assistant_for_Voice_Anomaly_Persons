"use server"

import { axiosInstance } from "@/api"
import { RecognitionResult } from "../../api/types"
import { isAuthenticated } from "@/app/auth/login/actions"


export async function recognizeAction(fd: FormData): Promise<RecognitionResult> {
    await isAuthenticated(false)
    let resp = await axiosInstance.post("predict_no_save", fd)
    return resp.data;
}