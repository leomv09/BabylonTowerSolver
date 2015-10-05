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

        errors = validate_matrix(start, "start") + validate_matrix(end, "end")
        return start, end, errors


def _parse_matrix(matrix):
    return [_parse_row(row) for row in matrix]


def _parse_row(row):
    return [str(x) for x in row]


def validate_matrix(matrix, name):
    """Validate  matrix

    parameters:
        Matrix matrix -- the matriz to validate


    return:
        [String] return matrix  errors
    """
    errors = "######  Matrix   " + name + ' errors    ######\n '
    errors += validate_values(matrix)
    errors += validate_structure(matrix)
    errors += validate_amount_balls(matrix)
    return errors


def validate_values(matrix):
    """Validate values of a matrix

    parameters:
        Matrix matrix -- the matriz to validate
        String name -- ID name for the matrix

    return:
        [String] matrix values errors
    """
    errors = ""
    row_in = 1
    values = ['*', '-', 'R', 'G', 'B', 'Y']
    for row in matrix:
            for value in row:
                if (value in values)==False:
                    error = "Caracter invalido  "+"'" + str(value) + "'" + "    Fila # " + str(row_in) + "\n"
                    errors += error
                row_in += 1
    return errors


def validate_structure(matrix):
    """Validate  matrix structure

    parameters:
        Matrix matrix -- the matriz to validate


    return:
        [String] matrix structure errors
    """
    errors = ""
    if len(matrix)!=5:
        errors += "Error en la cantidad de filas"
    row_in = 1
    for row in matrix:
        if len(row)!=4:
            errors += "Error en la cantidad de columnas" + " Fila  #" + str(row_in)+ "\n"
        row_in += 1
    return errors


def validate_amount_balls(matrix):
    """Validate  amount of balls

    parameters:
        Matrix matrix


    return:
        [String] amount balls errors
    """
    balls = [0, 0, 0, 0, 0, 0] #[red balls, Green balls , Blue balls,Yellow balls,-,*]
    errors = ""
    for row in matrix:
            balls[0] += row.count("R")
            balls[1] += row.count("G")
            balls[2] += row.count("B")
            balls[3] += row.count("Y")
            balls[4] += row.count("-")
            balls[5] += row.count("*")

    if balls[0] != 4:
        errors += "error en la cantidad de bolas rojas: aparecen " + str(balls[0]) + "\n"
    if balls[1] != 4:
        errors += "error en la cantidad de bolas verdes: aparecen " + str(balls[1]) + "\n"
    if balls[2] != 4:
        errors += "error en la cantidad de bolas azules: aparecen " + str(balls[2]) + "\n"
    if balls[3] != 4:
        errors += "error en la cantidad de bolas amarillas: aparecen " + str(balls[3]) + "\n"
    if balls[4] != 3:
        errors += "error en la cantidad de espacio bloqueado: aparecen: " + str(balls[4]) + "\n"
    if balls[5] != 1:
        errors += "error en la cantidad de muesca aparecen: " + str(balls[5]) + "\n"
    return errors


