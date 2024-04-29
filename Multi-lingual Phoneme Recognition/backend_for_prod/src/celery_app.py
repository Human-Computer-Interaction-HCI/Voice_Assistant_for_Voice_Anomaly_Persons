from ai_utils.dataset import SpeechDataset
from ai_utils.metric_store import MetricStore
from ai_utils.model import Model


def train_model(model_id: int, dataset_list: list[tuple[str, str]], task_id: str):
    model = Model.load(f'data/models/{model_id}')
    metric_store = MetricStore(["epoch", "train_loss", "train_cer", "val_loss", "val_cer"], task_id, lambda: model.save(f'data/models/{model_id}'))

    dataset = SpeechDataset()
    for i, j in dataset_list:
        dataset.add_audio(i, j)

    model.train_on_data(dataset, epochs=100, callback=metric_store.callback)
    
