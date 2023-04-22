<template>
    <h2 style="font-weight: 800;">{{ text }}</h2>
</template>

<script lang="ts">
export default {
    props: {
        text: {
            type: String,
            default: "HMR"
        }
    }
}
</script>