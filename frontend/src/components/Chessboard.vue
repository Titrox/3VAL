<script setup>
import { TheChessboard } from 'vue3-chessboard';
import 'vue3-chessboard/style.css';
import {onMounted} from "vue";

let boardApi;

// Client will only be able to play white pieces.
const playerColor = 'white';

// Moves into this match
let moveCounter = 0;

// Receive move from socket/server/etc here.
function onReceiveMove(move) {
  boardApi?.move(move);
  moveCounter++;
}

// Checks playerColor onmount to rotate chessboard if necessary
onMounted(() => {
  playerColor !== "white" ? boardApi.toggleOrientation() : null ;
});


// Resets board
function resetBoard() {
  boardApi.resetBoard();
}

//undo last move if possible
function undoLastMove() {
  boardApi.undoLastMove();
}




</script>

<template>

  <div class="main-container">

    <div class="button-container button-container--settings">
      <button class="button button--toggle-ai">Toggle AI <i class="bi bi-robot"></i> </button>
    </div>

    <div class="chessboard-container">
      <TheChessboard
          @board-created="(api) => (boardApi = api)"
          player-color="white"
      />
    </div>

    <div class="button-container button-container--options">
      <button class="button button--reset" @click="resetBoard">Brett zurücksetzen <i class="bi bi-arrow-repeat"></i></button>
      <button class="button button--undo" @click="undoLastMove">Zug zurück <i class="bi bi-arrow-counterclockwise"></i></button>
      <button class="button button-switch">Seite wechseln</button>
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
  z-index: 100;
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

/* BUTTONS */

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

  filter: brightness(90%);
}


.button--reset {
  background-color: #f64040;
}

.button--dissabled {
  background-color: rgb(128, 128, 128);
}

</style>