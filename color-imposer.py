"""
Name: Color Imposer
Written By: Nathaniel Holden
Date: 3/18/2020
Dependencies: Pillow

Inputs: a background color and
        a semi-transparent foreground color,
Outputs: an opaque (rgb) version of the imposed color.
"""

from PIL import ImageColor as ic;

class PixelColor(object):
    def __init__(self, inputString):
        super(PixelColor, self).__init__();
        self.color = ic.getrgb(inputString);
        self.r = self.color[0];
        self.g = self.color[1];
        self.b = self.color[2];
        self.a = self.color[3] if len(self.color) == 4 else 255;

    def getImposedColor(self, imposed):
        r = self.calculateTargetHue(self.r, imposed.r, imposed.a);
        g = self.calculateTargetHue(self.g, imposed.g, imposed.a);
        b = self.calculateTargetHue(self.b, imposed.b, imposed.a);
        return PixelColor('rgb({},{},{})'.format(r,g,b));

    def calculateTargetHue(self, bgHue, fgHue, a):
        alpha = float(a / 255);
        return int(((1 - alpha) * bgHue) + (alpha * fgHue));

    def toString(self):
        if len(self.color) == 4:
            return 'rgba{}'.format(self.color);
        else:
            return 'rgb{}'.format(self.color);


if __name__ == '__main__':
    backgroundInput = str(input('Please enter a background color:\n' +
                                ' * any standard color name, Ex: white\n' +
                                ' * a custom color, EX: #FFF or rgb(255,255,255)\n-> '));
    backgroundColor = PixelColor(backgroundInput);

    foregroundInput = str(input('Please enter a custom foreground color with an alpha value:\n' +
                                'Ex: #FFF7 or #FFFFFF7F or rgba(255,255,255,127)\n-> '));
    foregroundColor = PixelColor(foregroundInput);

    imposedColor = backgroundColor.getImposedColor(foregroundColor);

    print('background color: {}\n'.format(backgroundColor.toString()) +
          'foreground color: {}\n'.format(foregroundColor.toString()) +
          'imposed color:    {}'.format(imposedColor.toString()));
