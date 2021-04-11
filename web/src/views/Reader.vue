<template>
    <div class="reader">
        <div v-if="loading">loading article</div>
        <h1>{{ readerData.title }}</h1>
        <div v-if="!loading">{{ prettyDate }}</div>
        <div>{{ prettyAuthors }}</div>
        <div class="reader-html" v-html="readerData.html"></div>
<!--        <pre class="debug"><code>{{ readerData }}</code></pre>-->
    </div>
</template>

<script lang="ts">
import {defineComponent} from "vue";
import {ReaderData} from "../interfaces";

export default defineComponent({
    name: "Reader",
    props: {
        item: String,
    },
    data() {
        return {
            readerData: {} as ReaderData,
            loading: false
        }
    },
    methods: {
        loadReader(id?: string): void {
            if (typeof id === "undefined") {
                id = this.item
            }
            this.loading = true
            fetch("/api/read/" + id)
              .then(response => {
                  if (response.ok) {
                      return response.json()
                  }
                  return Promise.reject(response)
              })
              .then(data => (this.readerData = data))
              .then(a => {
                  this.loading = false;
                  document.title = this.readerData.title
              })

        }
    },
    mounted() {
        this.loadReader()
    },
    computed: {
        prettyDate(): string {
            if (!this.readerData) {
                return ""
            }
            const date = new Date(this.readerData.date)
            return date.toLocaleString()
        },
        prettyAuthors(): string {
            if (!this.readerData || !this.readerData.authors) {
                return ""
            }
            return this.readerData.authors.join(", ")
        }
    },
    watch: {
        "$route.params.item": function (id: string) {
            this.loadReader(id)
        }
    }

})
</script>
