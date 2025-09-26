import type { Ref, SetupContext } from "vue";
import type { PaginationProps, TableProps, TableSort } from "tdesign-vue-next";
import { computed, ref } from "vue";

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
  const tableData = ref(attrs.data as TableProps["data"]);

  const bindAttrs = computed(() => {
    const { columns, data = [], ...rest } = attrs as unknown as TableProps;

    const needInferColumns = !columns && data.length > 0;
    const columnsWithInfer = needInferColumns ? inferColumns(data) : columns;
    const {
      onSortChange,
      columns: realColumns,
      multipleSort,
    } = useTableSort({
      sort,
      tableData,
      columns: columnsWithInfer,
    });

    return {
      hover: true,
      bordered: true,
      tableLayout: "auto",
      columns: realColumns,
      onSortChange,
      multipleSort,
      showSortColumnBgColor: true,
      ...rest,
    } as TableProps;
  });

  return {
    sort,
    tableData,
    bindAttrs,
  };
}

function inferColumns(data: any[]): TableProps["columns"] {
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
  columns: TableProps["columns"];
}): {
  onSortChange: TableProps["onSortChange"] | undefined;
  columns: TableProps["columns"];
  multipleSort: boolean;
} {
  const { tableData, sort, columns } = options;
  let needSort = false;
  let sortCount = 0;

  const enhancedColumns = columns?.map((col) => {
    if (col.sorter === true) {
      needSort = true;
      sortCount++;
      return {
        ...col,
        sorter: makeDefaultSorter(col as { colKey: string }),
      };
    }
    return col;
  });

  const onSortChange: TableProps["onSortChange"] | undefined = needSort
    ? (nextSort, options) => {
        sort.value = nextSort;
        tableData.value = options.currentDataSource;
      }
    : undefined;

  return {
    onSortChange,
    columns: enhancedColumns,
    multipleSort: sortCount > 1,
  };
}
