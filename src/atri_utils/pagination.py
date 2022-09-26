from typing import Any, List, Tuple


def page_start_end(old_start: int, page_size: int, total: int):
    """
    Parameters
    ----------
    old_start: The old starting index of pagination
    page_size: The number of entries visible per page of pagination
    total: The total number of entries

    Returns
    -------
    (new_start, new_end): The new start and end value
    """
    if old_start == 0:
        return (min(1, total), min(page_size, total))

    new_start = min(old_start + page_size, total)
    new_end = min(new_start + page_size, total)

    return (new_start, new_end)

def page_show_hide(
    at: Any,
    alias_prefix: str,
    alias_range: Tuple[int, int],
    values: List[Any],
    accessor: List[str] = ["styles", "display"],
    show_value: Any = "flex",
    hide_value: Any = "none"):

    for i in range(alias_range[0], alias_range[1] + 1):
        value_index = i - alias_range[0]
        value = show_value if value_index < len(values) else hide_value
        
        attr = alias_prefix + str(i)
        if at.hasattr(attr):
            obj = at.getattr(attr)
            # iterate over accessor
            for acc_index, acc in enumerate(accessor):
                if acc_index == len(accessor) - 1:
                    obj.setattr(acc, value)
                else:
                    obj = obj.getattr(acc)

def page_assign_values(
    at: Any,
    alias_prefix: str,
    alias_range: Tuple[int, int],
    values: List[Any],
    accessor: List[str]):
    
    for i in range(alias_range[0], alias_range[1] + 1):
        value_index = i - alias_range[0]

        if value_index < len(values):  
            value = values[value_index]      
            attr = alias_prefix + str(i)
            if at.hasattr(attr):
                obj = at.getattr(attr)
                # iterate over accessor
                for acc_index, acc in enumerate(accessor):
                    if acc_index == len(accessor) - 1:
                        obj.setattr(acc, value)
                    else:
                        obj = obj.getattr(acc)
