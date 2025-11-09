import type { SetupContext } from "vue";
import type { TableProps } from "tdesign-vue-next";
import { computed, ref } from "vue";
import type { TTableRowsHandler } from "../types";

export function useTableData(attrs: SetupContext["attrs"]) {
  const handlers = [] as TTableRowsHandler[];

  const orgData = computed(() => (attrs.data as TableProps["data"]) ?? []);
  const forceUpdateFlag = ref(0);

  const tableData = computed(() => {
    // oxlint-disable-next-line no-unused-expressions
    forceUpdateFlag.value;
    const initData = orgData.value;
    return handlers.reduce((data, handler) => handler(data), initData);
  });

  const registerRowsHandler = (handler: TTableRowsHandler) => {
    handlers.push(handler);
  };

  function notifyTableDataChange() {
    forceUpdateFlag.value++;
  }

  return {
    tableData,
    orgData,
    registerRowsHandler,
    notifyTableDataChange,
  };
}
