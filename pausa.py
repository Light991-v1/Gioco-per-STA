import arcade
import arcade.gui

class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

        self.game_view.camera.position = (self.window.width // 2, self.window.height // 2)

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

        self.manager.add(arcade.gui.UIAnchorLayout(children=[layout]))

    def on_resume(self, event):
        self.window.show_view(self.game_view)

    def on_menu(self, event):
        from menu import MenuView   # ← IMPORT QUI
        self.window.show_view(MenuView())

    def on_quit(self, event):
        arcade.exit()

    def on_draw(self):
        self.clear()
        self.game_view.camera.use()
        bg = self.game_view.backgrounds
        bg.offset = self.game_view.camera.bottom_left
        bg.pos = self.game_view.camera.bottom_left
        bg.draw()
        self.game_view.scene.draw()

        w = self.window.width
        h = self.window.height

        arcade.draw_rect_filled(
            arcade.XYWH(w // 2, h // 2, w, h),
            (0, 0, 0, 150)
        )
        arcade.draw_text(
            "PAUSA",
            w // 2,
            h // 2 + 150,
            arcade.color.WHITE,
            48,
            anchor_x="center",
            anchor_y="center"
        )
        self.manager.draw()

    def on_hide_view(self):
        self.manager.disable()
