"use client"
import { useEffect, useState } from "react";
import Plot from "react-plotly.js";

type MetricPlotProps = {
    taskId: string
    refresh: () => Promise<string[][]>
}

export default function MetricPlot(
    { taskId, refresh }: MetricPlotProps
) {
    const [metrics, setMetrics] = useState<string[][]>([])
    useEffect(() => {
        const intervalId = setInterval(() => {
            refresh().then(r => {
                r.shift()
                setMetrics(r)
            })
        }, 1000)
        return () => { clearInterval(intervalId) }
    }, [refresh, taskId])
    let batches = getBatches(metrics)
    return <>
        <Plot
            data={[
                {
                    x: batches,
                    y: getLosses(metrics, 1),
                    type: 'scatter',
                    mode: 'lines+markers',
                    marker: { color: 'red' },
                    name: 'train_loss'
                },
                {
                    x: batches,
                    y: getLosses(metrics, 2),
                    type: 'scatter',
                    mode: 'lines+markers',
                    marker: { color: 'green' },
                    name: 'test_loss'
                },
            ]}
            layout={{ title: "Функция потерь" }}
        />
        <Plot
            data={[
                {
                    x: batches,
                    y: getLosses(metrics, 3),
                    type: 'scatter',
                    mode: 'lines+markers',
                    marker: { color: 'red' },
                    name: 'train cer'
                },
                {
                    x: batches,
                    y: getLosses(metrics, 4),
                    type: 'scatter',
                    mode: 'lines+markers',
                    marker: { color: 'green' },
                    name: 'test cer'
                },
            ]}
            layout={{ title: "Растояние Левенштейна" }}
        />
    </>
}

function getBatches(metrics: string[][]) {
    let batches = []
    for (let i = 0; i < metrics.length; i++) {
        batches.push(i)
    }
    return batches
}

function getLosses(metrics: string[][], idx: number, smooth: boolean = true) {
    let losses = []
    let epoch = null
    let k = 0
    let acc = 0
    for (let i = 0; i < metrics.length; i++) {
        if (metrics[i][2] != epoch) {
            epoch = metrics[i][2]
            losses.push(parseFloat(metrics[i][idx]))
            losses[losses.length - 1] = acc / k
            k = 0
            acc = 0
        }
        k++
        acc += parseFloat(metrics[i][idx])
        losses[losses.length - 1] = acc / k
    }
    return losses
}