"use client";
import AddIcon from "@mui/icons-material/Add";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import CloseIcon from "@mui/icons-material/Close";
import Modal from "@mui/material/Modal";
import Typography from "@mui/material/Typography";
import { useEffect, useState } from "react";
import IconButton from "@mui/material/IconButton";
import Recorder from "@/components/Recorder";
import { DatasetList, DatasetRecording } from "@/api/datasets";
import { getDatasets, getDataset } from "./actions";
import Stack from "@mui/material/Stack";
import Chip from "@mui/material/Chip";
import RecordingsTable from "@/components/RecordingsTable";

export default function Page() {
  const [recordingModalOpened, setRecordingModalOpened] = useState(false);
  const [datasets, setDatasets] = useState<DatasetList>()
  const [dataset, setDataset] = useState<DatasetRecording[]>([])

  function addRecord() {
    setRecordingModalOpened(true);
  }
  function closeModal() {
    setRecordingModalOpened(false);
  }

  useEffect(() => {
    getDatasets().then(setDatasets)
    getDataset().then(setDataset)
  }, [])

  const DSLIST = <Stack direction='row'>
    {datasets?.datasets.map(ds =>
      <Chip key={ds.label} label={ds.label} variant="filled" color="success" />
    )}
  </Stack>

  return (
    <>
      <Typography variant="h1">Мои записи</Typography>
      <Button variant="contained" startIcon={<AddIcon />} onClick={addRecord}>
        Добавить
      </Button>
      <Modal open={recordingModalOpened} onClose={closeModal}>
        <Box
          sx={{
            position: "absolute" as "absolute",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            width: "fit-content",
            bgcolor: "background.paper",
            border: "2px solid #000",
            boxShadow: 24,
            p: 4,
            display: "flex",
            flexDirection: "row-reverse",
            justifyContent: "flex-end",
            alignItems: "flex-start"
          }}
        >
          <IconButton onClick={closeModal} sx={{ width: "fit-content", height: "fit-content" }}>
            <CloseIcon />
          </IconButton>
          <Recorder />
        </Box>
      </Modal>
      {DSLIST}
      <RecordingsTable recordings={dataset} />
    </>
  );
}
