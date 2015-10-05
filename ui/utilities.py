
def read_file(name):
    text_file = open(name, "r")
    return text_file.read()

def is_valid_configuration(matrix):
    counter = {'R': 0, 'G': 0, 'B': 0, 'Y': 0, '-': 0, '*': 0}

    if len(matrix) != 5:
        return False

    for row in matrix:
        if len(row) != 4:
            return False
        for cell in row:
            counter[cell] += 1

    if matrix[0].count('-') != 3:
        return False

    if counter['R'] != 4 or counter['G'] != 4 or counter['B'] != 4 or counter['Y'] != 4 or counter['-'] != 3 or counter['*'] != 1:
        return False

    return True

def get_image_name(operation):
    images = {
        'R': 'red_ball.png',
        'G': 'green_ball.png',
        'B': 'blue_ball.png',
        'Y': 'yellow_ball.png',
        '*': 'black_dice.png',
        '-': 'inner_background_gray.png'
    }
    return images.get(operation)

def get_matrix_image_name(color_id):
    images = {
        'R': 'img/red_ball_small.png',
        'G': 'img/green_ball_small.png',
        'B': 'img/blue_ball_small.png',
        'Y': 'img/yellow_ball_small.png',
        '*': None,
        '-': 'img/plastic_cover_small.png'
    }
    return images.get(color_id)

def get_operation_name(image):
    images = {
        'img/red_ball_small.png': 'R',
        'img/green_ball_small.png': 'G',
        'img/blue_ball_small.png': 'B',
        'img/yellow_ball_small.png': 'Y',
        'img/wildcard_small.png': '*',
        'img/plastic_cover_small.png': '-'
    }
    return images.get(image)

def has_upward_moves(matrix):
    count = 0
    for matrix_set in matrix:
        if(count < 4):
            if(matrix_set[0] == '*'):
                return True
        count += 1
    return False

def move_upward(matrix):
    count = 0
    for matrix_set in matrix:
        if(count < 4):
            if(matrix_set[0] == '*'):
                wildcard = matrix_set.pop(0)
                elem = matrix[count + 1].pop(0)
                matrix_set.insert(0, elem)
                matrix[count + 1].insert(0, wildcard)
                return matrix
        count += 1


def has_downward_moves(matrix):
    count = 0
    for matrix_set in matrix:
        if(count < 5):
            if(matrix_set[0] == '*' and count > 0):
                return True
        count += 1
    return False

def move_downward(matrix):
    count = 0
    for matrix_set in matrix:
        if(count < 5):
            if(matrix_set[0] == '*' and count > 0):
                wildcard = matrix_set.pop(0)
                elem = matrix[count - 1].pop(0)
                matrix_set.insert(0, elem)
                matrix[count - 1].insert(0, wildcard)
                return matrix
        count += 1


def get_movement_description(movement):
    orientation = movement[0]
    target_cell = movement[1]
    shifts = movement[2]
    description = "Desplace "

    if target_cell == '*':
        description += describe_gap_shifts(orientation, shifts)
        return description
    description = "Gire la "
    description += get_cell_type(target_cell)
    description += "hacia "
    description += get_orientation_description(orientation)
    description += get_shifts_description(shifts)

    return description


def describe_gap_shifts(orientation, shifts):
    description = str(shifts)
    description += " bolas " if shifts > 1 else " bola "
    description += "hacia "
    description += "arriba " if orientation == 'D' else "abajo "
    return description


def get_orientation_description(orientation):
    descriptions = {
        'R': "la derecha ",
        'L': "la izquierda ",
        'U': "arriba ",
        'D': "abajo "
    }
    return descriptions.get(orientation)


def get_cell_type(cell):
    types = {
        0: "primera fila ",
        1: "segunda fila ",
        2: "tercera fila ",
        3: "cuarta fila ",
        4: "quinta fila "
    }
    return types.get(cell)


def get_shifts_description(shifts):
    description = str(shifts)
    description += " espacio " if shifts == 1 else " espacios "
    return description
