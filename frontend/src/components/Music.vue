<script setup>
import { ref } from 'vue';

const audio = new Audio('/music/BackgroundJazz.mp3');
audio.loop = true;
const isPlaying = ref(false);


// Toggle Music depending on current isPlaying value
function toggleMusic() {
  if (isPlaying.value) {
    audio.pause();
  } else {
    audio.play();
  }
  isPlaying.value = !isPlaying.value;
};




</script>

<template>
  <button class="button button--sound" @click="toggleMusic">
    <i v-if="!isPlaying" class="bi bi-volume-mute-fill"></i>
    <i v-else class="bi bi-volume-up-fill"></i>
  </button>
</template>

<style scoped>

.button {
  background: none;
  font-size: 200%;
  border: none;
}

.bi {
  color: rgba(0,0,0,40%);
}


.button:hover {
  cursor: pointer;
}

</style>
