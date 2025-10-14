import type { SetupContext } from "vue";
import type { TableProps } from "tdesign-vue-next";
import { computed } from "vue";

const m_defaultTableAttrs = {
  hover: true,
  bordered: true,
  tableLayout: "auto",
  showSortColumnBgColor: true,
};

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
