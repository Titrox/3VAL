<script setup>
import { useRouter } from 'vue-router'
import {ref} from "vue";


const router = useRouter()

// Text on the debug button
let debugText = ref("DEBUG")

// Store IntervalId for glitch effect of debug button
let intervalId = ref(null)


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



function goToNormalMode() {
  router.push("/normal-mode");
}

function goToDebugMode() {
  router.push("/debug-mode");
}

</script>

<template>

    <div class="main-container">

      <div class="button-container button-container--modeSelect">
        <button class="menu-button menu-button--normalMode" @click="goToNormalMode">Normal</button>
        <button
            class="menu-button menu-button--debugMode"
            @mouseover="startAction"
            @mouseleave="stopAction"
            @click="goToDebugMode"
        >
          {{ debugText }}
        </button>

      </div>

    </div>
    <div class="music-container" ref="musicContainer">
    </div>

</template>

<style scoped>

/* CONTAINER */

.main-container {
  height: 100vh;
  width: 100vw;

  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: row;
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

</style>
