"""
Name: Color Imposer
Written By: Nathaniel Holden
Date: 3/18/2020
Dependencies: Pillow

Inputs: a background color and
        a semi-transparent foreground color,
Outputs: an opaque (rgb) version of the imposed color.
"""

from PIL import ImageColor


class PixelColor(object):
    def __init__(self, input_string):
        super(PixelColor, self).__init__()
        self.color = ImageColor.getrgb(input_string)
        self.r = self.color[0]
        self.g = self.color[1]
        self.b = self.color[2]
        self.a = self.color[3] if len(self.color) == 4 else 255

    def get_imposed_color(self, imposed):
        r = self.calculate_target_hue(self.r, imposed.r, imposed.a)
        g = self.calculate_target_hue(self.g, imposed.g, imposed.a)
        b = self.calculate_target_hue(self.b, imposed.b, imposed.a)
        return PixelColor('rgb({},{},{})'.format(r, g, b))

    @staticmethod
    def calculate_target_hue(bg_hue, fg_hue, a):
        alpha = float(a / 255)
        return int(((1 - alpha) * bg_hue) + (alpha * fg_hue))

    def to_string(self):
        if len(self.color) == 4:
            return 'rgba{}'.format(self.color)
        else:
            return 'rgb{}'.format(self.color)


def impose_color():
    background_input = str(input('Please enter a background color:\n' +
                                 ' * any standard color name, Ex: white\n' +
                                 ' * a custom color, EX: #FFF or rgb(255,255,255)\n-> '))
    background_color = PixelColor(background_input)

    foreground_input = str(input('Please enter a custom foreground color with an alpha value:\n' +
                                 'Ex: #FFF7 or #FFFFFF7F or rgba(255,255,255,127)\n-> '))
    foreground_color = PixelColor(foreground_input)

    imposed_color = background_color.get_imposed_color(foreground_color)

    print('background color: {}\n'.format(background_color.to_string()) +
          'foreground color: {}\n'.format(foreground_color.to_string()) +
          'imposed color:    {}\n'.format(imposed_color.to_string()))


if __name__ == '__main__':
    while True:
        impose_color()
