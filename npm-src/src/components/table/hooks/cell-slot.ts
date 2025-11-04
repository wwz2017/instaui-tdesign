import type { TTableColumnsWithInfer } from "../types";

export function withCellSlotPropConverter(columns: TTableColumnsWithInfer) {
  const cellSlotNames = new Set(columns.value.map((col) => col.cell as string));

  return (slotName: string | number, orgProps: any) => {
    return cellSlotNames.has(slotName as string)
      ? { ...orgProps, currentValue: orgProps.row[orgProps.col.colKey] }
      : orgProps;
  };
}
