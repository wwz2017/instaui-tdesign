<script setup lang="ts">
import * as TDesign from "tdesign-vue-next";
import { computed, useAttrs, useSlots } from "vue";

defineOptions({ inheritAttrs: false });
const props = defineProps<{ options?: any[] }>();

const attrs = useAttrs();
const slots = useSlots();

const realOptions = computed(() => {
  const options = props.options;

  if (!options) return undefined;

  if (Array.isArray(options)) {
    if (options.length === 0) {
      return undefined;
    }

    return options.map((item) =>
      typeof item === "string" || typeof item === "number"
        ? { label: item, value: item }
        : item
    );
  }

  throw new Error("options must be an array");
});
</script>

<template>
  <TDesign.RadioGroup v-bind="attrs" :options="realOptions">
    <template v-for="(_, name) in slots" v-slot:[name]="slotProps" :key="name">
      <slot :name="name" v-bind="slotProps" />
    </template>
  </TDesign.RadioGroup>
</template>

<style scoped></style>
