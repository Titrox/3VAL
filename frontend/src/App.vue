<script setup>
import Chessboard from "./components/Chessboard.vue";
import Background from "./components/Background.vue";
import Music from "./components/Music.vue";
</script>

<template>
  <Background>
    <div class="main-container">
      <Chessboard />
    </div>
    <div class="music-container">
      <Music/>
    </div>
  </Background>
</template>

<style scoped>

/* CONTAINER */

.main-container {
  height: 100vh;
  width: 100vw;

  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: row;
}

.music-container {
  position: absolute;
  top: 1vw;
  right: 1vw;
  z-index: 101;
}

</style>
