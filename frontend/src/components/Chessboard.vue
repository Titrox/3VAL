<script setup>
import { TheChessboard } from 'vue3-chessboard';
import 'vue3-chessboard/style.css';
import {ref} from "vue";
import axios from 'axios';
import robotText from 'frontend/src/assets/roboter-texts.json'

let boardApi;

// Client will only be able to play white pieces.
let playerColor = ref('white');


// Value of last chessboard
let lastValue = ref(0);

// Value Difference
let deltaValue;

// Robot Emotion
let emotion = ref('happy');

// Robot Message
let message = ref(robotText["start"][Math.floor(Math.random() * robotText["start"].length)]);


let robotImage = ref('images/happy_1.png')


// Receive move from socket/server/etc here.
function onReceiveMove(move) {
  boardApi?.move(move)
}

function getRobotImage(emotion) {
  const randomNumber = Math.floor(Math.random() * 2) + 1; // ergibt 1 oder 2
  return `/images/${emotion}_${randomNumber}.png`;
}


function getRobotEmotion(deltaValue) {
    if (deltaValue >= 100) return "happy";
    if (deltaValue <= -50) return "embarrassed";
    if (deltaValue <= -100) return "shocked";
    return "thoughtful";
}


// Play best move found by validation function
async function playBestMove() {

  const request = {
    fen: boardApi?.getFen(),
    is_white: boardApi?.getTurnColor() === "white"
  }

  try {
    let response = await axios.post('http://localhost:8080/best-move', request)
    const move_object = response.data
    console.log(move_object)

    if (move_object.value !== "-inf" && move_object.value !== "inf") {

      deltaValue = lastValue.value - move_object.value;
      lastValue.value = move_object.value
      console.log(deltaValue)

      emotion = getRobotEmotion(deltaValue);
      message.value = robotText[emotion][Math.floor(Math.random() * robotText[emotion].length)];
      robotImage.value = getRobotImage(emotion)
      console.log("Emotion changed!")
      console.log(message)
    }

    onReceiveMove(move_object.move);
  } catch (e) {
     console.error(e.message);
  }
}


// Resets board
function resetBoard() {
  boardApi.resetBoard();
  playerColor.value = 'white';
  console.log("test")
  resetRobot();
}

//undo last move if possible
function undoLastMove() {
  boardApi.undoLastMove();
}


// Changes player side
function togglePlayerColor() {
  playerColor.value = playerColor.value === "white" ? "black" : "white";
}


// Check if it is AIs turn and play the best move found by validation function
function handleMove() {
  if (boardApi?.getTurnColor() !== playerColor.value) {
    playBestMove();
  }
}


function resetRobot() {
  message.value = robotText["start"][Math.floor(Math.random() * robotText["start"].length)];
  robotImage.value = 'images/happy_1.png';
}

function handleCheckmate(isMated) {

  console.log(isMated)
  console.log(playerColor.value)
  console.log(isMated === playerColor.value)

  if (isMated !== playerColor.value){
    emotion = 'embarrassed';
    message.value = robotText["player_win"][Math.floor(Math.random() * robotText["player_win"].length)];
    robotImage.value = 'images/shocked_1.png';
  }

  else {
    console.log("Matt");
    emotion = 'happy';
    message.value = robotText["engine_win"][Math.floor(Math.random() * robotText["engine_win"].length)];
    robotImage.value = 'images/happy_1.png';
  }

}


</script>

<template>

  <div class="main-container">

    <div class="button-container container--figure-text-container">
      <div class="container container--figure-container"><img :src="robotImage" alt="roboter-glücklich"> </div>
      <div class="container container--text-container">{{ message }}</div>
    </div>

    <div class="chessboard-container">
      <TheChessboard
          @board-created="(api) => {
            boardApi = api;

            if (playerColor === 'black') {
              boardApi.toggleOrientation();
              handleMove();
            }
          }"

          :player-color="playerColor"
          :key="playerColor"
          @move="handleMove()"
          @checkmate="handleCheckmate"

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


@import url('https://fonts.googleapis.com/css2?family=Jersey+25&display=swap');

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

.container--figure-text-container{
  height: 13vh;

  display: flex;
  justify-content: space-evenly;
  align-items: center;
  flex-direction: row;
  gap: 2vw;
}


.container--figure-container{
  border-radius: 10%;
  flex: 1;

  display: flex;
  justify-content: center;
  align-items: end;
}

.container--text-container{
  flex: 2;
  background-color: white;
  border-radius: 10%;
  height: 50%;

  display: flex;
  justify-content: center;
  align-items: center;

  padding: 1vw;

  font-family: 'Jersey 25', Arial, sans-serif;
}

img{
  width: 100%;
  height: auto;
}

</style>