<script setup>
import Chessboard from "frontend/src/components/Chessboard.vue";
import Robot from "./Robot.vue";


</script>

<template>
    <div class="main-container">
      <Chessboard>
      </Chessboard>
    </div>
</template>

<style scoped>

/*
*
* CONTAINER
*
*/

.main-container {
  height: 100vh;
  width: 100vw;

  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: row;
}


</style>
