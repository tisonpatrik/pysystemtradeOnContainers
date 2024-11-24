from typing import get_type_hints


def geT_all_annotations(cls) -> list[str]:
    annotations = {}
    for base_cls in cls.__mro__[::-1]:  # Traverse MRO in reverse
        if hasattr(base_cls, "__annotations__"):
            annotations.update(get_type_hints(base_cls))

    # Filter out attributes that are not user-defined fields
    excluded_keys = {
        "Config",
        "__extras__",
        "__schema__",
        "__config__",
        "__fields__",
        "__checks__",
        "__root_checks__",
        "__parsers__",
        "__root_parsers__",
    }
    return [key for key in annotations if key not in excluded_keys]
