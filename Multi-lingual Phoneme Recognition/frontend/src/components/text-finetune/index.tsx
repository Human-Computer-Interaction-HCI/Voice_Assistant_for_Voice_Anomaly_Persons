'use client';

import { useState } from "react";

export type FineTuneProps = {
    phonemes: string
}

export default function TextFinetune({ phonemes }: FineTuneProps) {
    const [text, setText] = useState("")
    function fineTune() {
        // DefaultService.fineTuneRecognizeFineTunePost({
        //     phonemes: phonemes,
        //     text: text
        // })
    }
    return <>
        <p>Введите правильный текст: <input value={text} onChange={e => setText(e.target.value)} /></p>
        <button onClick={fineTune}>Сохранить</button>
    </>;
}
