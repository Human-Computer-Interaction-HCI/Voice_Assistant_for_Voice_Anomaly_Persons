"use client";
import Typography from "@mui/material/Typography";
import RadioButtonCheckedIcon from "@mui/icons-material/RadioButtonChecked";
import React, { useState, useRef } from "react";
import IconButton from "@mui/material/IconButton";
import StopCircleIcon from "@mui/icons-material/StopCircle";
import ReplayCircleIcon from "@mui/icons-material/ReplayCircleFilled";
import Button from "@mui/material/Button";

enum RecordingState {
  NOT_RECORDED,
  RECORDING,
  RECORDED,
}

function getColor(state: RecordingState) {
  switch (state) {
    case RecordingState.NOT_RECORDED:
      return "default";
    case RecordingState.RECORDING:
      return "error";
    case RecordingState.RECORDED:
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

  async function recognize() {
    let blob = new Blob(chunks.current);
    // TODO: call server action
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
    </div>
  );
}

export default Recorder;
