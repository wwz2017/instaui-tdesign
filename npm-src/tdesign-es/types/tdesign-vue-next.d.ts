import "tdesign-vue-next";
import type { Ref } from "vue";

declare module "tdesign-vue-next" {
  export function useConfig(componentName: string): {
    t: (key: string, ...args: any[]) => string;
    globalConfig: Ref<TDesign.GlobalConfig>;
  };
}
