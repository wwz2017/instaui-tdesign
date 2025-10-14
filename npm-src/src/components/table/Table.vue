<script setup lang="ts">
import * as TDesign from "tdesign-vue-next";
import { useConfig } from "tdesign-vue-next";
import { useAttrs, useSlots } from "vue";
import { useTableData } from "./hooks/table-data";
import { useTableColumnsWithInfer } from "./hooks/columns-infer";
import { usePagination } from "./hooks/pagination";
import { useTableSort } from "./hooks/sort";
import { useTableFilter } from "./hooks/filter";
import { withDefaultAttrs } from "./hooks/default-attrs";
import { defaultHeaderSlotInfos } from "./hooks/header-slot";

defineOptions({ inheritAttrs: false });

const attrs = useAttrs();
const { t, globalConfig } = useConfig("table");

const { tableData, orgData, registerRowsHandler } = useTableData(attrs);
const [columnsWithInfer, registerColumnsHandler] = useTableColumnsWithInfer({
  tableData,
  attrs,
});

const pagination = usePagination({ tableData, attrs });
const { sort, onSortChange, multipleSort } = useTableSort({
  registerRowsHandler,
  attrs,
  registerColumnsHandler,
  columns: columnsWithInfer,
});

const { onFilterChange, filterValue, resetFilters, filterResultText } =
  useTableFilter({
    tableData: orgData,
    registerRowsHandler,
    attrs,
    registerColumnsHandler,
    columns: columnsWithInfer,
    tdesignGlobalConfig: globalConfig.value,
  });

const bindAttrs = withDefaultAttrs({ attrs });

const slots = useSlots();
const headerSlotInfos = defaultHeaderSlotInfos(slots, columnsWithInfer);
</script>

<template>
  <TDesign.Table
    v-bind="bindAttrs"
    :pagination="pagination"
    :sort="sort"
    :data="tableData"
    :columns="columnsWithInfer"
    :filter-value="filterValue"
    @sort-change="onSortChange"
    @filter-change="onFilterChange"
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

    <!-- filter row slot -->

    <template #filter-row>
      <div>
        <span>{{
          t(globalConfig.searchResultText, {
            result: filterResultText(),
            count: tableData.length,
          })
        }}</span>

        <TDesign.Button theme="primary" variant="text" @click="resetFilters">{{
          globalConfig.clearFilterResultButtonText
        }}</TDesign.Button>
      </div>
    </template>

    <!-- other slots -->
    <template v-for="(_, name) in slots" v-slot:[name]="slotProps" :key="name">
      <slot :name="name" v-bind="slotProps" />
    </template>
  </TDesign.Table>
</template>
