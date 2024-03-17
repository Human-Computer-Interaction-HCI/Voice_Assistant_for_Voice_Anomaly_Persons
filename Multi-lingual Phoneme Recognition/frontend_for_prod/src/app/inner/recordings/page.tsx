"use client";
import AddIcon from "@mui/icons-material/Add";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import CloseIcon from "@mui/icons-material/Close";
import Modal from "@mui/material/Modal";
import Typography from "@mui/material/Typography";
import { useState } from "react";
import IconButton from "@mui/material/IconButton";
import Recorder from "@/components/Recorder";

export default function Page() {
  const [recordingModalOpened, setRecordingModalOpened] = useState(false);
  function addRecord() {
    setRecordingModalOpened(true);
  }
  function closeModal() {
    setRecordingModalOpened(false);
  }

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
          <IconButton onClick={closeModal} sx={{width: "fit-content", height: "fit-content"}}>
            <CloseIcon />
          </IconButton>
          <Recorder />
        </Box>
      </Modal>
    </>
  );
}
