<script setup>
import { TheChessboard } from 'vue3-chessboard';
import 'vue3-chessboard/style.css';
</script>

<template>

  <div class="main-container">

    <div class="button-container button-container--settings">
      <button class="button button--toggle-ai">Toggle AI</button>
    </div>

    <div class="chessboard-container">
      <TheChessboard />
    </div>

    <div class="button-container button-container--options">
      <button class="button button--reset">Zurücksetzen</button>
      <button class="button button--undo">Zurück</button>
      <button class="button button--forward">Weiter</button>
    </div>
  </div>
</template>

<style scoped>

/* CONTAINER */

.main-container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: row;

  gap: 3vw;

  background-color: #add39b;
}


.button-container {
  height: auto;
  width: 20%;
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


.chessboard-container {
  box-shadow: rgba(0,0,0,10%) 4px 4px;
  padding: 1vw 1vw;
  background-color: beige;
  border-radius: 10px;
}

/* BUTTON */

.button {
  border: none;
  border-radius: 10px;
  height: 5vh;
  width: 10vw;

  box-shadow: black 4px 4px;
  background-color: #99f381;
}


.button:hover {
  transform: translateY(4px);
  box-shadow: none;
  cursor: pointer;
}


.button--reset {
  background-color: #f64040;
}

</style>