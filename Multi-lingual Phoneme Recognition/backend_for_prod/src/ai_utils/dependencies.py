from ai_utils.dataset import SpeechDataset
from ai_utils.model import Model


def get_model() -> Model:
    model = Model()
    model.eval()
    return model

def get_dataset() -> SpeechDataset:
    dataset = SpeechDataset()
    return dataset

