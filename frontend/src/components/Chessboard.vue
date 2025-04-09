<script setup>
import {TheChessboard} from 'vue3-chessboard';
import 'vue3-chessboard/style.css';
import {computed, ref} from "vue";
import axios from 'axios';
import robotText from 'frontend/src/assets/roboter-texts.json'
import {globalState} from 'frontend/public/store/globalState.js'


let boardApi;

// Reactive computed property to check if sound is muted from the global state.
const soundMuted = computed(() => globalState.soundMuted);

// Client will only be able to play white pieces.
let playerColor = ref('white');

// Value of the last evaluated chessboard position.
let lastValue = ref(0);

// Difference in evaluation value between the last and current position.
let deltaValue;

// Current emotion of the robot. Defaults to 'happy'.
let emotion = 'happy';

// Stores the robot's emotion from the last chessboard evaluation.
let lastEmotion = '';

// Message displayed by the robot. Initialized with a random start message.
let message = ref(robotText["start"][Math.floor(Math.random() * robotText["start"].length)]);

// Currently displayed robot image. Initialized with a happy image.
let robotImage = ref('images/happy_1.png')

// Counter for the current turn number.
let turnNumber = 0

// Opening played by player
let opening;


// Keeps track of emotion changes
let sameEmotionCount;






// Function to receive a move from an external source (e.g., socket, server) and apply it to the chessboard.
function onReceiveMove(move) {
  boardApi?.move(move)
}

// Function to get the file path of a robot image based on the given emotion.
function getRobotImage(emotion) {
  const randomNumber = Math.floor(Math.random() * 2) + 1; // Generates either 1 or 2.
  return `/images/${emotion}_${randomNumber}.png`;
}


// Function to determine the robot's emotion based on the change in evaluation value.
function getRobotEmotion(deltaValue) {

  if (playerColor.value === 'black') { // Invert the value if the engine is playing white.
    deltaValue = -deltaValue;
  }

  if (deltaValue >= 150) return "happy";
  if (deltaValue <= -70) return "embarrassed";
  if (deltaValue <= -150) return "shocked";
  return "thoughtful";
}


// Asynchronously fetches the best move from the backend based on the current board state.
async function playBestMove() {

  const request = {
    fen: boardApi?.getFen(),
    is_white: boardApi?.getTurnColor() === "white"
  }

  try {
    let response = await axios.post('http://localhost:8080/best-move', request)
    const move_object = response.data
    console.log(move_object)



    onReceiveMove(move_object.move);

    if (move_object.value !== "-inf" && move_object.value !== "inf") {

      deltaValue = lastValue.value - move_object.value;
      lastValue.value = move_object.value

      updateRobot(deltaValue);
    }

  } catch (e) {
    console.error(e.message);
  }
}


// Updates the robot's emotion, message, and image based on the change in evaluation value.
// TODO Refactor
function updateRobot(deltaValue) {

  // Get updated robot emotion
  emotion = getRobotEmotion(deltaValue);

  console.log(emotion)
  console.log(lastEmotion)

  if (turnNumber < 3) { // For the first few moves of the engine.

    message.value = robotText["opening"][Math.floor(Math.random() * robotText["opening"].length)];
    playSpeechSound()

  } else if ((emotion !== lastEmotion || turnNumber % 3 === 0) && turnNumber >= 10) {  // Change message all 3 moves or if emotion changes

    if (emotion === lastEmotion) { // Check if Emotion changed
      sameEmotionCount++
    } else {
      sameEmotionCount = 0;
    }


    lastEmotion = emotion;
    message.value = robotText[emotion][Math.floor(Math.random() * robotText[emotion].length)];
    robotImage.value = getRobotImage(emotion)
    playSpeechSound()

  } else if (emotion === lastEmotion) { // Random fun-fact if robots emotion have not changed for 4 engine moves

    sameEmotionCount++
    console.log(`Same Emotion + ${sameEmotionCount}`)

    if (sameEmotionCount > 4 && turnNumber >= 10) {
      message.value = robotText["fun_facts"][Math.floor(Math.random() * robotText["fun_facts"].length)];
      emotion = "happy" // TODO isnt happy lol
      sameEmotionCount = 0;
      playSpeechSound()
    }

  } else if (turnNumber === 8 || turnNumber === 9) { // Comment on opening on 8. or 9. move (depending on player-color)

    const rawMessage = robotText["opening_commentary"][Math.floor(Math.random() * robotText["opening_commentary"].length)];

    message.value = rawMessage.replace("${opening}", opening)
    robotImage.value = getRobotImage("happy")
    playSpeechSound()

  }
}

// Resets the chessboard to its initial state and resets the robot's state.
function resetBoard() {

  deltaValue = 0;
  lastValue.value = 0;
  turnNumber = 0;

  boardApi.resetBoard();
  playerColor.value = 'white';
  console.log("test")
  resetRobot();
}

// Undoes the last move made on the chessboard, if possible.
function undoLastMove() {
  boardApi.undoLastMove();
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
    opening = await boardApi?.getOpeningName();
  }

  if (move.captured !== undefined) { // Piece was captured
    playCapturedSound()
  }

  if (boardApi?.getTurnColor() !== playerColor.value) {
    await playBestMove();
  }
}


// Resets the robot's message and image to the initial state and plays a speech sound.
function resetRobot() {
  message.value = robotText["start"][Math.floor(Math.random() * robotText["start"].length)];
  robotImage.value = 'images/happy_1.png';
  playSpeechSound()
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


// Plays a random speech sound if sound is not muted.
function playSpeechSound() {

  if (!soundMuted.value) {
    const randomNum = Math.floor(Math.random() * 6) + 1;
    const speechSound = new Audio(`/sounds/speech-sounds/speech_${randomNum}.wav`)
    speechSound.volume = 0.2;

    speechSound.play();
  }

}

// Handles the checkmate event. Updates the robot's emotion and message based on who is checkmated.
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
    robotImage.value = 'images/happy_2.png';
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