import arcade
import arcade.gui


# MISURE

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Il mio gioco"


# MENU PRINCIPALE

class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        play_button = arcade.gui.UIFlatButton(text="PLAY", width=200)
        quit_button = arcade.gui.UIFlatButton(text="ESCI", width=200)

        play_button.on_click = self.on_play
        quit_button.on_click = self.on_quit

        layout = arcade.gui.UIBoxLayout(spacing=20)
        layout.add(play_button)
        layout.add(quit_button)

        self.manager.add(arcade.gui.UIAnchorLayout(children=[layout]))

    def on_play(self, event):
        self.window.show_view(GameView())

    def on_quit(self, event):
        arcade.exit()

    def on_draw(self):
        self.clear()
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY) 
        self.manager.draw()

    def on_hide_view(self):
        self.manager.disable()


# GIOCO

class GameView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_draw(self):
        self.clear()
        arcade.draw_text("GIOCO", 
                        self.window.width // 2, 
                        self.window.height // 2,
                        arcade.color.WHITE, 48, anchor_x="center", anchor_y="center")
        arcade.draw_text("Premi ESC per pausa", 
                        self.window.width // 2, 30,
                        arcade.color.LIGHT_GRAY, 18, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(PauseView(self))
        
        
            



# MENU DI PAUSA

class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        resume_button = arcade.gui.UIFlatButton(text="RIPRENDI", width=200)
        menu_button   = arcade.gui.UIFlatButton(text="MENU PRINCIPALE", width=200)
        quit_button   = arcade.gui.UIFlatButton(text="ESCI", width=200)

        resume_button.on_click = self.on_resume
        menu_button.on_click   = self.on_menu
        quit_button.on_click   = self.on_quit

        layout = arcade.gui.UIBoxLayout(spacing=20)
        layout.add(resume_button)
        layout.add(menu_button)
        layout.add(quit_button)

        self.manager.add(
            arcade.gui.UIAnchorLayout(  
                children=[layout]
            )
        )

    def on_resume(self, event):
        self.window.show_view(self.game_view)

    def on_menu(self, event):
        self.window.show_view(MenuView())

    def on_quit(self, event):
        arcade.exit()

    def on_draw(self):
        self.clear()
        self.game_view.on_draw()
        arcade.draw_rect_filled(
            arcade.XYWH(self.window.width // 2, self.window.height // 2, self.window.width, self.window.height),
            (0, 0, 0, 150)
        )
        arcade.draw_text("PAUSA", 
                        self.window.width // 2, 
                        self.window.height // 2 + 150,
                        arcade.color.WHITE, 48, anchor_x="center", anchor_y="center")
        self.manager.draw()

    def on_hide_view(self):
        self.manager.disable()

def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, fullscreen=True)
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()

main()