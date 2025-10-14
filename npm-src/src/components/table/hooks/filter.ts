import { type TableProps, DateRangePickerPanel } from "tdesign-vue-next";
import { ref, type SetupContext } from "vue";
import { orderBy as _orderBy, uniqBy as _uniqBy } from "lodash-es";
import type {
  TTableData,
  TTableRowsHandler,
  TTableColumns,
  TTableColumnsWithInfer,
  TTableColumnHandler,
  TFilterType,
} from "../types";
import { functionFromString } from "@/systems/function-systems";

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
      const filter = colKey2Info.get(key)!.filter!;
      const type = filter.type!;
      const predicate = filter.predicate
        ? functionFromString(filter.predicate)
        : undefined;

      const realType = type ?? ((filter as any)._type as TFilterType);

      return {
        key,
        value,
        type: realType,
        predicate,
      };
    });

    return rows.filter((row) => {
      return filterInfos.every((info) => {
        const filterType = info.type as TFilterType;
        const filterPredicate = info.predicate;

        if (filterType === "multiple") {
          const filterValues = info.value as string[];
          if (filterValues.length === 0) return true;
          return filterPredicate
            ? filterPredicate(filterValue, row)
            : filterValues.includes(row[info.key]);
        }

        if (filterType === "single") {
          const filterValue = info.value as any;
          if (!filterValue) return true;
          return filterPredicate
            ? filterPredicate(filterValue, row)
            : row[info.key] === filterValue;
        }

        if (filterType === "input") {
          const filterValue = info.value as string;
          if (!filterValue) return true;
          return filterPredicate
            ? filterPredicate(filterValue, row)
            : row[info.key].toString().includes(filterValue);
        }

        if (filterType === "date") {
          const filterValue = info.value as [Date, Date] | string;
          if (!filterValue || filterValue === "") return true;
          const [start, end] = filterValue;
          const date = new Date(row[info.key]);
          return filterPredicate
            ? filterPredicate(filterValue, row)
            : new Date(start) <= date && date <= new Date(end);
        }

        const _: never = filterType;

        throw new Error(`not support filter type ${filterType}`);
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
  const filterType = column.filter.type as TFilterType;

  if (filterType === "multiple") {
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

  if (filterType === "single") {
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

  if (filterType === "input") {
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

  if (filterType === "date") {
    const newFilter = {
      resetValue: "",
      showConfirmAndReset: true,
      props: {
        firstDayOfWeek: 7,
        ...column.filter?.props,
      },
      style: {
        fontSize: "14px",
      },
      classNames: "custom-class-name",
      attrs: {
        "data-type": "date-range-picker",
      },
      ...column.filter,
      component: DateRangePickerPanel,
      _type: "date",
    };

    delete newFilter.type;

    return {
      ...column,
      filter: newFilter,
    };
  }

  const _: never = filterType;
  throw new Error(`not support filter type ${filterType}`);
}
