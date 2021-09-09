def dictionary_insert_with_levels(
    *levels, _value: any, _current_dict_level: dict, _current_arg_id: int = 0
):
    level_size = len(levels)
    if level_size == 0:
        return

    if _current_arg_id == level_size - 1:
        _current_dict_level[levels[_current_arg_id]] = _value
        return

    level = levels[_current_arg_id]
    if _current_dict_level.get(level) is None:
        _current_dict_level.update({level: {}})

    dictionary_insert_with_levels(
        *levels,
        _value=_value,
        _current_arg_id=_current_arg_id + 1,
        _current_dict_level=_current_dict_level[level]
    )
