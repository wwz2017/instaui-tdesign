import type { SetupContext } from "vue";
import type { AffixProps } from "tdesign-vue-next";

export function withDefaultContainer(
  attrs: SetupContext["attrs"]
): AffixProps["container"] {
  const { container = ".insta-main" } = attrs as AffixProps;

  return container;
}
