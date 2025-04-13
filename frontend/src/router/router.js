// router/index.ts oder router.js
import { createRouter, createWebHistory } from 'vue-router'
import NormalMode from "frontend/src/components/NormalMode.vue"
import DebugMode from "frontend/src/components/DebugMode.vue"
import StartScreen from "../components/StartScreen.vue";


const routes = [
    { path: '/', component: StartScreen},
    { path: '/normal-mode', component: NormalMode },
    { path: '/debug-mode', component: DebugMode },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router