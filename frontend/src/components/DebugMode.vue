<script setup>
import Chessboard from "frontend/src/components/Chessboard.vue";
import {onMounted, onUnmounted, ref, watch} from "vue";
import axios from "axios";



let valueChanged = ref(false)
let ignoreWatch = false;


// KING SAFETY
let pawnShieldValue = ref(0)
let virtualMobilityValue = ref(0)

// KING SAFETY - standard values
let standardPawnShieldValue = 0
let standardVirtualMobilityValue = 0


// DYNAMIC CONTROL
let centerControlValue = ref(0)

// DYNAMIC CONTROL - standard values
let standardCenterControlValue = 0


// EVALUATION OF PIECES
let badBishopValue = ref(0)
let knightOutpostValue = ref(0)
let queenEarlyDevValue = ref(0)


// EVALUATION OF PIECES - standard values
let standardBadBishopValue = 0
let standardKnightOutpostValue = 0
let standardQueenEarlyDevValue = 0



// PIECE VALUES

let queenValue = ref(0)
let knightValue = ref(0)
let bishopValue = ref(0)
let rookValue = ref(0)
let pawnValue = ref(0)


// PIECE VALUES - standard values

let standardQueenValue = 0
let standardKnightValue = 0
let standardBishopValue = 0
let standardRookValue = 0
let standardPawnValue = 0




onMounted(() => {
  const getFactorsInit = async () => {
    await getEvaluationFactors()

    valueChanged.value = false
  }
  getFactorsInit()
})

watch(
    [
      pawnShieldValue,
      virtualMobilityValue,
      centerControlValue,
      badBishopValue,
      knightOutpostValue,
      queenEarlyDevValue,
      queenValue,
      rookValue,
      bishopValue,
      knightValue,
      pawnValue
    ],
    () => {
      if (ignoreWatch) return

      if (valueChanged.value === false) { // Only trigger once when a change is detected
        console.log("Value changed")
        valueChanged.value = true
      }
    }
)


//
// FACTORS API REQUESTS
//

// Fetch the evaluation factors from backend
async function getEvaluationFactors() {
  try {
    const response = await axios.get('http://localhost:8080/get-evaluation-factors');
    const factors = response.data

    // Initialize values
    initFactors(factors)

  } catch (e) {
    console.log(e.message)
  }
}

// Send updated factors to the backend
async function putFactors() {
  const factors = {
    "pawnShieldValue": pawnShieldValue.value,
    "virtualMobilityValue": virtualMobilityValue.value,
    "centerControlValue": centerControlValue.value,
    "badBishopValue": badBishopValue.value,
    "knightOutpostValue": knightOutpostValue.value,
    "queenEarlyDevValue": queenEarlyDevValue.value,
    "queenValue": queenValue.value,
    "rookValue": rookValue.value,
    "bishopValue": bishopValue.value,
    "knightValue": knightValue.value,
    "pawnValue": pawnValue.value,
  }

  try {
    const response = await axios.put(
        'http://localhost:8080/put-evaluation-factors',
        factors,
        {
          headers: {
            'Content-Type': 'application/json'
          }
        }
    )

    valueChanged.value = false;

  } catch (e) {
    console.log(e.message)
  }
}

// Reset evaluation factors in backend to previously standard values (Backend)
async function resetFactors() {
  try {
    const response = await axios.post(
        'http://localhost:8080/reset-evaluation-factors',
        null,
        {
          headers: {
            'Content-Type': 'application/json'
          }
        }
    )

    valueChanged.value = false;

  } catch (e) {
    console.log(e.message)
  }
}



//
// FACTORS FUNCTIONS
//

// Revert current factor values to the standard values (Client)
async function discardFactorChanges() {
  pawnShieldValue.value = standardPawnShieldValue
  virtualMobilityValue.value = standardVirtualMobilityValue
  centerControlValue.value = standardCenterControlValue
  badBishopValue.value = standardBadBishopValue
  knightOutpostValue.value = standardKnightOutpostValue
  queenEarlyDevValue.value = standardQueenEarlyDevValue

  queenValue.value = standardQueenValue
  rookValue.value = standardRookValue
  bishopValue.value = standardBishopValue
  knightValue.value = standardKnightValue
  pawnValue.value = standardPawnValue

  await resetFactors() // Also reset on backend

  ignoreWatch = true
  valueChanged.value = false

  // Temporarily disable the watcher to prevent triggering valueChanged flag again
  setTimeout(() => {
    ignoreWatch = false
  }, 10)
}

// Update factor values in frontend and store the standard versions
function initFactors(factors) {
  pawnShieldValue.value = standardPawnShieldValue = factors.pawnShieldValue
  virtualMobilityValue.value = standardVirtualMobilityValue = factors.virtualMobilityValue
  centerControlValue.value = standardCenterControlValue = factors.centerControlValue
  badBishopValue.value = standardBadBishopValue = factors.badBishopValue
  knightOutpostValue.value = standardKnightOutpostValue = factors.knightOutpostValue
  queenEarlyDevValue.value = standardQueenEarlyDevValue = factors.queenEarlyDevValue

  queenValue.value = standardQueenValue = factors.queenValue
  rookValue.value = standardRookValue = factors.rookValue
  bishopValue.value = standardBishopValue = factors.bishopValue
  knightValue.value = standardKnightValue = factors.knightValue
  pawnValue.value = standardPawnValue = factors.pawnValue
}



//
// REACTIVE CSS CLASSES
//


// Determine CSS class for save button based on whether there are unsaved changes
function getSaveButtonClass() {
  return valueChanged.value ? "button button--save" : "button button--disabled"
}



</script>

<template>
  <div class="main-container">
    <Chessboard>
      <h2 class="text text--debug-text">DEBUG MODE</h2>
      <div class="container container--debug-container">

        <div class="container container--debug-tools-container">

          <div class="text text--information-text">
            Für genaue Werte nutze die Pfeiltasten <b><i class="bi bi-arrow-left-short"></i> und <i class="bi bi-arrow-right-short"></i></b> nach dem Auswählen eines Sliders.
            <br>
            Die Erklärungen der verschiedenen Konzepte können der <b>theory.md</b> entnommen werden.
          </div>


            <div class="debug-container debug-container--king-safety">

              <h3>King Safety</h3>

              <div class="debug-container debug-container--pawn-shield">
                <p>Pawn Shield: <b>{{pawnShieldValue}}</b></p>
                <input type="range" v-model="pawnShieldValue" min="0" max="30" step="0.1" />
              </div>

              <div class="debug-container debug-container--virtual-mobility">
                <p>Virtual Mobility: <b>{{virtualMobilityValue}}</b></p>
                <input type="range" v-model="virtualMobilityValue" min="0" max="30" step="0.1" />
              </div>


          <div class="debug-container debug-container--dynamic-control">
            <h3>Dynamic Control</h3>

            <div class="debug-container debug-container--bad-bishop">
              <p>Center Control: <b>{{centerControlValue}}</b></p>
              <input type="range" v-model="centerControlValue" min="0" max="30" step="0.1" />
            </div>

          </div>

          <div class="debug-container debug-container--evaluation-of-pieces">
            <h3>Evaluation Of Pieces</h3>

            <div class="debug-container debug-container--bad-bishop">
              <p>Bad Bishop: <b>{{badBishopValue}}</b></p>
              <input type="range" v-model="badBishopValue" min="0" max="30" step="0.1" />
            </div>


            <div class="debug-container debug-container--knight-outpost">
              <p>Knight Outpost: <b>{{knightOutpostValue}}</b></p>
              <input type="range" v-model="knightOutpostValue" min="0" max="30" step="0.1" />
            </div>


            <div class="debug-container debug-container--early-queen-dev">
              <p>Early Queen Development Penalty: <b>{{queenEarlyDevValue}}</b></p>
              <input type="range" v-model="queenEarlyDevValue" min="0" max="100" step="1" />
            </div>


            <div class="debug-container debug-container--evaluation-of-pieces">
              <h3>Piece Values</h3>

              <div class="debug-container debug-container--queen-value">
                <p>Queen Value: <b>{{queenValue}}</b></p>
                <input type="range" v-model="queenValue" min="0" max="1000" step="10" />
              </div>

              <div class="debug-container debug-container--rook-value">
                <p>Rook Value: <b>{{rookValue}}</b></p>
                <input type="range" v-model="rookValue" min="0" max="1000" step="10" />
              </div>


              <div class="debug-container debug-container--bishop-value">
                <p>Bishop Value: <b>{{bishopValue}}</b></p>
                <input type="range" v-model="bishopValue" min="0" max="1000" step="10" />
              </div>


              <div class="debug-container debug-container--knight-value">
                <p>Knight Value: <b>{{knightValue}}</b></p>
                <input type="range" v-model="knightValue" min="0" max="1000" step="10" />
              </div>


              <div class="debug-container debug-container--knight-value">
                <p>Pawn Value: <b>{{pawnValue}}</b></p>
                <input type="range" v-model="pawnValue" min="0" max="1000" step="10" />
              </div>

            </div>

          </div>
        </div>







          </div>



        <div class="container container--save-discard-container">
          <button :class="getSaveButtonClass()" @click="putFactors">Speichern</button>
          <button class="button button--discard" @click="discardFactorChanges">Zurücksetzen</button>
        </div>

      </div>
    </Chessboard>
  </div>
</template>

<style scoped>


input:hover {
  cursor: pointer;
}

i {
  color: rgba(0,0,0,0.6);
}


h3 {
  margin-top: 2vh;
}


/*
*
*CONTAINER
*
*/


.container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.debug-container {
  display: flex;
  justify-content: center;
  align-items: start;
}

.main-container {
  height: 100vh;
  width: 100vw;
  font-family: 'Jersey 25', Arial, sans-serif;

  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: row;
}


.container--debug-container {
  height: 40vh;
  padding: 5vh 1vw;

  background-color: beige;
  position: relative;
  border-radius: 10px;
  box-shadow: rgba(0,0,0,10%) 4px 4px;

  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  gap: 5vh;
}

.container--debug-tools-container{
  width: 100%;

  display: flex;
  flex-direction: column;
  align-items: start;
  justify-content: start;

  overflow-y: scroll;

  gap: 3vh;
}


.container--save-discard-container {
  width: 100%;
  justify-content: space-between;
}

.debug-container {

  display: flex;
  justify-content: start;
  align-items: start;
  flex-direction: column;

  gap: 1vh;
}


/* Hide scrollbar */

.container {
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none;  /* IE 10+ */
}

.container::-webkit-scrollbar {
  display: none; /* Chrome, Safari, Opera */
}




/*
*
* TEXT
*
 */

.text {
  text-align: center;
}

.text--debug-text {
  margin-top: 30px;
  margin-bottom: 10px;
}


.text--information-text {
  color: rgba(0,0,0,0.4);
  font-size: 80%;
}




/*
*
* BUTTONS
*
 */


.button {
  width: 8vw;
  height: 4vh;
  border: none;
  border-radius: 4px;

  font-family: 'Jersey 25', Arial, sans-serif;
}


.button--save {
  background-color: #9dfb8f;
}


.button:hover {
  cursor: pointer;
  filter: brightness(90%);
}

.button--discard {
  background-color: #f64040;
}



.button--disabled {
  background-color: lightgrey;
}


.button--disabled:hover {
  cursor: default;
  filter: brightness(100%);
}




</style>


