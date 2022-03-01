<template>
    <div class="item-header" v-if="item">
        <h2>
            <span v-if="item.dead">[dead]</span>
            {{ item.title }}
        </h2>
        <div>
            <span>{{ item.score }}</span>
            <span>{{ item.by }}</span>
            <span>{{ prettyTime }}</span>
            <span>{{ item.descendants }}</span>
        </div>
        <a :href="item.url">{{ item.url }}</a>
        <a :href="hnURL">{{ hnURL }}</a>
    </div>
</template>

<script lang="ts">
import {defineComponent, PropType} from "vue";
import {Item} from "../interfaces";
import {dateToText} from "../utils";


export default defineComponent({
    name: "Header",
    props: {
        item: {} as PropType<Item>,
    },
    computed: {
        hnURL(): string {
            if (!this.item) {
                return "#"
            }
            return "https://news.ycombinator.com/item?id=" + this.item.id
        },
        prettyTime(): string {
            if (!this.item) {
                return ""
            }
            return dateToText(this.item.time)
        }
    }
})
</script>
