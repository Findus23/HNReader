<template>
    <div class="comments">
        <Header :item="story"></Header>
        <div v-if="loading">LOADING</div>
        <comment :item="story" :original-author="story.by" :first-layer="true"></comment>
        <!--        <pre class="debug"><code>{{ story }}</code></pre>-->
    </div>
</template>

<script lang="ts">
import {defineComponent} from "vue";
import {Item} from "../interfaces";
import Comment from "../components/Comment.vue";
import Header from "../components/Header.vue";

export default defineComponent({
    name: "Comments",
    props: {
        item: String,
    },
    data() {
        return {
            story: {} as Item,
            loading: false
        }
    },
    methods: {
        loadComments(id?: string): void {
            if (typeof id === "undefined") {
                id = this.item
            }
            this.loading = true
            fetch("/api/item/" + id)
              .then(response => {
                  if (response.ok) {
                      return response.json()
                  }
                  return Promise.reject(response)
              })
              .then(data => (this.story = data))
              .then(a => {
                  this.loading = false;
                  document.title = this.story.title
              })

        }
    },
    mounted(): void {
        this.loadComments()
    },
    components: {
        Header,
        "comment": Comment
    },
    watch: {
        "$route.params.item": function (id: string) {
            this.loadComments(id)
        }
    }
})
</script>
