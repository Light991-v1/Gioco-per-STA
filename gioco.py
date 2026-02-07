import arcade
import random
import arcade.gui

class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(1920, 1080, fullscreen=True, resizable=True, title="Rock Run")
        self.manager = arcade.gui.UIManager()
        arcade.set_background_color(arcade.color.BLACK)
        self.menu_background = arcade.load_texture("./assets/sfondo_menu.png")
        switch_menu_button = arcade.gui.UIFlatButton(text="Pause", width=250)
        @switch_menu_button.event("on_click")
        def on_click_switch_button(event):
            menu_view = MenuView(self)
            self.window.show_view(menu_view)
            self.anchor = self.manager.add(arcade.gui.UIAnchorLayout())

        self.anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=switch_menu_button,
        )
            
    
    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        self.manager.enable()
    
    def on_hide_view(self):
        self.manager.disable()

    def on_update(self, delta_time):
        return super().on_update(delta_time)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.menu_background,arcade.LBWH(0, 0, self.width, self.height))
        self.manager.draw()
    
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.set_fullscreen(False)
    
    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.F11:
            self.set_fullscreen(True)


























def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
    main_view = MainView()
    window.show_view(main_view)
    arcade.run()


if __name__ == "__main__":
    main()
