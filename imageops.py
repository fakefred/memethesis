from PIL import Image

WHITE = (255, 255, 255, 255)


def stack(images: list, mode='RGB', color=WHITE):
    w = max([im.size[0] for im in images])  # width of widest image
    h = sum([im.size[1] for im in images])  # sum of images' height

    stacked = Image.new(mode, (w, h), color=color)

    y = 0
    for im in images:
        stacked.paste(im, box=(0, y))  # no transparency
        y += im.size[1]

    return stacked
