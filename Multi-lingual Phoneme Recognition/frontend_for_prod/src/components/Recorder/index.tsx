"use client";
import Typography from "@mui/material/Typography";
import RadioButtonCheckedIcon from "@mui/icons-material/RadioButtonChecked";
import React, { useState, useRef } from "react";
import IconButton from "@mui/material/IconButton";
import StopCircleIcon from "@mui/icons-material/StopCircle";
import ReplayCircleIcon from "@mui/icons-material/ReplayCircleFilled";
import Button from "@mui/material/Button";
import { recognizeAction, sendCorrectedText } from "./actions";

enum RecordingState {
  NOT_RECORDED,
  RECORDING,
  RECORDED,
  NEED_MARKUP
}

function getColor(state: RecordingState) {
  switch (state) {
    case RecordingState.NOT_RECORDED:
      return "default";
    case RecordingState.RECORDING:
      return "error";
    case RecordingState.RECORDED:
    case RecordingState.NEED_MARKUP:
      return "success";
  }
}

function Recorder() {
  const [recordingState, setRecordingState] = useState<RecordingState>(
    RecordingState.NOT_RECORDED
  );
  const [icon, setIcon] = useState(<RadioButtonCheckedIcon />);
  const recorder = useRef<MediaRecorder>();
  const chunks = useRef<Blob[]>([]);
  const [recordingURL, setRecordingURL] = useState<string>();
  const fileInput = useRef<HTMLFormElement>(null);
  const [initialText, setInitialText] = useState<string>();
  const [requestId, setRequestId] = useState<string>();
  const correctedText = useRef<HTMLTextAreaElement>(null);

  async function record() {
    switch (recordingState) {
      case RecordingState.NOT_RECORDED:
      case RecordingState.RECORDED:
        let stream = await navigator.mediaDevices.getUserMedia({
          audio: true,
          video: false,
        });
        recorder.current = new MediaRecorder(stream);
        recorder.current.start();
        recorder.current.ondataavailable = (e) => {
          chunks.current.push(e.data);
        };
        recorder.current.onstop = () => {
          let blob = new Blob(chunks.current);
          setRecordingURL(URL.createObjectURL(blob));
        };
        setRecordingState(RecordingState.RECORDING);
        setIcon(<StopCircleIcon />);
        break;
      case RecordingState.RECORDING:
        recorder.current!.stop();
        setRecordingState(RecordingState.RECORDED);
        setIcon(<ReplayCircleIcon />);
        break;
    }
  }

  async function sendForRecognition(form: FormData){
    let result = await recognizeAction(form)
    setInitialText(result.result)
    setRequestId(result.request_id)
    setRecordingState(RecordingState.NEED_MARKUP)
  }

  async function recognize() {
    let blob = new Blob(chunks.current);
    let fd = new FormData()
    fd.append('file', blob, 'smth.webm');
    await sendForRecognition(fd)
  }

  async function recognizeFile() {
    let form = new FormData(fileInput.current!);
    await sendForRecognition(form)
  }

  async function saveText() {
    await sendCorrectedText(requestId!, correctedText.current!.value)
  }

  return (
    <div>
      <Typography variant="h2">Запись звука</Typography>
      <IconButton color={getColor(recordingState)} onClick={record}>
        {icon}
      </IconButton>
      {recordingState == RecordingState.RECORDED ? <>
        <audio src={recordingURL} controls />
        <Button variant="contained" onClick={recognize}>Распознать</Button>
      </> : null}
      <Typography>или</Typography>
      <form ref={fileInput}>
        <input type="file" accept="audio/*" name="file" />
      </form>
      {!initialText&&<Button variant="contained" onClick={recognizeFile}>Распознать</Button>}
      {initialText&&<>
        <Typography>Распознанный текст:</Typography>
        <Typography><em>{initialText}</em></Typography>
        <Typography>Корректный текст</Typography>
        <textarea placeholder="Введите текст" cols={60} rows={3} ref={correctedText}/>
        <br/>
        <Button variant="contained" onClick={saveText}>Сохранить</Button>
      </>}
    </div>
  );
}

export default Recorder;
