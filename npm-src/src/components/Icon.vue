<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{
  name: string;
  size?: string;
  color?: string;
  prefix?: string;
}>();

const icon = computed(() => {
  const [_, name] = props.name.split(":");
  if (name) {
    return props.name;
  }

  return `${props.prefix || "tdesign"}:${props.name}`;
});
</script>

<template>
  <component
    class="t-icon"
    is="icon"
    :icon="icon"
    :size="size"
    :color="color"
  />
</template>

<style scoped></style>
