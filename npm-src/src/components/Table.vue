<script setup lang="ts">
import * as TDesign from "tdesign-vue-next";
import { useAttrs, useSlots } from "vue";
import {
  defaultHeaderSlotInfos,
  usePagination,
  withDefaultAttrs,
} from "./table";

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
const headerSlotInfos = defaultHeaderSlotInfos(slots, columns);
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
    <!-- column title slot -->
    <template
      v-for="info in headerSlotInfos"
      v-slot:[info.slotName]
      :key="info.slotName"
    >
      {{ info.content }}
    </template>

    <template v-for="(_, name) in slots" v-slot:[name]="slotProps" :key="name">
      <slot :name="name" v-bind="slotProps" />
    </template>
  </TDesign.Table>
</template>
