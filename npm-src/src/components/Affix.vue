<script setup lang="ts">
import * as TDesign from "tdesign-vue-next";
import { useAttrs, useSlots } from "vue";
import { withDefaultContainer } from "./affix";

defineOptions({ inheritAttrs: false });

const attrs = useAttrs();
const slots = useSlots();
const container = withDefaultContainer(attrs);
</script>

<template>
  <TDesign.Affix v-bind="attrs" :container="container">
    <template v-for="(_, name) in slots" v-slot:[name]="slotProps" :key="name">
      <slot :name="name" v-bind="slotProps" />
    </template>
  </TDesign.Affix>
</template>

<style scoped></style>
