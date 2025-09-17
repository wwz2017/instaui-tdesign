<script setup lang="ts">
import { Anchor } from "tdesign-vue-next";
import { useAttrs, useSlots } from "vue";
import { withDefaultAffixProps, withDefaultContainer } from "./anchor";

defineOptions({ inheritAttrs: false });

const attrs = useAttrs();
const slots = useSlots();
const affixProps = withDefaultAffixProps(attrs);
const container = withDefaultContainer(attrs);
</script>

<template>
  <Anchor v-bind="attrs" :container="container" :affix-props="affixProps">
    <template v-for="(_, name) in slots" v-slot:[name]="slotProps" :key="name">
      <slot :name="name" v-bind="slotProps" />
    </template>
  </Anchor>
</template>

<style scoped></style>
