import {
  defineComponent,
  h,
  onMounted,
  reactive,
  ref,
  useSlots,
  watch,
} from "vue";

export default defineComponent(render, {
  props: ["props"],
});

type TProps = {
  props: {
    value: any;
    onChange: (value: any) => void;
    fSlot: any;
  };
};

function render(inputProps: TProps) {
  // setup
  const props = inputProps.props;

  onMounted(() => {
    console.log("mounted");
  });

  const slotArgs = reactive({
    value: "",
  });

  watch(
    () => slotArgs.value,
    (value) => {
      props.onChange(value);
    }
  );

  // render
  return () => props.fSlot(slotArgs);
}
