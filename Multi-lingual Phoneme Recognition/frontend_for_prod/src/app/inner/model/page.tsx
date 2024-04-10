"use client"
import Typography from "@mui/material/Typography";
import {getModelInfo} from "./actions"
import { useEffect, useState } from "react";
import { ModelInfo } from "@/api/model";
import Card from "@mui/material/Card";
import CardHeader from "@mui/material/CardHeader";
import CardContent from "@mui/material/CardContent";
import CardActions from "@mui/material/CardActions";
import { Button } from "@mui/material";

export default function Page() {
    const [modelInfo, setModelInfo] = useState<ModelInfo>()

    useEffect(() => {
        getModelInfo().then(setModelInfo)
    }, [])

    return <>
        <Typography variant="h1">Моя модель</Typography>
        <Card sx={{width: "fit-content", maxWidth: "300px"}}>
            <CardHeader title={`Модель ${modelInfo?.id}`}/>
            <CardContent>
                <Typography>Метрики</Typography>
            </CardContent>
            <CardActions>
                <Button size="small">Запустить обучение</Button>
            </CardActions>
        </Card>
    </>
}