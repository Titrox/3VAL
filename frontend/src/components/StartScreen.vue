<script setup>
import { useRouter } from 'vue-router'
import {onMounted, ref, computed} from "vue";
import robotText from "../assets/roboter-texts.json";
import {globalState} from 'frontend/public/store/globalState.js'


const router = useRouter()

// Reactive computed property to check if sound is muted from the global state.
const soundMuted = computed(() => globalState.soundMuted);

// Text on the debug button
let debugText = ref("DEBUG")

// Store IntervalId for glitch effect of debug button
let intervalId = ref(null)


//
// ROBOT
//


// Message loaded
let message = ref("test123")

// Robot image
const robotImage = "/images/happy_2.png"


// Triggered when component is loaded
onMounted(() => {
  message.value = robotText["mode_select"][Math.floor(Math.random() * robotText["mode_select"].length)];
  playSpeechSound()
})


// Plays a random speech sound if sound is not muted.
function playSpeechSound() {

  if (!soundMuted.value) {
    const randomNum = Math.floor(Math.random() * 6) + 1;
    const speechSound = new Audio(`/sounds/speech-sounds/speech_${randomNum}.wav`)
    speechSound.volume = 0.2;

    speechSound.play();
  }

}

//
// BUTTONS
//

function goToNormalMode() {
  router.push("/normal-mode");
}

function goToDebugMode() {
  router.push("/debug-mode");
}



//
// DEBUG BUTTON
//

function generateRandomString(length = 5) {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-_=+[]{};:,.<>?'
  let result = ''
  for (let i = 0; i < length; i++) {
    const randomIndex = Math.floor(Math.random() * chars.length)
    result += chars[randomIndex]
  }
  return result
}

function startAction() {
  if (intervalId.value == null) {
    intervalId.value = setInterval(() => {
      debugText.value = generateRandomString()
    }, 70)
  }
}

function stopAction() {
  clearInterval(intervalId.value)
  intervalId.value = null
  debugText.value = "DEBUG"
}




</script>

<template>

    <div class="main-container">

      <div class="button-container container--figure-text-container">
        <div class="container container--figure-container"><img :src="robotImage" alt="roboter-glücklich"> </div>
        <div class="container container--text-container">{{ message }}</div>
      </div>

      <h2>Wähle einen Modus</h2>

      <div class="button-container button-container--modeSelect">

        <div class="container container--button-description">

          <button class="menu-button menu-button--normalMode" @click="goToNormalMode">Normal</button>
          <p>Spiele gegen die aktuelle Version von <b>3VAL</b></p>
        </div>

        <div class="container container--button-description">
        <button
            class="menu-button menu-button--debugMode"
            @mouseover="startAction"
            @mouseleave="stopAction"
            @click="goToDebugMode"
        >
          {{ debugText }}
        </button>

          <p>Passe die Evaluierungsfunktion an, lade FEN oder lasse <b>3VAL</b> gegen Stockfish spielen!</p>

        </div>
      </div>

    </div>
    <div class="music-container" ref="musicContainer">
    </div>

</template>

<style scoped>

@import url('https://fonts.googleapis.com/css2?family=DynaPuff:wght@400..700&family=Jersey+25&display=swap');


p {
  font-family: 'Jersey 25', Arial, sans-serif;
  margin-top: 10px;
  color: rgba(0,0,0,0.4);
  text-align: center;
  font-size: 90%;
}

h2{
  font-family: 'Jersey 25', Arial, sans-serif;
  letter-spacing: 1px;
  margin-top: 10vh;
  margin-bottom: 3vh;
}




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
  flex-direction: column;
}

.music-container {
  position: absolute;
  top: 1vw;
  right: 1vw;
  z-index: 101;
}


.button-container {
  height: auto;
  width: 20%;
  padding: 5vh 1vw;
  z-index: 10;

  background-color: beige;
  border-radius: 10px;
  box-shadow: rgba(0,0,0,10%) 4px 4px;

  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  gap: 5vh;
}


.container--button-description {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;


  width: 100%;

}



/*
*
* BUTTON
*
*/


.menu-button {
  border: none;
  border-radius: 10px;
  height: 5vh;
  width: 10vw;

  font-family: 'Jersey 25', Arial, sans-serif;
  font-weight: 200;
  font-size: 110%;

  box-shadow: black 4px 4px;
  background-color: #99f381;
}


.menu-button:hover {
  transform: translateY(4px);
  box-shadow: none;
  cursor: pointer;

  filter: brightness(90%);
}


.menu-button--debugMode {
  letter-spacing: 4px;
  background-color: rgba(79, 133, 194, 0.93);
}

/**
*
* ROBOT
*
**/


.container--figure-text-container{
  height: 13vh;
  width: 30vw;

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
