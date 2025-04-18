<script setup>
import Chessboard from "frontend/src/components/Chessboard.vue";
import {onMounted} from "vue";
import axios from "axios";



// Make sure standard evaluation factors are loaded
onMounted(() => {
  const resetFactorsToStandard = async () => {
    await resetFactors()
    console.log("Evaluation factors reset")

  }
  resetFactorsToStandard()
})

// Reset factors (Backend)
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

    console.log(response)

  } catch (e) {
    console.log(e.message)
  }
}


</script>

<template>
    <div class="main-container">
      <Chessboard>
      </Chessboard>
    </div>
</template>

<style scoped>

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
  flex-direction: row;
}


</style>
