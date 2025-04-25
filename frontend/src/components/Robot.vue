<script setup>
import {globalState} from 'frontend/public/store/globalState.js'
import 'vue3-chessboard/style.css';
import {computed, ref} from "vue";
import robotText from 'frontend/src/assets/roboter-texts.json'


// Reactive computed property to check if sound is muted from the global state.
const soundMuted = computed(() => globalState.soundMuted);


//
// ROBOT FIELDS
//


// Keeps track of emotion changes
let sameEmotionCount;

// Current emotion of the robot. Defaults to 'happy'.
let emotion = 'happy';

// Stores the robot's emotion from the last chessboard evaluation.
let lastEmotion = '';

// Message displayed by the robot. Initialized with a random start message.
let message = ref(robotText["start"][Math.floor(Math.random() * robotText["start"].length)]);

// Currently displayed robot image. Initialized with a happy image.
let robotImage = ref('images/happy_1.png')

// Opening played by player
let opening = ref("test123");

// True if Engine is currently
let evaluating = ref(false)




// Defines exposed functions, given functions can be called by parent component
defineExpose({
  updateRobot,
  resetRobot,
  playSpeechSound,
  evaluating,
  emotion,
  robotImage,
  opening,
  message,
})



//
// ROBOT
//



function getRobotImage(emotion) {
  const randomNumber = Math.floor(Math.random() * 2) + 1; // Generates either 1 or 2.
  return `/images/${emotion}_${randomNumber}.png`;
}

// Function to determine the robot's emotion based on the change in evaluation value.
function getRobotEmotion(deltaValue, playerColor) {

  if (playerColor.value === 'black') { // Invert the value if the engine is playing white.
    deltaValue = -deltaValue;
  }

  if (deltaValue >= 150) return "happy";
  if (deltaValue <= -70) return "embarrassed";
  if (deltaValue <= -150) return "shocked";
  return "thoughtful";
}


// Updates the robot's emotion, message, and image based on the change in evaluation value.
// TODO Refactor
function updateRobot(deltaValue, turnNumber, playerColor) {

  // Get updated robot emotion
  emotion = getRobotEmotion(deltaValue, playerColor);


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

  } else if (emotion === lastEmotion) { // Random fun-fact if robots emotion have not changed for 6 engine moves

    sameEmotionCount++
    console.log(`Same Emotion + ${sameEmotionCount}`)

    if (sameEmotionCount > 5 && turnNumber >= 10) {
      message.value = robotText["fun_facts"][Math.floor(Math.random() * robotText["fun_facts"].length)];
      emotion = "happy"
      robotImage.value = getRobotImage("happy")
      sameEmotionCount = 0;
      playSpeechSound()
    }

  } else if (turnNumber === 8 || turnNumber === 9) { // Comment on opening on 8. or 9. move (depending on player-color)

    const rawMessage = robotText["opening_commentary"][Math.floor(Math.random() * robotText["opening_commentary"].length)];
    console.log("COMMENT OPENING")

    message.value = rawMessage.replace("${opening}", opening.value)
    emotion = "happy"
    robotImage.value = getRobotImage("happy")
    playSpeechSound()
  }
}


// Resets the robot's message and image to the initial state and plays a speech sound.
function resetRobot() {
  message.value = robotText["start"][Math.floor(Math.random() * robotText["start"].length)];
  robotImage.value = 'images/happy_1.png';
  playSpeechSound()
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

</script>

<template>

  <div class="main-container">

    <div class="button-container container--figure-text-container">

      <div class="container container--figure-container"><img :src="robotImage" alt="roboter-glücklich">

        <div class="container container--loading-container" v-if="evaluating">
          <div class="loader"></div>

        </div>

      </div>
      <div class="container container--text-container">{{ message }}</div>

    </div>

  </div>

</template>

<style scoped>


/**
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


/**
*
* ROBOT
*
 */



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
  position: relative;

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


.container--loading-container{
  position: absolute;
  top: -3vh;
  color: rgba(0,0,0,0.4);
  font-size: 70%;
}

img{
  width: 100%;
  height: auto;
}


/**
*
* Loader
*
 */



.loader {
  width: 8px;
  aspect-ratio: 1;
  border-radius: 20%;
  animation: l5 1s infinite linear alternate;
}
@keyframes l5 {
  0%  {box-shadow: 10px 0 #000, -10px 0 #0002;background: #000 }
  33% {box-shadow: 10px 0 #000, -10px 0 #0002;background: #0002}
  66% {box-shadow: 10px 0 #0002,-10px 0 #000; background: #0002}
  100%{box-shadow: 10px 0 #0002,-10px 0 #000; background: #000 }
}



</style>