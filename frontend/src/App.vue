<script setup>
import Background from "frontend/src/components/Background.vue";
import { useRouter } from 'vue-router'
import Music from "./components/Music.vue";


const router = useRouter()

function goToNormalMode() {
  router.push("/normal-mode");
}

function goToDebugMode() {
  router.push("/debug-mode");
}

</script>

<template>
  <Background>
    <div class="container container--music-container" ref="musicContainer">
      <Music />
    </div>
    <div class="container container--name-container">
      <p><b>3VAL</b> - Chess Engine</p>
      <p>entwickelt von Tim Terbach</p>
    </div>
    <router-view/>
  </Background>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=DynaPuff:wght@400..700&family=Jersey+25&display=swap');

p{
  font-family: 'Jersey 25', Arial, sans-serif;
  font-size: 110%;
  color: rgba(0,0,0,0.4);
}


.container--music-container {
  position: absolute;
  top: 1vw;
  right: 1vw;
  z-index: 101;
}

.container--name-container {
  position: absolute;
  top: 1vw;
  left: 1vw;
  z-index: 101;
}



</style>
