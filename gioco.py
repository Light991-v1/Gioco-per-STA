import arcade

class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(1920, 1080, fullscreen=True)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.set_fullscreen(False)

    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.F11:
            self.set_fullscreen(True)

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.text = "SEI NEL GIOCO!"

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

    def on_draw(self):
        self.clear()
        arcade.draw_text(self.text, 100, 100, arcade.color.WHITE, 40)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            menu = mymenu()
            self.window.show_view(menu)

class mymenu(arcade.View):
    def __init__(self):
        super().__init__()

        self.background_menu = arcade.load_texture("./Gioco-per-STA/assets/sfondo_menu.png")

        self.button1 = arcade.Sprite("./Gioco-per-STA/assets/play.png")
        self.button2 = arcade.Sprite("./Gioco-per-STA/assets/options.png")
        self.button3 = arcade.Sprite("./Gioco-per-STA/assets/exit.png")

        self.button1.center_x = 708 + 504 // 2
        self.button1.center_y = 610 + 120 // 2

        self.button2.center_x = 708 + 504 // 2
        self.button2.center_y = 480 + 120 // 2

        self.button3.center_x = 708 + 504 // 2
        self.button3.center_y = 350 + 120 // 2

        self.button1_box = arcade.LBWH(708, 610, 504, 120)
        self.button2_box = arcade.LBWH(708, 480, 504, 120)
        self.button3_box = arcade.LBWH(708, 350, 504, 120)

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(
            self.background_menu,
            arcade.LBWH(0, 0, self.window.width, self.window.height)
        )

        arcade.draw_sprite(self.button1) 
        arcade.draw_sprite(self.button2) 
        arcade.draw_sprite(self.button3)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.window.set_fullscreen(False)

    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.F11:
            self.window.set_fullscreen(True)

    def on_mouse_press(self, x, y, button, modifiers):

# --- VISTA GAME OVER ---
class GameOverView(arcade.View):
    def __init__(self, score):
        super().__init__()
        self.score = score

    def on_draw(self):
        self.clear()
        arcade.draw_text("GAME OVER", SCREEN_WIDTH/2, SCREEN_HEIGHT/2, arcade.color.RED, 50, anchor_x="center")
        arcade.draw_text(f"Punti: {self.score}", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 60, arcade.color.WHITE, 24, anchor_x="center")
        arcade.draw_text("Premi ESC per il menu", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 120, arcade.color.GRAY, 16, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE or key == arcade.key.ENTER:
            self.window.show_view(MenuView())

# --- MAIN ---
def main():
    window = GameWindow()
    menu = mymenu()
    window.show_view(menu)
    arcade.run()


if __name__ == "__main__":
    main()
