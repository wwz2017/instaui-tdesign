import { type App } from "vue";
import * as TDesign from "tdesign-vue-next";
import Affix from "@/components/Affix.vue";
import Table from "@/components/table/Table.vue";
import Anchor from "@/components/Anchor.vue";
import Icon from "@/components/Icon.vue";
import Select from "@/components/Select.vue";
import RadioGroup from "@/components/RadioGroup.vue";
import { NotifyPlugin, MessagePlugin } from "tdesign-vue-next";
import "tdesign-vue-next/es/style/index.css";
import "./style/index.css";

function install(app: App) {
  app.use(TDesign);
  app.component("t-table", Table);
  app.component("t-affix", Affix);
  app.component("t-anchor", Anchor);
  app.component("t-icon", Icon);
  app.component("t-select", Select);
  app.component("t-radio-group", RadioGroup);
  (window as any).$tdesign = {
    NotifyPlugin,
    MessagePlugin,
  };
}

export { install };
