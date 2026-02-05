import arcade
import random

# --- COSTANTI ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
GRAVITY = 1.1
JUMP_FORCE = 18
PLAYER_ACCEL = 0.8
PLAYER_FRICTION = 0.9
PLAYER_START_Y = 100
FLOOR_HEIGHT = 85

# --- MENU PRINCIPALE ---
class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        # Definiamo le aree dei pulsanti per il clic del mouse
        self.button_width = 200
        self.button_height = 50
        self.center_x = SCREEN_WIDTH / 2
        
        # Altezze dei pulsanti
        self.play_y = SCREEN_HEIGHT / 2
        self.settings_y = SCREEN_HEIGHT / 2 - 70
        self.exit_y = SCREEN_HEIGHT / 2 - 140

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

    def on_draw(self):
        self.clear()
        # Titolo
        arcade.draw_text("MINER RUNNER 3.0", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 120,
                         arcade.color.GOLD, font_size=50, anchor_x="center", bold=True)
        
        # Pulsante GIOCA
        arcade.draw_rectangle_filled(self.center_x, self.play_y, self.button_width, self.button_height, arcade.color.AMBER)
        arcade.draw_text("GIOCA", self.center_x, self.play_y, arcade.color.BLACK, font_size=20, anchor_x="center", anchor_y="center")

        # Pulsante SETTINGS
        arcade.draw_rectangle_filled(self.center_x, self.settings_y, self.button_width, self.button_height, arcade.color.GRAY)
        arcade.draw_text("SETTINGS", self.center_x, self.settings_y, arcade.color.BLACK, font_size=20, anchor_x="center", anchor_y="center")

        # Pulsante ESCI
        arcade.draw_rectangle_filled(self.center_x, self.exit_y, self.button_width, self.button_height, arcade.color.BATTLESHIP_GREY)
        arcade.draw_text("ESCI (ESC)", self.center_x, self.exit_y, arcade.color.BLACK, font_size=20, anchor_x="center", anchor_y="center")

        # Istruzioni extra
        arcade.draw_text("Usa il MOUSE per cliccare o ESC per uscire", SCREEN_WIDTH / 2, 50,
                         arcade.color.LIGHT_GRAY, font_size=15, anchor_x="center")

    def on_mouse_press(self, x, y, button, modifiers):
        # Controllo clic su GIOCA
        if abs(x - self.center_x) < self.button_width / 2 and abs(y - self.play_y) < self.button_height / 2:
            self.start_game()
        
        # Controllo clic su ESCI
        if abs(x - self.center_x) < self.button_width / 2 and abs(y - self.exit_y) < self.button_height / 2:
            arcade.exit()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            self.start_game()
        elif key == arcade.key.ESCAPE:
            arcade.exit() # Esce dal programma se premi ESC nel menu

    def start_game(self):
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)

# --- VISTA DI GIOCO ---
class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.player_sprite = None
        self.enemy_list = arcade.SpriteList()
        self.score = 0
        self.game_speed = 8.0
        self.is_on_ground = True
        self.left_pressed = False
        self.right_pressed = False

    def setup(self):
        self.score = 0
        self.game_speed = 8.0
        self.enemy_list.clear()
        self.player_sprite = arcade.SpriteSolidColor(width=35, height=50, color=arcade.color.AMBER)
        self.player_sprite.center_x = 200
        self.player_sprite.center_y = PLAYER_START_Y

    def on_update(self, delta_time):
        self.score += delta_time * 10
        self.game_speed = 8.0 + (self.score / 500)

        if self.left_pressed: self.player_sprite.change_x -= PLAYER_ACCEL
        elif self.right_pressed: self.player_sprite.change_x += PLAYER_ACCEL
        
        self.player_sprite.change_x *= PLAYER_FRICTION
        self.player_sprite.center_x += self.player_sprite.change_x

        if self.player_sprite.left < 0: self.player_sprite.left = 0
        if self.player_sprite.right > SCREEN_WIDTH: self.player_sprite.right = SCREEN_WIDTH

        self.player_sprite.change_y -= GRAVITY
        self.player_sprite.center_y += self.player_sprite.change_y

        if self.player_sprite.center_y <= PLAYER_START_Y:
            self.player_sprite.center_y = PLAYER_START_Y
            self.player_sprite.change_y = 0
            self.is_on_ground = True

        if random.random() < 0.02:
            enemy = arcade.SpriteSolidColor(width=random.randint(50, 80), height=30, color=arcade.color.BATTLESHIP_GREY)
            enemy.center_x = SCREEN_WIDTH + 100
            enemy.center_y = FLOOR_HEIGHT + 15
            enemy.change_x = -self.game_speed
            self.enemy_list.append(enemy)

        for enemy in self.enemy_list:
            enemy.center_x += enemy.change_x
            if enemy.right < 0: enemy.remove_from_sprite_lists()

        if arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list):
            self.window.show_view(GameOverView(int(self.score)))

    def on_draw(self):
        self.clear()
        arcade.set_background_color(arcade.color.BLACK_OLIVE)
        arcade.draw_lrbt_rectangle_filled(0, SCREEN_WIDTH, 0, FLOOR_HEIGHT, arcade.color.BROWN)
        self.enemy_list.draw()
        arcade.draw_lrbt_rectangle_filled(self.player_sprite.left, self.player_sprite.right,
                                          self.player_sprite.bottom, self.player_sprite.top, arcade.color.AMBER)
        arcade.draw_text(f"SCORE: {int(self.score)} | ESC per MENU", 20, SCREEN_HEIGHT - 40, 
                         arcade.color.CYAN, font_size=24, bold=True)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(MenuView()) # Torna al menu se premi ESC durante il gioco
        
        if key in [arcade.key.W, arcade.key.SPACE, arcade.key.UP] and self.is_on_ground:
            self.player_sprite.change_y = JUMP_FORCE
            self.is_on_ground = False
        if key in [arcade.key.A, arcade.key.LEFT]: self.left_pressed = True
        if key in [arcade.key.D, arcade.key.RIGHT]: self.right_pressed = True

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.A, arcade.key.LEFT]: self.left_pressed = False
        if key in [arcade.key.D, arcade.key.RIGHT]: self.right_pressed = False

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
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Miner Runner 3.0")
    window.show_view(MenuView())
    arcade.run()

if __name__ == "__main__":
    main()