<script setup>
import Chessboard from "./components/Chessboard.vue";
import Background from "./components/Background.vue";
</script>

<template>
  <Background>
    <div class="main-container">
      <Chessboard />
    </div>
  </Background>
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
