def _find(list, element, index):
    """Find an element in a list.
    The search is started at a specific index and then is expanded in both directions.

    parameters:
        [list] list -- The list.
        [object] element -- The element to search.
        [int] index -- The start index.
    """
    if (index < 0 or index >= len(list)):
        raise IndexError("list index out of range")

    max_delta = max(index + 1, len(list) - index)
    delta = 0

    while delta < max_delta:
        lower_index = index - delta
        if lower_index >= 0 and list[lower_index] == element:
            return lower_index

        upper_index = index + delta
        if upper_index <= len(list) - 1 and list[upper_index] == element:
            return upper_index

        delta += 1

    raise ValueError(element + " is not in list")
