<template>
    <div class="stories">
        <div v-for="story in stories" :key="story.id" :class="{storywrapper:true, active:isActiveStory(story)}">
            <router-link :to="{name:'reader',params:{item:story.id}}" class="story">
                <h3>{{ story.title }}</h3>
                <div class="info">{{ story.by }} {{ dateToText(story.time) }}</div>
                <div class="link">{{ story.url }}</div>
                <div v-if="story.type==='job'">Job</div>
            </router-link>
            <router-link :to="{name:'comments',params:{item:story.id}}" class="storycomments">
                <div class="numcomments">{{ story.descendants }}</div>
                <div class="points">{{ story.score }}</div>
            </router-link>
        </div>
        <div class="load-more storywrapper" @click="loadStory">
            <div>Load More</div>
        </div>
        <!--        <pre class="debug"><code>{{ stories }}</code></pre>-->
    </div>
</template>

<script lang="ts">
import {defineComponent} from "vue";
import {Item} from "../interfaces";
import {dateToText} from "../utils";

const STORIES_PER_LOAD = 25;

export default defineComponent({
    name: "Stories",
    data() {
        return {
            stories: [] as Item[],
        }
    },
    methods: {
        loadStory(): void {
            fetch("/api/topstories?" + new URLSearchParams({
                offset: this.stories.length.toString()
            }))
              .then(response => {
                  if (response.ok) {
                      return response.json()
                  }
                  return Promise.reject(response)
              })
              .then(data => (this.stories.push(...data)))
        },
        refreshStories(): void {
            this.stories = [] as Item[]
            this.loadStory()
        },
        isActiveStory(item: Item): boolean {
            return this.$route.params.item === item.id.toString()
        },
        dateToText(timestamp: number): string {
            return dateToText(timestamp)
        }
    },
    mounted() {
        this.loadStory()
    },
})
</script>
