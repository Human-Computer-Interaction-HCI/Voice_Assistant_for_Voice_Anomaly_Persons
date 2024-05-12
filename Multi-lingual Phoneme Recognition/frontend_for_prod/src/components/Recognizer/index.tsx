"use client";
import Typography from "@mui/material/Typography";
import RadioButtonCheckedIcon from "@mui/icons-material/RadioButtonChecked";
import React, { useState, useRef } from "react";
import StopCircleIcon from "@mui/icons-material/StopCircle";
import ReplayCircleIcon from "@mui/icons-material/ReplayCircleFilled";
import Button from "@mui/material/Button";
import { recognizeAction } from "./actions";

enum RecordingState {
  NOT_RECORDED,
  RECORDING,
  RECORDED,
}

function getColor(state: RecordingState) {
  switch (state) {
    case RecordingState.NOT_RECORDED:
      return "primary";
    case RecordingState.RECORDING:
      return "error";
    case RecordingState.RECORDED:
      return "success";
  }
}

function getText(state: RecordingState) {
  switch (state) {
    case RecordingState.NOT_RECORDED:
      return "Записать";
    case RecordingState.RECORDING:
      return "Остановить";
    case RecordingState.RECORDED:
      return "Записать";
  }
}

function Recognizer() {
  const [recordingState, setRecordingState] = useState<RecordingState>(
    RecordingState.NOT_RECORDED
  );
  const [icon, setIcon] = useState(<RadioButtonCheckedIcon />);
  const recorder = useRef<MediaRecorder>();
  const chunks = useRef<Blob[]>([]);
  const [recordingURL, setRecordingURL] = useState<string>();
  const [recognizedText, setRecognizedText] = useState<string>();

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
          console.log('new data available')
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

  async function sendForRecognition(form: FormData) {
    let result = await recognizeAction(form)
    setRecognizedText(result.result)
    setRecordingState(RecordingState.NOT_RECORDED)
  }

  async function recognize() {
    let blob = new Blob(chunks.current);
    let fd = new FormData()
    fd.append('file', blob, 'smth.webm');
    await sendForRecognition(fd)
  }

  return (
    <div>
      <Button variant="contained" color={getColor(recordingState)} onClick={record} startIcon={icon}>{getText(recordingState)}</Button><br />
      {recordingState == RecordingState.RECORDED ? <>
        <audio src={recordingURL} controls /><br />
        <Button variant="contained" onClick={recognize}>Распознать</Button><br />
      </> : null}
      {recognizedText && <>
        <Typography>Распознанный текст:</Typography>
        <Typography><em>{recognizedText}</em></Typography>
      </>}
    </div>
  );
}

export default Recognizer;
