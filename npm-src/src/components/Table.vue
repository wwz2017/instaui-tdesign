<script setup lang="ts">
import * as TDesign from "tdesign-vue-next";
import { useAttrs, useSlots } from "vue";
import { usePagination, withDefaultAttrs } from "./table";

defineOptions({ inheritAttrs: false });

const attrs = useAttrs();
const pagination = usePagination(attrs);
const {
  sort,
  onSortChange,
  onDataChange,
  columns,
  multipleSort,
  tableData,
  bindAttrs,
} = withDefaultAttrs(attrs);

const slots = useSlots();
</script>

<template>
  <TDesign.Table
    v-bind="bindAttrs"
    :pagination="pagination"
    :sort="sort"
    :data="tableData"
    :columns="columns"
    @sort-change="onSortChange"
    @data-change="onDataChange"
    :multiple-sort="multipleSort"
  >
    <template v-for="(_, name) in slots" v-slot:[name]="slotProps" :key="name">
      <slot :name="name" v-bind="slotProps" />
    </template>
  </TDesign.Table>
</template>
