from collections import Counter
from io import BytesIO
from base64 import b64decode
from PIL import Image, ImageOps

operators_dataset = {
    '+': [
        ((2, 10), 1),
        ((9, 2), 1),
        ((18, 11), 1),
        ((10, 11), 1),
        ((10, 10), 0),
        ((9, 11), 0),
        ((5, 6), 0),
        ((15, 17), 0),
    ],
    '-': [
        ((4, 13), 1),
        ((4, 17), 1),
        ((15, 18), 1),
        ((17, 12), 1),
        ((18, 11), 0),
        ((3, 11), 0),
        ((3, 19), 0),
        ((19, 19), 0),
    ],
    '*': [
        ((6, 6), 1),
        ((21, 25), 1),
        ((4, 23), 1),
        ((22, 5), 1),
        ((6, 18), 0),
        ((13, 14), 0),
        ((8, 8), 0),
        ((20, 8), 0),
    ]
}
numbers_dataset = {
    0: [
        ((1, 14), 1),
        ((9, 2), 1),
        ((19, 15), 1),
        ((11, 27), 1),
        ((10, 15), 0),
        ((3, 3), 0),
        ((18, 25), 0),
        ((10, 23), 0),
        ((10, 4), 0)
    ],
    1: [
        ((4, 8), 1),
        ((9, 2), 1),
        ((15, 25), 1),
        ((5, 25), 1),
        ((7, 7), 0),
        ((6, 23), 0),
        ((14, 22), 0),
        ((11, 23), 0),
        ((11, 14), 0)
    ],
    2: [
        ((18, 25), 1),
        ((6, 26), 1),
        ((3, 6), 1),
        ((13, 3), 1),
        ((17, 21), 0),
        ((7, 21), 0),
        ((16, 16), 0),
        ((6, 7), 0),
        ((13, 6), 0)
    ],
    3: [
        ((3, 3), 1),
        ((4, 24), 1),
        ((7, 15), 1),
        ((16, 16), 1),
        ((7, 22), 0),
        ((13, 17), 0),
        ((9, 13), 0),
        ((13, 7), 0),
        ((10, 5), 0)
    ],
    4: [
        ((2, 15), 1),
        ((7, 2), 1),
        ((18, 6), 1),
        ((12, 27), 1),
        ((12, 22), 0),
        ((13, 12), 0),
        ((15, 8), 0),
        ((11, 5), 0),
        ((5, 17), 0)
    ],
    5: [
        ((7, 3), 1),
        ((2, 22), 1),
        ((18, 22), 1),
        ((19, 4), 1),
        ((13, 20), 0),
        ((13, 15), 0),
        ((13, 5), 0),
        ((7, 13), 0),
        ((9, 5), 0)
    ],
    6: [
        ((14, 3), 1),
        ((11, 27), 1),
        ((16, 18), 1),
        ((9, 18), 1),
        ((10, 19), 0),
        ((5, 17), 0),
        ((14, 15), 0),
        ((11, 10), 0),
        ((17, 12), 0)
    ],
    7: [
        ((4, 24), 1),
        ((18, 4), 1),
        ((2, 4), 1),
        ((9, 26), 1),
        ((11, 26), 0),
        ((7, 21), 0),
        ((12, 13), 0),
        ((4, 7), 0),
        ((15, 7), 0)
    ],
    8: [
        ((3, 23), 1),
        ((16, 5), 1),
        ((4, 3), 1),
        ((9, 15), 1),
        ((10, 20), 0),
        ((9, 10), 0),
        ((14, 9), 0),
        ((17, 26), 0),
        ((3, 2), 0)
    ],
    9: [
        ((17, 27), 1),
        ((2, 8), 1),
        ((10, 2), 1),
        ((10, 7), 1),
        ((13, 9), 0),
        ((14, 5), 0),
        ((13, 22), 0),
        ((5, 15), 0),
        ((17, 2), 0)
    ]
}


def get_operator(i) -> tuple[int, float]:
    result = {
        operator: (
                          Counter([(1 if i.getpixel(coords) else 0) == color for coords, color in data]).get(
                              True) or 0) / len(data)
        for operator, data in operators_dataset.items()
    }

    most_probably_operator = max(result, key=result.get)
    probably = result[most_probably_operator]

    return most_probably_operator, probably


def get_number(i) -> tuple[int, float]:
    result = {
        number: (
                        Counter([(1 if i.getpixel(coords) else 0) == color for coords, color in data]).get(
                            True) or 0) / len(data)
        for number, data in numbers_dataset.items()
    }

    most_probably_number = max(result, key=result.get)
    probably = result[most_probably_number]

    return most_probably_number, probably


def solve_from_base64(base64: str):
    im = Image.open(BytesIO(b64decode(base64.replace('data:image/png;base64,', ''))))
    w, h = im.size
    im = im.crop((4, 6, w - 41, h - 5))
    im = ImageOps.invert(im.convert('L'))

    w, h = im.size
    x = im.crop((0, 0, 20, h))  # first number
    y = im.crop((24, 0, 49, h))  # operator
    z = im.crop((48, 0, 48 + 20, h))  # second number they are 48 pixels from first number

    x, px = get_number(x)
    y, py = get_operator(y)
    z, pz = get_number(z)

    return eval(f'{x}{y}{z}')
