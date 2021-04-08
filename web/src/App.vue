<template>
    <div id="mainwrapper">
        <section id="sidebar">
            <div id="sidebar-header">
                <router-link :to="{name: 'about'}">i</router-link>
            </div>
            <Stories></Stories>
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
import {defineComponent} from 'vue'
import Stories from "./views/Stories.vue";

export default defineComponent({
    components: {Stories},
    data() {
        return {
            message: "ffd Vue"
        };
    }
});
</script>
