import json


def save(path, start_matrix, end_matrix):
    """Save a configuration to a file.

    parameters:
        [string] path -- The file location.
        [list] start_matrix -- The start matrix.
        [list] end_matrix -- The end matrix.
    """
    obj = {
        "start": start_matrix,
        "end": end_matrix
    }

    with open(path, "w") as f:
        text = json.dumps(obj)
        f.write(text)


def load(path):
    """Load a configuration from a file.

    parameters:
        [string] path -- The file location.

    return:
        [tuple] A (M1, M2) tuple containing the start and end matrix.
    """
    with open(path, "r") as f:
        text = f.read()
        obj = json.loads(text)

        start = _parse_matrix(obj["start"])
        end = _parse_matrix(obj["end"])

        return start, end


def _parse_matrix(matrix):
    return [_parse_row(row) for row in matrix]


def _parse_row(row):
    return [str(x) for x in row]
