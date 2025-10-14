import type { ComputedRef, SetupContext } from "vue";
import { computed } from "vue";
import type { TRequiredTableColumns } from "../types";

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
