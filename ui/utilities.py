
def get_image_name(operation):
    images = {
        'R': 'red_ball.png',
        'G': 'green_ball.png',
        'B': 'blue_ball.png',
        'Y': 'yellow_ball.png',
        '*': 'black_dice.png'
    }
    return images.get(operation)

def get_operation_name(image):
    images = {
        'red_ball.png': 'R',
        'green_ball.png': 'G',
        'blue_ball.png': 'B',
        'yellow_ball.png': 'Y',
        'black_dice.png': '*'
    }

def get_movement_description(movement):
    orientation = movement[0]
    target_cell = movement[1]
    shifts = movement[2]

    description = "Mueva la "
    description += get_cell_type(target_cell)
    description += "hacia "
    description += get_orientation_description(orientation)
    description += get_shifts_description(shifts)
    return description


def get_orientation_description(orientation):
    descriptions = {
        'R': "la derecha ",
        'L': "la izquierda ",
        'U': "arriba ",
        'D': "abajo "
    }
    return descriptions.get(orientation);


def get_cell_type(cell):
    types = {
        '*': "muesca ",
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
