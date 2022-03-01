<template>
    <div v-if="item && !item.deleted">
        <div :class="{comment:true, fromauthor:item.by===originalAuthor, textpost:textPost, dead:item.dead}" v-if="!firstLayer">
            <div class="comment-header" @click="toogleCollapse">
                <div class="author">{{ item.by }}</div>
                <div class="time">{{ prettyTime }}</div>
                <div v-if="item.dead">[dead]</div>
            </div>
            <div class="text" v-html="item.text" v-if="!collapsed"></div>
        </div>
        <div v-for="kid in item.kids" :key="kid.id" class="kids" v-if="!collapsed && !textPost">
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
        },
        textPost: {
            type: Boolean,
            default: () => false
        }
    },
    data() {
        return {
            collapsed: false
        }
    },
    computed: {
        prettyTime(): string {
            if (!this.item) {
                return ""
            }
            return dateToText(this.item.time)
        }
    },
    methods: {
        toogleCollapse(): void {
            this.collapsed = !this.collapsed;
        },
    }
})
</script>
