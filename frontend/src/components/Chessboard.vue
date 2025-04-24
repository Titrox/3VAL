<script setup>
import {TheChessboard} from 'vue3-chessboard';
import 'vue3-chessboard/style.css';
import {computed, ref} from "vue";
import axios from 'axios';
import robotText from 'frontend/src/assets/roboter-texts.json'
import {globalState} from 'frontend/public/store/globalState.js'
import { onMounted } from 'vue'
import Robot from "./Robot.vue";





// GENERAL


let boardApi = ref();

// Reactive computed property to check if sound is muted from the global state.
const soundMuted = computed(() => globalState.soundMuted);

// Client will only be able to play white pieces.
let playerColor = ref('white');

// Value of the last evaluated chessboard position.
let lastValue = ref(0);

// Difference in evaluation value between the last and current position.
let deltaValue;

// Counter for the current turn number.
let turnNumber = 0

// Opening played by player
let opening;



const robot = ref()

defineExpose({
  boardApi,
})


// ROBOT FIELDS




// Triggered when component is loaded
onMounted(() => {
  robot.value?.playSpeechSound()
})


// Function to receive a move from an external source (e.g., socket, server) and apply it to the chessboard.
function onReceiveMove(move) {
  boardApi?.value.move(move)
}


// Asynchronously fetches the best move from the backend based on the current board state.
async function playBestMove() {

  robot.value.evaluating = true // Engine starts evaluating

  const request = {
    fen: boardApi?.value.getFen(),
    is_white: boardApi?.value.getTurnColor() === "white"
  }

  try {

    let response = await axios.post('http://localhost:8080/best-move', request)
    const move_object = response.data

    console.log(move_object)
    onReceiveMove(move_object.move); // Play received move

    if (move_object.value >= -5000 && move_object.value <= 5000) { // Handle checkmate position

      deltaValue = lastValue.value - move_object.value;
      console.log("Delta value:" + deltaValue)
      lastValue.value = move_object.value

      robot.value?.updateRobot(deltaValue, turnNumber, playerColor.value);

    }

  } catch (e) {

    robot.value.message = "Ups, etwas scheint mit meiner Verbindung nicht zu stimmen."
    robot.value.playSpeechSound()

  } finally {
    robot.value.evaluating = false // Engine stops evaluating
  }
}


async function evaluatePosition() {

  const fen = boardApi?.value.getFen().split(" ")[0]

  const request = {
    fen: fen
  }

  try {

    const response = await axios.post("http://localhost:8080/evaluate-position", request)
    lastValue.value = parseFloat(response.data)
    return response.data

  } catch (e) {
    console.log(e.message)
  }
}




// Resets the chessboard to its initial state and resets the robot's state.
function resetBoard() {

  deltaValue = 0;
  lastValue.value = 0;
  turnNumber = 0;

  boardApi.value.resetBoard();
  playerColor.value = 'white';
  robot.value?.resetRobot();
}


// Undoes the last move made on the chessboard, if possible.
function undoLastMove() {
  boardApi.value.undoLastMove();
}


// Toggles the player's color between white and black.
function togglePlayerColor() {
  playerColor.value = playerColor.value === "white" ? "black" : "white";

  if (playerColor.value === "black") {
    playBestMove();
  }
}


// Handles a move made on the chessboard. If it's the engine's turn, it triggers the best move calculation.
// TODO: Prevent execution if the engine is in checkmate.
async function handleMove(move) {

  turnNumber += 1 // Increment turn counter

  playPieceSound()

  // Store played opening on 6. move
  if (turnNumber === 6) {
    opening = await boardApi?.value.getOpeningName();
    console.log(`OPENING STORED: ${opening}`)
    console.log("STORE IN ROBOT COMPONENT")
    robot.value.opening = await boardApi?.value.getOpeningName();
    console.log(`VALUE STORED:${robot.value.opening}`)
  }

  if (move.captured !== undefined) { // Piece was captured
    playCapturedSound()
  }

  if (boardApi?.value.getTurnColor() !== playerColor.value) {
    console.log("Player move:" + await evaluatePosition()) // Calc evaluation value after player move
    await playBestMove();
  }
}


// Handles the checkmate event. Updates the robot's emotion and message based on who is checkmated.
function handleCheckmate(isMated) {

  console.log(isMated)
  console.log(playerColor.value)
  console.log(isMated === playerColor.value)

  if (isMated !== playerColor.value){
    console.log("Matt");
    robot.value.emotion = 'embarrassed';
    robot.value.message = robotText["player_win"][Math.floor(Math.random() * robotText["player_win"].length)];
    robot.value.robotImage = 'images/shocked_1.png';
  }

  else {

    robot.value.emotion = 'happy';
    robot.value.message = robotText["engine_win"][Math.floor(Math.random() * robotText["engine_win"].length)];
    robot.value.robotImage = 'images/happy_2.png';
  }

  robot.value?.playSpeechSound()

}


// Plays a random piece movement sound if sound is not muted.
function playPieceSound() {

  if (!soundMuted.value) {
    const randomNum = Math.floor(Math.random() * 4) + 1;
    const piece_sound = new Audio(`/sounds/piece-sounds/piece_sound_${randomNum}.wav`)
    piece_sound.volume = 1.0;

    piece_sound.play()
  }
}


// Plays sound when peace is captured
function playCapturedSound() {

  if (!soundMuted.value) {

    console.log("Captured Sound")
    const captured_sound = new Audio(`/sounds/piece-sounds/captured_sound_2.mp3`)
    captured_sound.volume = 0.075
    captured_sound.play();
  }

}





</script>

<template>

  <div class="main-container">

    <div class="container container--robot-container">
      <Robot ref="robot"/>
      <slot>

      </slot>
    </div>

    <div class="chessboard-container">
      <TheChessboard
          @board-created="(api) => {
              boardApi = api;

              if (playerColor === 'black') {
                boardApi.toggleOrientation();
                handleMove;
              }
            }"

          :player-color="playerColor"
          :key="playerColor"
          @move="handleMove"
          @checkmate="handleCheckmate"


      />
    </div>

    <div class="button-container button-container--options">
      <button class="button button--reset" @click="resetBoard">Zurücksetzen <i class="bi bi-arrow-repeat"></i></button>
      <button class="button button--undo" @click="undoLastMove">Zug zurück <i class="bi bi-arrow-counterclockwise"></i></button>
      <button class="button button--switch" @click="togglePlayerColor">Seite wechseln <i class="bi bi-arrow-left-right"></i></button>
    </div>
  </div>
</template>

<style scoped>



@import url('https://fonts.googleapis.com/css2?family=DynaPuff:wght@400..700&family=Jersey+25&display=swap');


/*
*
* CONTAINER
*
*/

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


.container--robot-container {
  width: 20%;
  height: auto;

}

/*
*
* BUTTONS
*
*/

.button {
  border: none;
  border-radius: 10px;
  height: 5vh;
  width: 10vw;

  font-family: 'Jersey 25', Arial, sans-serif;
  font-size: 110%;
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



img{
  width: 100%;
  height: auto;
}



</style>