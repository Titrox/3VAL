<script setup>
import Chessboard from "frontend/src/components/Chessboard.vue";
import Robot from "./Robot.vue";


</script>

<template>
  <div class="main-container">
    <Chessboard>
      <h2 class="text text--debug-test">DEBUG MODE</h2>
      <div class="container container--debug-container">
        <div class="container container--debug-tools-container"></div>
        <div class="container container--safe-discard-button-container"></div>
      </div>
    </Chessboard>
  </div>
</template>

<style scoped>

/* CONTAINER */

.main-container {
  height: 100vh;
  width: 100vw;
  font-family: 'Jersey 25', Arial, sans-serif;

  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: row;
}

.text--debug-test {
  text-align: center;
  margin-top: 30px;
  margin-bottom: 10px;
}


.container--debug-container {
  height: 30vh;
  padding: 5vh 1vw;

  background-color: beige;
  border-radius: 10px;
  box-shadow: rgba(0,0,0,10%) 4px 4px;

  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  gap: 5vh;
}


</style>


