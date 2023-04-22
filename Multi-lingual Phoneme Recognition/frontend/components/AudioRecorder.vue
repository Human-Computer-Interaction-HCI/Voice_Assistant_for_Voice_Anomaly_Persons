<script setup lang="ts">

const audio = ref<HTMLAudioElement | null>(null)
const mediaRecorder: Ref<MediaRecorder | null> = ref(null)

async function startRecording() {
    let stream = await navigator
        .mediaDevices
        .getUserMedia({
            audio: true,
            video: false
        })

    mediaRecorder.value = new MediaRecorder(stream)
    mediaRecorder.value!.start()

    let chunks: Blob[] = []
    mediaRecorder.value!.ondataavailable = (e) => {
        chunks.push(e.data)
    }
    mediaRecorder.value!.onerror = (e) => {
        alert(e)
    }

    mediaRecorder.value!.onstop = (e)=>{
        let url = URL.createObjectURL(new Blob(chunks))
        audio.value!.src = url
    }
}

</script>

<template>
    <div>
        <audio controls ref="audio" />
        <button @click="startRecording">Старт</button>
        <button @click="mediaRecorder?.stop()">Стоп</button>
    </div>
</template>
