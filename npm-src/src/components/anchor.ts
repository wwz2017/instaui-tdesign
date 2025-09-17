import type { SetupContext } from "vue";
import type { AnchorProps } from "tdesign-vue-next";

export function withDefaultAffixProps(
  attrs: SetupContext["attrs"]
): AnchorProps["affixProps"] {
  const { affixProps = {} } = attrs as AnchorProps;

  return {
    container: ".insta-main",
    ...affixProps,
  };
}

export function withDefaultContainer(
  attrs: SetupContext["attrs"]
): AnchorProps["container"] {
  const { container = ".insta-main" } = attrs as AnchorProps;

  return container;
}
