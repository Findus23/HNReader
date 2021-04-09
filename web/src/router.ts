import {createRouter, createWebHashHistory, createWebHistory} from "vue-router";
import About from './views/About.vue';
import Comments from "./views/Comments.vue";
import Reader from "./views/Reader.vue";
import {isInStandaloneMode} from "./utils";

let history;

if (isInStandaloneMode()) {
    history = createWebHashHistory()
} else {
    history = createWebHistory()
}

export const router = createRouter({
    history: history,
    routes: [
        {path: '/', name: "about", component: About},
        {path: "/comments/:item", name: "comments", component: Comments, props: true},
        {path: "/read/:item", name: "reader", component: Reader, props: true},
    ]
})
