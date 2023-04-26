'use client'

import React, { useRef, useState } from 'react'

function RecordPage() {
  const [recordingInProgress, setRecordingInProgress] = useState(false)
  const [audioRecorded, setAudioRecorded] = useState<string>()
  const mediaRecorder = useRef<MediaRecorder>()

  async function startRecording() {
    const stream = await navigator
    .mediaDevices
    .getUserMedia({
      audio: true,
      video: false
    })

    mediaRecorder.current = new MediaRecorder(stream)
    let chunks: Blob[] = []
    mediaRecorder.current.start()
    setRecordingInProgress(true)
    
    mediaRecorder.current.ondataavailable = e => chunks.push(e.data)
    mediaRecorder.current.onstop = () => setAudioRecorded(URL.createObjectURL(new Blob(chunks)))
  }
  function stopRecording() {
    mediaRecorder.current!.stop()
    setRecordingInProgress(false)
  }

  return (
    <div>
      <h2>Запишите аудио для распознавания</h2>
      {audioRecorded && <audio src={audioRecorded} controls />}
      {recordingInProgress ? <button onClick={stopRecording}>Остановить</button> : <button onClick={startRecording}>Начать</button>}
    </div>
  )
}

export default RecordPage