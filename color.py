import math


class color:

    hex_values = ["0", "1", "2", "3", "4", "5", "6",
                  "7", "8", "9", "A", "B", "C", "D", "E", "F"]

    def __init__(self, R, G, B, A=1):
        self.R = R
        self.G = G
        self.B = B
        self.A = A

    def return_color_between(self, color2, perc):
        r_change = color2.R - self.R
        g_change = color2.G - self.G
        b_change = color2.B - self.B
        a_change = color2.A - self.A

        r = self.R + (r_change * perc)
        g = self.G + (g_change * perc)
        b = self.B + (b_change * perc)
        a = self.A + (a_change * perc)

        return color(r, g, b, a)

    def __convert_tuple__(self, tuple):
        string = '('
        for i, item in enumerate(tuple):
            if i == len(tuple) - 1:
                string = string + str(item)
            else:
                string = string + str(item) + ","
        return string + ")"

    def return_string_in(self, code):
        if code == "RGB":
            return "rgba" + self.__convert_tuple__((self.R, self.G, self.B, self.A * 255))
        if code == "HSB":
            return "hsb" + self.__convert_tuple__((self.R, self.G, self.B, self.A))
        if code == "HEX":
            hex1 = self.__return_hex(self.R)
            hex2 = self.__return_hex(self.G)
            hex3 = self.__return_hex(self.B)
            hex4 = self.__return_hex(self.A)
            return "#{}{}{}{}{}{}".format(hex1[0], hex1[1], hex2[0], hex2[1], hex3[0], hex3[1], hex4[0], hex4[1])

    def return_color_in(self, code):
        if code == "RGB":
            return (self.R, self.G, self.B, self.A * 255)
        if code == "HSB":
            return (self.R, self.G, self.B, self.A)
        if code == "HEX":
            hex1 = self.__return_hex(self.R)
            hex2 = self.__return_hex(self.G)
            hex3 = self.__return_hex(self.B)
            hex4 = self.__return_hex(self.A)
            return "#{}{}{}{}{}{}".format(hex1[0], hex1[1], hex2[0], hex2[1], hex3[0], hex3[1], hex4[0], hex4[1])

    def __return_hex(self, component):
        rounded = math.floor(component / 16)
        remainder = (component / 16) - rounded

        hex1 = self.hex_values[rounded]
        hex2 = self.hex_values[math.floor(remainder * 16)]
        return (hex1, hex2)

    def __return_primes_for_RGB(self, hue, C, X):
        if 0 <= hue and hue < 60:
            return (C, X, 0)
        elif 60 <= hue and hue < 120:
            return (X, C, 0)
        elif 120 <= hue and hue < 180:
            return (0, C, X)
        elif 180 <= hue and hue < 240:
            return (0, X, C)
        elif 240 <= hue and hue < 300:
            return (X, 0, C)
        elif 300 <= hue and hue < 360:
            return (C, 0, X)

    def return_RGB(self):
        value = self.B / 100
        sat = self.G / 100

        C = sat * value
        X = C * (1 - abs(((self.R / 60) % 2) - 1))
        m = value - C

        primes = self.__return_primes_for_RGB(self.R, C, X)
        r = (primes[0] + m) * 255
        g = (primes[1] + m) * 255
        b = (primes[2] + m) * 255
        return (r, g, b)

    def return_HSB(self):
        r = self.R / 255
        g = self.G / 255
        b = self.B / 255

        cmax = max(r, g, b)
        cmin = min(r, g, b)
        delta = cmax - cmin

        h = 0
        s = 0
        v = 0

        # hue:
        if delta == 0:
            h = 0
        elif cmax == r:
            h = 60 * (((g - b) / delta) % 6)
        elif cmax == g:
            h = 60 * (((b - r) / delta) + 2)
        elif cmax == b:
            h = 60 * (((r - g) / delta) + 4)

        # saturation
        if cmax == 0:
            s = 0
        else:
            s = delta / cmax

        # value
        v = cmax

        return (h, s * 100, v * 100)

    def return_color_grad(self, second_color, steps):
        colors = []
        for step in range(0, steps):
            interval = step / (steps - 1)
            color = self.return_color_between(second_color, interval)
            colors.append(color.return_color_in("HEX"))
        return colors


class pallet:
    def __init__(self, grad, primary_color, secondary_color, background, secondary_background, text):
        self.grad = grad
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.background = background
        self.secondary_background = secondary_background
        self.text = text

        self.prim_RGB = primary_color.return_color_in("RGB")
        self.second_RGB = secondary_color.return_color_in("RGB")
        self.back_RGB = background.return_color_in("RGB")
        self.second_back_RGB = secondary_background.return_color_in("RGB")
        self.text_RGB = text.return_color_in("RGB")

        self.prim_HEX = primary_color.return_color_in("HEX")
        self.second_HEX = secondary_color.return_color_in("HEX")
        self.back_HEX = background.return_color_in("HEX")
        self.second_back_HEX = secondary_background.return_color_in("HEX")
        self.text_HEX = text.return_color_in("HEX")
