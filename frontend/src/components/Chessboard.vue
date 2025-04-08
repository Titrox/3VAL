<script setup>
import { TheChessboard } from 'vue3-chessboard';
import 'vue3-chessboard/style.css';
import {computed, ref} from "vue";
import axios from 'axios';
import robotText from 'frontend/src/assets/roboter-texts.json'
import { globalState } from 'frontend/public/store/globalState.js'


let boardApi;

//
const soundMuted = computed(() => globalState.soundMuted);

// Client will only be able to play white pieces.
let playerColor = ref('white');

// Value of last chessboard
let lastValue = ref(0);

// Value Difference
let deltaValue;

// Robot Emotion
let emotion = 'happy';

// Stores robot emotion of last chessboard evaluation
let lastEmotion = '';

// Robot Message
let message = ref(robotText["start"][Math.floor(Math.random() * robotText["start"].length)]);

// Currently loaded Robot image
let robotImage = ref('images/happy_1.png')

// Current turn
let turnNumber = 0;





// Receive move from socket/server/etc here.
function onReceiveMove(move) {
  boardApi?.move(move)
}

function getRobotImage(emotion) {
  const randomNumber = Math.floor(Math.random() * 2) + 1; // ergibt 1 oder 2
  return `/images/${emotion}_${randomNumber}.png`;
}


function getRobotEmotion(deltaValue) {

    if (playerColor.value === 'black') { // Invert value if engine is playing white
      deltaValue = -deltaValue;
    }

    if (deltaValue >= 150) return "happy";
    if (deltaValue <= -70) return "embarrassed";
    if (deltaValue <= -150) return "shocked";
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

      updateRobot(deltaValue);
    }

    onReceiveMove(move_object.move);
  } catch (e) {
     console.error(e.message);
  }
}


function updateRobot(deltaValue) {


  emotion = getRobotEmotion(deltaValue);

  if (turnNumber < 3) { // First moves of Engine -
    message.value = robotText["opening"][Math.floor(Math.random() * robotText["opening"].length)];
    return
  }

  // No new text for next few moves

  if ((emotion !== lastEmotion || turnNumber % 3 === 0) && turnNumber > 5) {

    lastEmotion = emotion;
    message.value = robotText[emotion][Math.floor(Math.random() * robotText[emotion].length)];
    robotImage.value = getRobotImage(emotion)

    playSpeechSound()
  }

}

// Resets board
function resetBoard() {

  deltaValue = 0;
  lastValue.value = 0;

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
// TODO dont exec if engine is in checkmate
function handleMove() {

  playPieceSound()

  if (boardApi?.getTurnColor() !== playerColor.value) {
    playBestMove();
  }

  turnNumber = boardApi?.getCurrentTurnNumber(); // Increase turn counter
}


function resetRobot() {
  message.value = robotText["start"][Math.floor(Math.random() * robotText["start"].length)];
  robotImage.value = 'images/happy_1.png';
  playSpeechSound()
}


function playPieceSound() {

  console.log(soundMuted.value)

  if (!soundMuted.value) {
    const randomNum = Math.floor(Math.random() * 4) + 1;
    const piece_sound = new Audio(`/sounds/piece-sounds/piece_sound_${randomNum}.wav`)
    piece_sound.volume = 1.0;


    piece_sound.play()
  }
}


function playSpeechSound() {

  if (!soundMuted.value) {
    const randomNum = Math.floor(Math.random() * 6) + 1;
    const speechSound = new Audio(`/sounds/speech-sounds/speech_${randomNum}.wav`)
    speechSound.volume = 0.3;

    speechSound.play();
  }

}

function handleCheckmate(isMated) {

  console.log(isMated)
  console.log(playerColor.value)
  console.log(isMated === playerColor.value)

  if (isMated !== playerColor.value){
    console.log("Matt");
    emotion = 'embarrassed';
    message.value = robotText["player_win"][Math.floor(Math.random() * robotText["player_win"].length)];
    robotImage.value = 'images/shocked_1.png';
  }

  else {

    emotion = 'happy';
    message.value = robotText["engine_win"][Math.floor(Math.random() * robotText["engine_win"].length)];
    robotImage.value = 'images/happy_1.png';
  }

  playSpeechSound()

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
      <button class="button button--reset" @click="resetBoard">Zurücksetzen <i class="bi bi-arrow-repeat"></i></button>
      <button class="button button--undo" @click="undoLastMove">Zug zurück <i class="bi bi-arrow-counterclockwise"></i></button>
      <button class="button button-switch" @click="togglePlayerColor">Seite wechseln <i class="bi bi-arrow-left-right"></i></button>
    </div>
  </div>
</template>

<style scoped>



@import url('https://fonts.googleapis.com/css2?family=DynaPuff:wght@400..700&family=Jersey+25&display=swap');


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

  font-family: 'Dynapuff', Arial, sans-serif;
  font-weight: 200;

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