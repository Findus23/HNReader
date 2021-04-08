<template>
    <div class="item-header">
        <h2>{{ item.title }}</h2>
        <a :href="item.url">{{ item.url }}</a>
        <a :href="hnURL">{{ hnURL }}</a>
    </div>
</template>

<script lang="ts">
import {defineComponent, PropType} from "vue";
import {Item} from "../interfaces";


export default defineComponent({
    name: "Header",
    props: {
        item: {} as PropType<Item>,
    },
    computed: {
        hnURL(): string {
            return "https://news.ycombinator.com/item?id=" + this.item.id
        }
    }
})
</script>
