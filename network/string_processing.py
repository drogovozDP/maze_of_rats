def rats_to_str(rats):
    rats_str = ''
    for rat in rats:
        rats_str += f"{rat[0]},{rat[1]}:"
    return rats_str[0:-1]


def rats_from_str(rats_str):
    return [[int(coord) for coord in rat.split(',')] for rat in rats_str.split(':')]

