<script setup>
import Background from "frontend/src/components/Background.vue";
import { useRouter } from 'vue-router'
import Music from "./components/Music.vue";


const router = useRouter()

function goToNormalMode() {
  router.push("/normal-mode");
}

function goToDebugMode() {
  router.push("/debug-mode");
}

</script>

<template>
  <Background>
    <div class="music-container" ref="musicContainer">
      <Music />
    </div>
    <router-view/>
  </Background>
</template>

<style scoped>

.music-container {
  position: absolute;
  top: 1vw;
  right: 1vw;
  z-index: 101;
}

</style>
