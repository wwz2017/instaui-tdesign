export function functionFromString(code: string) {
  return new Function("return " + code)();
}
