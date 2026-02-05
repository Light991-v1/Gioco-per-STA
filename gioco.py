import arcade
import random

class mywindodw(arcade.Window):
    def __init__(self, larghezza, altezza, titolo):
        super().__init__(larghezza, altezza, titolo,resizable=True, fullscreen=True)

    def on_update(self, delta_time):
        pass    

    def on_draw(self):
        pass

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.set_fullscreen(False)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.BACKSLASH:
            self.set_fullscreen(True)

def main():
    gioco = mywindodw(1920, 1080, "Gioco py")
    arcade.run()

if __name__ == "__main__":
    main()