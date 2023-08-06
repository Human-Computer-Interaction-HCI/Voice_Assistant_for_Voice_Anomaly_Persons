'use client';

import { fineTune } from "@/api";
import { useState } from "react";

export type FineTuneProps = {
    phonemes: string
}

export default function TextFinetune({ phonemes }: FineTuneProps) {
    const [text, setText] = useState("")
    function _fineTune() {
        fineTune(text, phonemes)
        // DefaultService.fineTuneRecognizeFineTunePost({
        //     phonemes: phonemes,
        //     text: text
        // })
    }
    return <>
        <p>Введите правильный текст: <input value={text} onChange={e => setText(e.target.value)} /></p>
        <button onClick={_fineTune}>Сохранить</button>
    </>;
}
