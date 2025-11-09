from typing import Any, Literal, Optional
from instaui import custom
import copy


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
        bind_value: Optional[Any] = None,
        confirm_events: Optional[list[str]] = None,
    ) -> None:
        self.filter_type = filter_type
        self.props = props
        self.predicate_js = predicate_js
        self._state_props: set[str] = set()
        self.bind_value = (
            custom.convert_reference(bind_value) if bind_value is not None else None
        )
        self.confirm_events = confirm_events

        if self.props:
            self.props = copy.deepcopy(self.props)
            self.props["value"] = custom.convert_reference(self.props["value"])
            self._state_props.add("value")

    def to_dict(self) -> dict:
        result = remove_none_entries(
            {
                "type": self.filter_type,
                "props": self.props,
                "predicate": self.predicate_js,
                "bindValue": self.bind_value,
                "confirmEvents": self.confirm_events,
            }
        )

        if self._state_props:
            result["stateProps"] = list(self._state_props)

        return result


define_filter = FilterInfo


if __name__ == "__main__":
    columns = define_col("name", define_filter("date"))
