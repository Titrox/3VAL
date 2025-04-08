<script setup>
import { ref } from 'vue';
import { globalState } from 'frontend/public/store/globalState.js';

const audio = new Audio('/music/8-bit.mp3');


audio.loop = true;
audio.volume = 0.5
let soundMuted = ref(globalState.soundMuted);


// Toggle Music depending on current isPlaying value
function toggleMusic() {
  if (!soundMuted.value) {
    audio.pause();
  } else {
    audio.play();
  }
  soundMuted.value = !soundMuted.value;
  globalState.soundMuted = soundMuted.value
}





</script>

<template>
  <button class="button button--sound" @click="toggleMusic">
    <i v-if="soundMuted" class="bi bi-volume-mute-fill"></i>
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
