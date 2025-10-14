from typing import Literal, Optional


def remove_none_entries(data: dict) -> dict:
    return {k: v for k, v in data.items() if v is not None}


def define_col(
    col_key: str,
    *args,
    align: Optional[Literal["left", "center", "right"]] = None,
    sorter: Optional[bool] = None,
):
    result_dict = {
        "colKey": col_key,
        "align": align,
        "sorter": sorter,
    }
    filters: list[FilterInfo] = []

    for arg in args:
        if isinstance(arg, FilterInfo):
            filters.append(arg)

    if filters:
        assert len(filters) == 1, "Only one filter is allowed per column"
        result_dict["filter"] = filters[0].to_dict()

    return remove_none_entries(result_dict)


class FilterInfo:
    def __init__(
        self,
        filter_type: Literal["multiple", "single", "input", "date"],
        *,
        props: Optional[dict] = None,
        predicate_js: Optional[str] = None,
    ) -> None:
        self.filter_type = filter_type
        self.props = props
        self.predicate_js = predicate_js

    def to_dict(self) -> dict:
        return remove_none_entries(
            {
                "type": self.filter_type,
                "props": self.props,
                "predicate": self.predicate_js,
            }
        )


define_filter = FilterInfo


if __name__ == "__main__":
    columns = define_col("name", define_filter("date"))
