<script setup>
import Chessboard from "frontend/src/components/Chessboard.vue";
import Background from "frontend/src/components/Background.vue";
import Music from "frontend/src/components/Music.vue";

</script>

<template>
    <div class="main-container">
      <Chessboard />
    </div>
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


</style>
