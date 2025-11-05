<script setup lang="ts">
import * as TDesign from "tdesign-vue-next";
import { useAttrs, useSlots } from "vue";
import { useFormatRequest } from "./format-request";

defineOptions({ inheritAttrs: false });

const attrs = useAttrs();
const slots = useSlots();
const formatRequest = useFormatRequest(attrs);
</script>

<template>
  <TDesign.Upload v-bind="attrs" :formatRequest="formatRequest">
    <template v-for="(_, name) in slots" v-slot:[name]="slotProps" :key="name">
      <slot :name="name" v-bind="slotProps" />
    </template>
  </TDesign.Upload>
</template>

<style scoped></style>
