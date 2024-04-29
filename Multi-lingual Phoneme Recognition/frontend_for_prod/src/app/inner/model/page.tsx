"use client"
import Typography from "@mui/material/Typography";
import { getModelInfo, trainModel, getModelMetrics } from "./actions"
import { useEffect, useState } from "react";
import { ModelInfo } from "@/api/model";
import Card from "@mui/material/Card";
import CardHeader from "@mui/material/CardHeader";
import CardContent from "@mui/material/CardContent";
import CardActions from "@mui/material/CardActions";
import { Button } from "@mui/material";
import MetricPlot from "@/components/MetricPlot";

export default function Page() {
    const [modelInfo, setModelInfo] = useState<ModelInfo>()
    const [taskId, setTaskId] = useState<string>()
    const [training, setTraining] = useState(false)

    useEffect(() => {
        getModelInfo().then(setModelInfo)
    }, [])

    function startTrain() {
        trainModel().then(r=>setTaskId(r.task_id))
        setTraining(true)
    }

    return <>
        <Typography variant="h1">Моя модель</Typography>
        <Card sx={{ width: "fit-content" }}>
            <CardHeader title={`Модель ${modelInfo?.id}`} />
            <CardContent>
                <Typography>Метрики</Typography>
                {taskId&&<MetricPlot taskId={taskId} refresh={()=>getModelMetrics(taskId)} />}
            </CardContent>
            <CardActions>
                {!training&&<Button size="small" onClick={startTrain}>Запустить обучение</Button>}
            </CardActions>
        </Card>
    </>
}