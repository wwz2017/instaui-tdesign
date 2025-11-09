import type { ComputedRef } from "vue";
import type {
  PrimaryTableCol,
  TableProps,
  TableRowData,
} from "tdesign-vue-next";

export type TRequiredTableColumns = NonNullable<TableProps["columns"]>;

export type TTableData = ComputedRef<any[]>;
export type TTableRowsHandler = (data: any[]) => any[];

export type TTableColumns = (PrimaryTableCol<TableRowData> & {
  label: string;
  name: string;
  filter: PrimaryTableCol<TableRowData>["filter"] & {
    predicate?: string;
  };
})[];

export type TFilterType = "single" | "multiple" | "input" | "date" | "custom";
export type TTableColumnsWithInfer = ComputedRef<TTableColumns>;
export type TTableColumnHandler = (columns: TTableColumns) => TTableColumns;
