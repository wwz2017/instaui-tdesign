import type { SetupContext } from "vue";
import type { PaginationProps, TableProps } from "tdesign-vue-next";
import { computed } from "vue";

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
  return computed(
    () =>
      ({
        hover: true,
        bordered: true,
        tableLayout: "auto",
        ...attrs,
      } as TableProps)
  );
}
