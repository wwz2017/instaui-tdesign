import type { ComputedRef, SetupContext } from "vue";
import type {
  PaginationProps,
  PrimaryTableCol,
  TableProps,
  TableRowData,
} from "tdesign-vue-next";
import { computed, ref } from "vue";
import { orderBy as _orderBy, uniqBy as _uniqBy } from "lodash-es";

type TRequiredTableColumns = NonNullable<TableProps["columns"]>;
const m_defaultTableAttrs = {
  hover: true,
  bordered: true,
  tableLayout: "auto",
  showSortColumnBgColor: true,
};

type TTableData = ComputedRef<any[]>;
type TTableRowsHandler = (data: any[]) => any[];

type TTableColumns = (PrimaryTableCol<TableRowData> & {
  label: string;
  name: string;
})[];

type TTableColumnsWithInfer = ComputedRef<TTableColumns>;
type TTableColumnHandler = (columns: TTableColumns) => TTableColumns;

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

export function usePagination(options: {
  tableData: TTableData;
  attrs: SetupContext["attrs"];
}) {
  const { tableData, attrs } = options;

  return computed(() => {
    const { pagination } = attrs as {
      pagination: PaginationProps | boolean | number;
    };

    let realPagination = undefined;

    if (typeof pagination === "boolean") {
      if (!pagination) {
        return undefined;
      }

      realPagination = {
        defaultPageSize: 10,
      };
    }

    if (typeof pagination === "number" && pagination > 0) {
      realPagination = {
        defaultPageSize: pagination,
      };
    }

    if (typeof pagination === "object" && pagination !== null) {
      realPagination = pagination;
    }

    return {
      defaultCurrent: 1,
      total: tableData.value.length,
      ...realPagination,
    };
  });
}

export function useTableSort(options: {
  registerRowsHandler: (handler: TTableRowsHandler) => void;
  attrs: SetupContext["attrs"];
  columns: TTableColumnsWithInfer;
  registerColumnsHandler: (handler: TTableColumnHandler) => void;
}) {
  const { attrs, columns, registerRowsHandler } = options;
  let sort = ref(attrs.sort as TableProps["sort"]);

  const needSort = computed(() => columns.value?.some((col) => col.sorter));

  const multipleSort = computed(
    () => columns.value.filter((col) => col.sorter).length > 1
  );

  registerRowsHandler((rows) => {
    if (!sort.value) {
      return rows;
    }

    const sortInfos = Array.isArray(sort.value)
      ? sort.value
      : ([sort.value] as {
          sortBy: string;
          descending: boolean;
        }[]);

    const sortFields = sortInfos.map((item) => item.sortBy);
    const sortOrders = sortInfos.map((item) =>
      item.descending ? "desc" : "asc"
    );

    return _orderBy(rows, sortFields, sortOrders);
  });

  const onSortChange: TableProps["onSortChange"] = (newSort) => {
    if (!needSort.value) {
      return;
    }
    sort.value = newSort;
  };

  return {
    onSortChange,
    multipleSort,
    sort,
  };
}

export function useTableFilter(options: {
  tableData: TTableData;
  registerRowsHandler: (handler: TTableRowsHandler) => void;
  attrs: SetupContext["attrs"];
  columns: TTableColumnsWithInfer;
  registerColumnsHandler: (handler: TTableColumnHandler) => void;
  tdesignGlobalConfig: Record<string, any>;
}) {
  const { tableData, registerColumnsHandler, registerRowsHandler, columns } =
    options;

  registerColumnsHandler(
    (columns) =>
      columns.map((column) =>
        normalizeTableFilterRecord(
          column,
          tableData,
          options.tdesignGlobalConfig
        )
      ) as TTableColumns
  );

  const filterValue = ref<TableProps["filterValue"]>();

  const colKey2Info = new Map(columns.value.map((col) => [col.colKey, col]));

  registerRowsHandler((rows) => {
    if (!filterValue.value) {
      return rows;
    }

    const filterInfos = Object.keys(filterValue.value).map((key) => {
      const value = (filterValue.value as any)[key] as any;
      const type = colKey2Info.get(key)!.filter!.type!;

      return {
        key,
        value,
        type,
      };
    });

    return rows.filter((row) => {
      return filterInfos.every((info) => {
        if (info.type === "multiple") {
          const filterValues = info.value as string[];
          if (filterValues.length === 0) return true;
          return filterValues.includes(row[info.key]);
        }

        if (info.type === "single") {
          const filterValue = info.value as any;
          if (!filterValue) return true;
          return row[info.key] === filterValue;
        }

        if (info.type === "input") {
          const filterValue = info.value as string;
          if (!filterValue) return true;
          return row[info.key].toString().includes(filterValue);
        }

        throw new Error("not support filter type");
      });
    });
  });

  const onFilterChange: TableProps["onFilterChange"] = (filters, ctx) => {
    if (!ctx.col) {
      filterValue.value = undefined;
      return;
    }
    filterValue.value = {
      ...filters,
    };
  };

  function resetFilters() {
    filterValue.value = undefined;
  }

  function filterResultText(): string | null {
    if (!filterValue.value) return null;

    return Object.keys(filterValue.value)
      .map((key) => {
        const label = colKey2Info.get(key)!.label;
        const values = filterValue.value![key];
        if (values.length === 0) {
          return "";
        }
        return `${label}: ${JSON.stringify(values)}`;
      })
      .join("; ");
  }

  return {
    onFilterChange,
    filterValue,
    resetFilters,
    filterResultText,
  };
}

export function withDefaultAttrs(options: { attrs: SetupContext["attrs"] }) {
  const { attrs } = options;

  const bindAttrs = computed(() => {
    return {
      ...m_defaultTableAttrs,
      ...attrs,
    } as TableProps;
  });

  return bindAttrs;
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

function normalizeTableFilterRecord(
  column: Record<string, any>,
  tableData: TTableData,
  tdesignGlobalConfig: Record<string, any>
) {
  const hasFilter = "filter" in column;

  if (!hasFilter) {
    return column;
  }

  if (!("type" in column.filter)) throw new Error("filter type is required");

  const { colKey } = column;
  const { type } = column.filter as { type: "multiple" | "single" | "input" };

  if (type === "multiple") {
    const list = _uniqBy(tableData.value, colKey).map((item) => {
      return {
        label: item[colKey],
        value: item[colKey],
      };
    });

    const newFilter = {
      resetValue: [],
      list: [
        { label: tdesignGlobalConfig.selectAllText, checkAll: true },
        ...list,
      ],
      ...column.filter,
    };

    return {
      ...column,
      filter: newFilter,
    };
  }

  if (type === "single") {
    const list = _uniqBy(tableData.value, colKey).map((item) => {
      return {
        label: item[colKey],
        value: item[colKey],
      };
    });

    const newFilter = {
      resetValue: null,
      list,
      showConfirmAndReset: true,
      ...column.filter,
    };

    return {
      ...column,
      filter: newFilter,
    };
  }

  if (type === "input") {
    const newFilter = {
      resetValue: "",
      confirmEvents: ["onEnter"],
      showConfirmAndReset: true,
      ...column.filter,
      props: {
        ...column.filter?.props,
      },
    };

    return {
      ...column,
      filter: newFilter,
    };
  }

  throw new Error("not support filter type");
}

export function defaultHeaderSlotInfos(
  slots: SetupContext["slots"],
  columns: ComputedRef<TRequiredTableColumns>
) {
  return computed(() => {
    const excludeNames = Object.keys(slots).filter((name) =>
      name.startsWith("header-cell-")
    );

    return columns.value
      .filter((col: any) => !excludeNames.includes(col.title))
      .map((col: any) => ({
        slotName: `header-cell-${col.name}`,
        content: col.label ?? col.colKey,
      }));
  });
}
