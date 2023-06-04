'use client'

import { DefaultService } from '@/client'
import TextFinetune from '@/components/text-finetune'
import { useEffect, useRef, useState } from 'react'

function RecordPage() {
  const [recordingInProgress, setRecordingInProgress] = useState(false)
  const [audioRecorded, setAudioRecorded] = useState<Blob>()
  const [recognizedPhonemes, setRecognnizedPhonemes] = useState("")
  const [recognizedText, setRecognizedText] = useState("")

  const mediaRecorder = useRef<MediaRecorder>()

  async function startRecording() {
    const stream = await navigator
      .mediaDevices
      .getUserMedia({
        audio: true,
        video: false
      })

    mediaRecorder.current = new MediaRecorder(stream, {
      mimeType: 'audio/webm'
    })
    let chunks: Blob[] = []
    mediaRecorder.current.start()
    setRecordingInProgress(true)

    mediaRecorder.current.ondataavailable = e => chunks.push(e.data)
    mediaRecorder.current.onstop = () => setAudioRecorded(new Blob(chunks, {type: 'audio/webm'}))
  }
  function stopRecording() {
    mediaRecorder.current!.stop()
    setRecordingInProgress(false)
  }
  function recognize() {
    DefaultService
      .recognizePhonemesRecognizePhonemesPost({ file: audioRecorded! })
      .then(r => {
          DefaultService
      .recognizeRecognizePhonemeToTextPost({ phonemes: recognizedPhonemes }).then(r => setRecognizedText(r.result))
        setRecognnizedPhonemes(r.result)
      })
  }

  // useEffect(() => {
  //   if (recognizedPhonemes.length==0) return
    
  //     
  // }, [recognizedPhonemes, setRecognnizedPhonemes])

  return (
    <div>
      <h2>Запишите аудио для распознавания</h2>
      {audioRecorded && <audio src={URL.createObjectURL(audioRecorded)} controls />}
      {recordingInProgress ? <button onClick={stopRecording}>Остановить</button> : <button onClick={startRecording}>Начать</button>}
      {audioRecorded && <button onClick={recognize}>Распознать</button>}
      <p>Распознанные фонемы: <i>{recognizedPhonemes}</i></p>
      <p>Распознанный текст: <i>{recognizedText}</i></p>
      <TextFinetune phonemes={recognizedPhonemes}/>
    </div>
  )
}

export default RecordPage