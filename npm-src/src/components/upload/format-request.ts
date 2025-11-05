import { type UploadProps } from "tdesign-vue-next";

export function useFormatRequest(
  props: UploadProps
): UploadProps["formatRequest"] {
  return (data) => {
    if (data.length && data.length < 1) {
      return data;
    }

    const { multiple = false } = props;

    // Use file[i] or files field to let backend recognize as multiple files
    if (multiple) {
      if (data.length > 1) {
        const { file: _, ...newObj } = data;
        return newObj;
      }

      return { "file[0]": data.file };
    }

    // Use file field to let backend recognize as single file
    return data;
  };
}
