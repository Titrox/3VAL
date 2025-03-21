<script setup>
import { TheChessboard } from 'vue3-chessboard';
import 'vue3-chessboard/style.css';
import {onMounted, ref} from "vue";
import axios from 'axios';

let boardApi;

// Client will only be able to play white pieces.
let playerColor = ref('white');


// Receive move from socket/server/etc here.
function onReceiveMove(move) {
  boardApi?.move(move);
}


// Play best move found by validation function
async function playBestMove() {
  try {
    let response = await axios.post('http://localhost:8080/best-move', boardApi.getFen())
    console.log((response).data);
  } catch (e) {
     console.error(e.message);
  }
}


// Resets board
function resetBoard() {
  boardApi.resetBoard();
  playerColor.value = 'white';
}

//undo last move if possible
function undoLastMove() {
  boardApi.undoLastMove();
}


// Changes player side
function togglePlayerColor() {
  playerColor.value = playerColor.value === "white" ? "black" : "white";
}



function handleMove() {
  if (boardApi?.getTurnColor() !== playerColor.value) {
    playBestMove();
  }
}


</script>

<template>

  <div class="main-container">

    <div class="button-container button-container--settings">
      <button class="button button--toggle-ai">Toggle AI <i class="bi bi-robot"></i> </button>
    </div>

    <div class="chessboard-container">
      <TheChessboard
          @board-created="(api) => {
            boardApi = api;

            if (playerColor === 'black') {
              boardApi.toggleOrientation();
            }
          }"

          :player-color="playerColor"
          :key="playerColor"
          @move="handleMove()"
      />
    </div>

    <div class="button-container button-container--options">
      <button class="button button--reset" @click="resetBoard">Brett zurücksetzen <i class="bi bi-arrow-repeat"></i></button>
      <button class="button button--undo" @click="undoLastMove">Zug zurück <i class="bi bi-arrow-counterclockwise"></i></button>
      <button class="button button-switch" @click="togglePlayerColor">Seite wechseln <i class="bi bi-arrow-left-right"></i></button>
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