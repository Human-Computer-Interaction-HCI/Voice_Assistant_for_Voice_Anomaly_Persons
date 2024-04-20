class MetricStore:
    history: dict[str, list[float | str]]
    def __init__(self, metrics: list[str]) -> None:
        self.history = {i: [] for i in metrics}
    
    def callback(self, metric: str, value: float | str) -> None:
        self.history[metric].append(value)
                