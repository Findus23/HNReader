<template>
    <div id="mainwrapper">
        <section id="sidebar">
            <div id="sidebar-header">
                <router-link :to="{name: 'about'}">i</router-link>
                <button class="refresh" @click="refresh">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 65 65">
                        <g fill="currentColor">
                            <path d="M32.5 5a27.3 27.3 0 00-14.7 4.28l-5.75-5.75v16.11h16.11l-6.4-6.4a21.83 21.83 0 0110.74-2.81A22.1 22.1 0 0154.57 32.5c0 2.9-.57 5.66-1.6 8.2l4.74 2.76A27.53 27.53 0 0032.5 5zM43.23 51.75a21.82 21.82 0 01-10.73 2.82A22.1 22.1 0 0110.43 32.5c0-2.74.52-5.35 1.44-7.77l-4.73-2.85A27.53 27.53 0 0032.5 60c5.4 0 10.43-1.58 14.7-4.29l5.75 5.76V45.36H36.84l6.39 6.39z"/>
                        </g>
                    </svg>
                </button>
            </div>
            <Stories ref="stories"></Stories>
        </section>
        <section id="mainpane">
            <div id="mainpane-header"></div>

            <router-view></router-view>
            <header>
                <!--                <router-link :to="{name:'stories'}">Go to Home</router-link>-->
                <!--                <router-link :to="{name:'about'}">Go to About</router-link>-->
            </header>
        </section>
    </div>
</template>

<script lang="ts">
import {defineComponent, ref} from 'vue'
import Stories from "./views/Stories.vue";

export default defineComponent({
    components: {Stories},
    data() {
        return {
            message: "ffd Vue"
        };
    },
    methods: {
        refresh(): void {
            (this.$refs.stories as typeof Stories).refreshStories()
        }
    }
});
</script>
