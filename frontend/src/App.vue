<script setup>
import Chessboard from "./components/Chessboard.vue";
</script>

<template>
  <div class="main-container">
    <Chessboard />
  </div>
</template>

<style scoped>
.main-container {
  height: 100vh;
  width: 100vw;

  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: row;
}
</style>
