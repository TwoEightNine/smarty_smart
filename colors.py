import colorsys


def to_rgb(t):
    return hex(int(t[0] * 255))[2:].zfill(2) \
           + hex(int(t[1] * 255))[2:].zfill(2) \
           + hex(int(t[2] * 255))[2:].zfill(2)


def create_colors():
    result = [hex(i * 15 // 6)[2:] * 6 for i in range(7)]
    for hue in range(30):
        h = hue / 30.0
        result.append(to_rgb(colorsys.hsv_to_rgb(h, 1, 0.25)))
        result.append(to_rgb(colorsys.hsv_to_rgb(h, 1, 0.5)))
        result.append(to_rgb(colorsys.hsv_to_rgb(h, 1, 0.75)))
        result.append(to_rgb(colorsys.hsv_to_rgb(h, 1, 1)))
        result.append(to_rgb(colorsys.hsv_to_rgb(h, 0.75, 1)))
        result.append(to_rgb(colorsys.hsv_to_rgb(h, 0.5, 1)))
        result.append(to_rgb(colorsys.hsv_to_rgb(h, 0.25, 1)))

    return result


if __name__ == "__main__":
    print(create_colors())
