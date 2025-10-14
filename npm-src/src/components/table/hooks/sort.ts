import type { SetupContext } from "vue";
import type { TableProps } from "tdesign-vue-next";
import { computed, ref } from "vue";
import { orderBy as _orderBy } from "lodash-es";
import type {
  TTableColumnHandler,
  TTableColumnsWithInfer,
  TTableRowsHandler,
} from "../types";

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
