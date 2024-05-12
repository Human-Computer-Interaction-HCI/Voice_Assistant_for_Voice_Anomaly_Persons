"use client"
import Typography from "@mui/material/Typography";
import { getModelInfo, trainModel, getModelMetrics, getCurrentMetrics } from "./actions"
import { useEffect, useState } from "react";
import { ModelInfo, ModelMetrics } from "@/api/model";
import Card from "@mui/material/Card";
import CardHeader from "@mui/material/CardHeader";
import CardContent from "@mui/material/CardContent";
import CardActions from "@mui/material/CardActions";
import MetricPlot from "@/components/MetricPlot";
import Recognizer from "@/components/Recognizer";
import Button from "@mui/material/Button";
import CircularProgress from "@mui/material/CircularProgress";

export default function Page() {
    const [modelInfo, setModelInfo] = useState<ModelInfo>()
    const [taskId, setTaskId] = useState<string>()
    const [training, setTraining] = useState(false)
    const [modelMetrics, setModelMetrics] = useState<ModelMetrics>()
    const [modelMetricsState, setModelMetricsState] = useState<number>(0)

    useEffect(() => {
        getModelInfo().then(setModelInfo)
    }, [])

    function calculateMetrics() {
        setModelMetricsState(1)
        getCurrentMetrics().then(r => {
            setModelMetrics(r)
            setModelMetricsState(2)
        })
    }

    function startTrain() {
        trainModel().then(r => setTaskId(r.task_id))
        setTraining(true)
    }

    return <>
        <Typography variant="h1">Моя модель</Typography>

        <Card sx={{ width: "fit-content" }}>
            <CardHeader title="Распознавание" />
            <CardContent><Recognizer /></CardContent>
        </Card>
        <Card sx={{ width: "fit-content" }}>
            <CardHeader title={`Модель ${modelInfo?.id}`} />
            <CardContent>
                <Typography>Метрики</Typography>
                {modelMetrics && <div>
                    <p>CER: {modelMetrics.cer}</p>
                    <p>loss: {modelMetrics.loss}</p>
                </div>}
                {modelMetricsState == 0 && <Button size="small" onClick={calculateMetrics} variant="contained" color="secondary">Подсчитать метрики</Button>}
                {modelMetricsState == 1 && <CircularProgress />}
                <div>
                    {taskId && <MetricPlot taskId={taskId} refresh={() => getModelMetrics(taskId)} />}
                </div>
            </CardContent>
            <CardActions>
                {!training && <Button size="small" onClick={startTrain} variant="contained">Запустить обучение</Button>}
            </CardActions>
        </Card>
    </>
}