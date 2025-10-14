import type { SetupContext } from "vue";
import type { PaginationProps } from "tdesign-vue-next";
import { computed } from "vue";
import type { TTableData } from "../types";

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
