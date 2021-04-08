<template>
    <div v-if="!item.deleted">
        <div :class="{comment:true,fromauthor:item.by===originalAuthor}" v-if="!firstLayer">
            <div class="comment-header" @click="toogleCollapse">
                <div class="author">{{ item.by }}</div>
                <div class="time">{{ dateToText(item.time) }}</div>
            </div>
            <div class="text" v-html="item.text" v-if="!collapsed"></div>
        </div>
        <div v-for="kid in item.kids" :key="kid.id" class="kids" v-if="!collapsed">
            <comment :item="kid" :original-author="originalAuthor"></comment>
        </div>
    </div>
</template>

<script lang="ts">
import {defineComponent, PropType} from "vue";
import {Item} from "../interfaces";
import {dateToText} from "../utils";


export default defineComponent({
    name: "Comment",
    props: {
        item: {} as PropType<Item>,
        originalAuthor: String,
        firstLayer: {
            type: Boolean,
            default: () => false
        }
    },
    data() {
        return {
            collapsed: false
        }
    },
    methods: {
        toogleCollapse(): void {
            console.log("toggle")
            this.collapsed = !this.collapsed;
        },
        dateToText(num: number): string {
            return dateToText(num)
        }
    }
})
</script>
