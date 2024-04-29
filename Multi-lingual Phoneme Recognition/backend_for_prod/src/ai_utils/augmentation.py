import random
import torch
import torchaudio


effects = [
    ",".join(
        [
            "lowpass=frequency=300:poles=1",  # apply single-pole lowpass filter
            "atempo=1.2",  # reduce the speed
            "aecho=in_gain=0.8:out_gain=0.9:delays=200:decays=0.3|delays=400:decays=0.3",
            # Applying echo gives some dramatic feeling
        ],
    ),
]


def apply_effect(waveform, sample_rate, effect):
    effector = torchaudio.io.AudioEffector(
        effect=effect,
        format="wav",
    )
    return effector.apply(waveform, sample_rate)


cache = dict()

def augment_audio(audio: torch.Tensor, idx):
    if len(cache) > 2000:
        del cache[random.choice(list(cache.keys()))]
    efn = random.choices([0, 1, 2],[0.5, 0.3, 0.2])[0]
    if (idx, efn) in cache:
        cache[(idx, efn)] = (cache[(idx, efn)][0], cache[(idx, efn)][1]+1)
        return cache[(idx, efn)][0]
                
    match efn:
        case 0:
            cache[(idx, efn)] = (audio, 0)
        case 1:
            audio += torch.rand(audio.shape) * 0.1
            cache[(idx, efn)] =  (audio, 0)
        case 2:
            cache[(idx, efn)] =  (apply_effect(audio.T, 16000, random.choice(effects)).T, 0)
        case 3:
            cache[(idx, efn)] =  (torchaudio.functional.pitch_shift(
                audio, 16000, random.randint(-3, 3)
            ), 0)
    return cache[(idx, efn)][0]
