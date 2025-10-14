import type { SetupContext } from "vue";
import type { TableProps } from "tdesign-vue-next";
import { computed } from "vue";
import type {
  TRequiredTableColumns,
  TTableColumnHandler,
  TTableColumns,
  TTableColumnsWithInfer,
  TTableData,
  TTableRowsHandler,
} from "../types";

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

export function useTableColumnsWithInfer(options: {
  tableData: TTableData;
  attrs: SetupContext["attrs"];
}) {
  const { tableData, attrs } = options;
  const handlers = [] as TTableColumnHandler[];

  const columnsWithInfer = computed(() => {
    const needInferColumns = !attrs.columns && tableData.value.length > 0;
    let result = (
      needInferColumns ? inferColumns(tableData.value) : attrs.columns ?? []
    ) as TTableColumns;

    result = result.map(normalizeTableColumnRecord) as TTableColumns;

    for (const handler of handlers) {
      result = handler(result);
    }

    return result;
  });

  function registerHandler(handler: TTableColumnHandler) {
    handlers.push(handler);
  }

  return [columnsWithInfer, registerHandler] as [
    TTableColumnsWithInfer,
    (handler: TTableColumnHandler) => void
  ];
}

function inferColumns(data: any[]): TRequiredTableColumns {
  const firstRow = data[0];

  const keys = Object.keys(firstRow);

  return keys.map((key) => {
    return {
      colKey: key,
      title: key,
      sorter: true,
    };
  });
}

function normalizeTableColumnRecord(
  column: Record<string, any>
): Record<string, any> {
  const colName = column.name ?? column.colKey;
  const title = `header-cell-${colName}`;
  const cell = `body-cell-${colName}`;
  const label = column.label ?? column.colKey;

  return {
    ...column,
    name: colName,
    label,
    title,
    cell,
  };
}
