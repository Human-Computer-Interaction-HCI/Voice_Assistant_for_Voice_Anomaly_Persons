import os


class MetricStore:
    current_value: dict[str, float | str | None]
    task_id: str
    fp: str

    def __init__(self, metrics: list[str], task_id: str) -> None:
        self.current_value = {i: None for i in metrics}
        self.task_id = task_id
        if not os.path.exists("data/metrics"):
            os.makedirs("data/metrics")
        self.fp = f"data/metrics/{task_id}.csv"
        if not os.path.exists(self.fp):
            with open(self.fp, "w") as f:
                f.write(",".join(metrics) + "\n")
                f.flush()

    def callback(self, metric: str, value: float | str) -> None:
        print(metric, value)
        self.current_value[metric] = value
        if None not in self.current_value.values():
            with open(self.fp, "a+") as f:
                f.write(",".join([str(i) for i in self.current_value.values()]) + "\n")
            self.current_value = {i: None for i in self.current_value}

    def get_metrics(self) -> str:
        with open(self.fp, "r+") as f:
            return f.read()
