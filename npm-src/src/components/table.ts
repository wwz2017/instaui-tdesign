import type { ComputedRef, Ref, SetupContext } from "vue";
import type { PaginationProps, TableProps } from "tdesign-vue-next";
import { computed, ref, watch } from "vue";

type TRequiredTableColumns = NonNullable<TableProps["columns"]>;
const m_defaultTableAttrs = {
  hover: true,
  bordered: true,
  tableLayout: "auto",
  showSortColumnBgColor: true,
};

export function usePagination(attrs: SetupContext["attrs"]) {
  return computed(() => {
    const { pagination, data = [] } = attrs as {
      pagination: PaginationProps | boolean | number;
      data: any[];
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
      total: data.length,
      ...realPagination,
    };
  });
}

export function withDefaultAttrs(attrs: SetupContext["attrs"]) {
  let sort = ref(attrs.sort as TableProps["sort"]);
  const tableData = ref([...((attrs.data as TableProps["data"]) ?? [])]);

  watch(
    () => attrs.data,
    (data) => {
      tableData.value = [...(data as any[])];
    }
  );

  const columnsWithInfer = computed(() => {
    const needInferColumns = !attrs.columns && tableData.value.length > 0;
    const result = needInferColumns
      ? inferColumns(tableData.value)
      : attrs.columns ?? [];
    return result as TRequiredTableColumns;
  });

  const {
    onSortChange,
    onDataChange,
    columns: realColumns,
    multipleSort,
  } = useTableSort({
    sort,
    tableData,
    columns: columnsWithInfer,
  });

  const bindAttrs = computed(() => {
    return {
      ...m_defaultTableAttrs,
      ...attrs,
    } as TableProps;
  });

  return {
    sort,
    tableData,
    onSortChange,
    onDataChange,
    columns: realColumns,
    multipleSort,
    bindAttrs,
  };
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

function makeDefaultSorter(column: { colKey: string }) {
  const key = column.colKey;

  return (a: Record<string, any>, b: Record<string, any>) => {
    const v1 = a[key];
    const v2 = b[key];

    // null/undefined last
    if (v1 == null && v2 == null) return 0;
    if (v1 == null) return 1;
    if (v2 == null) return -1;

    // number
    if (typeof v1 === "number" && typeof v2 === "number") {
      return v1 - v2;
    }

    // Date
    if (v1 instanceof Date && v2 instanceof Date) {
      return v1.getTime() - v2.getTime();
    }

    // string
    if (typeof v1 === "string" && typeof v2 === "string") {
      return v1.localeCompare(v2, undefined, { numeric: true });
    }

    return String(v1).localeCompare(String(v2), undefined, { numeric: true });
  };
}

function useTableSort(options: {
  tableData: Ref<TableProps["data"]>;
  sort: Ref<TableProps["sort"]>;
  columns: ComputedRef<TRequiredTableColumns>;
}): {
  onSortChange: TableProps["onSortChange"];
  onDataChange: TableProps["onDataChange"];
  columns: ComputedRef<TRequiredTableColumns>;
  multipleSort: ComputedRef<boolean>;
} {
  const { tableData, sort, columns } = options;

  const enhancedColumns = computed(() => {
    return columns.value.map((col) => {
      if (col.sorter === true) {
        return {
          ...col,
          sorter: makeDefaultSorter(col as { colKey: string }),
        };
      }
      return col;
    });
  });

  const needSort = computed(() =>
    enhancedColumns.value?.some((col) => col.sorter)
  );

  const multipleSort = computed(
    () => enhancedColumns.value.filter((col) => col.sorter).length > 1
  );

  const onSortChange: TableProps["onSortChange"] = (nextSort, options) => {
    if (!needSort.value) {
      return;
    }
    sort.value = nextSort;
    tableData.value = [...(options.currentDataSource ?? [])];
  };

  const onDataChange: TableProps["onDataChange"] = (newData) => {
    tableData.value = newData;
  };

  return {
    onSortChange,
    onDataChange,
    columns: enhancedColumns,
    multipleSort,
  };
}
