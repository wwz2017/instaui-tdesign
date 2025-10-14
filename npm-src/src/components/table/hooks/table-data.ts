import type { SetupContext } from "vue";
import type { TableProps } from "tdesign-vue-next";
import { computed } from "vue";
import type { TTableRowsHandler } from "../types";

export function useTableData(attrs: SetupContext["attrs"]) {
  const handlers = [] as TTableRowsHandler[];

  const orgData = computed(() => (attrs.data as TableProps["data"]) ?? []);

  const tableData = computed(() => {
    const initData = orgData.value;
    return handlers.reduce((data, handler) => handler(data), initData);
  });

  const registerRowsHandler = (handler: TTableRowsHandler) => {
    handlers.push(handler);
  };

  return {
    tableData,
    orgData,
    registerRowsHandler,
  };
}
