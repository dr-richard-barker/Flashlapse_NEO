try:
    import board
    import neopixel
except ImportError:
    # Use mock objects for simulation if the libraries are not installed
    class MockPixel:
        def __init__(self, pin, n, auto_write=False):
            self.n = n
            self._pixels = [(0, 0, 0)] * n

        def __setitem__(self, key, value):
            self._pixels[key] = value

        def __getitem__(self, key):
            return self._pixels[key]

        def fill(self, color):
            for i in range(self.n):
                self._pixels[i] = color

        def show(self):
            pass # In simulation, we don't need to do anything here

    class MockBoard:
        D18 = None

    board = MockBoard()
    neopixel = type("neopixel", (), {"NeoPixel": MockPixel})


try:
    from adafruit_led_animation.animation.solid import Solid
    from adafruit_led_animation.animation.blink import Blink
    from adafruit_led_animation.animation.colorcycle import ColorCycle
    from adafruit_led_animation.animation.chase import Chase
    from adafruit_led_animation.animation.comet import Comet
    from adafruit_led_animation.animation.pulse import Pulse
    from adafruit_led_animation.animation.rainbow import Rainbow
    from adafruit_led_animation.animation.sparkle import Sparkle
except ImportError:
    # Mock animation classes
    class MockAnimation:
        def __init__(self, pixels, *args, **kwargs):
            pass
        def animate(self):
            pass
    Solid = Blink = ColorCycle = Chase = Comet = Pulse = Rainbow = Sparkle = MockAnimation

class NeoPixelControl:
    def __init__(self, width=16, height=16, pin=board.D18, simulation=False):
        self.width = width
        self.height = height
        self.num_pixels = width * height
        self.simulation = simulation

        if not self.simulation:
            self.pixels = neopixel.NeoPixel(pin, self.num_pixels, auto_write=False)
        else:
            self.pixels = [(0, 0, 0)] * self.num_pixels

        self.animations = {
            "solid": Solid(self.pixels, color=(0, 0, 0)),
            "blink": Blink(self.pixels, speed=0.5, color=(255, 0, 0)),
            "colorcycle": ColorCycle(self.pixels, speed=0.5, colors=[(255, 0, 0), (0, 255, 0), (0, 0, 255)]),
            "chase": Chase(self.pixels, speed=0.1, color=(0, 0, 255), size=3, spacing=6),
            "comet": Comet(self.pixels, speed=0.1, color=(255, 0, 0), tail_length=10, bounce=True),
            "pulse": Pulse(self.pixels, speed=0.1, color=(0, 255, 0), period=3),
            "rainbow": Rainbow(self.pixels, speed=0.1, period=2),
            "sparkle": Sparkle(self.pixels, speed=0.1, color=(255, 255, 255), num_sparkles=10),
        }
        self.active_animation = None

    def _get_pixel_index(self, x, y):
        return (y * self.width) + x

    def set_pixel(self, x, y, color):
        if self.active_animation:
            self.active_animation = None

        index = self._get_pixel_index(x, y)
        if self.simulation:
            print(f"SIM: Setting pixel ({x}, {y}) to {color}")
            self.pixels[index] = color
        else:
            self.pixels[index] = color
            self.pixels.show()

    def fill(self, color):
        if self.active_animation:
            self.active_animation = None

        if self.simulation:
            print(f"SIM: Filling all pixels with {color}")
            for i in range(self.num_pixels):
                self.pixels[i] = color
        else:
            self.pixels.fill(color)
            self.pixels.show()

    def clear(self):
        self.fill((0, 0, 0))

    def run_animation(self, animation_name):
        if animation_name in self.animations:
            self.active_animation = self.animations[animation_name]
        else:
            print(f"Error: Animation '{animation_name}' not found.")

    def animate(self):
        if self.active_animation:
            if self.simulation:
                # In a real application, you might want to have a more sophisticated
                # simulation of the animation, but for now, we'll just print a message.
                print(f"SIM: Running animation '{self.active_animation.__class__.__name__}'")
            else:
                self.active_animation.animate()

    def load_pattern(self, pattern):
        """
        Loads a pattern from a 2D list of colors.
        """
        if self.active_animation:
            self.active_animation = None

        for y, row in enumerate(pattern):
            for x, color in enumerate(row):
                index = self._get_pixel_index(x, y)
                if self.simulation:
                    self.pixels[index] = tuple(color)
                else:
                    self.pixels[index] = tuple(color)

        if self.simulation:
            print("SIM: Loaded pattern")
            # print(self.pixels)
        else:
            self.pixels.show()

    def get_pattern(self):
        """
        Returns the current pattern as a 2D list of colors.
        """
        pattern = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                index = self._get_pixel_index(x, y)
                row.append(self.pixels[index])
            pattern.append(row)
        return pattern
