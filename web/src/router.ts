import {createRouter, createWebHistory} from "vue-router";
import Stories from './views/Stories.vue';
import About from './views/About.vue';
import Comments from "./views/Comments.vue";
import Reader from "./views/Reader.vue";

export const router = createRouter({
    history: createWebHistory(),
    routes: [
        {path: '/', name: "about", component: About},
        {path: "/comments/:item", name: "comments", component: Comments, props: true},
        {path: "/read/:item", name: "reader", component: Reader, props: true},
    ]
})
