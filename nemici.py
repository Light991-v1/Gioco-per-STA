import os
import arcade
from sprite_animato import SpriteAnimato

FRAME_SIZE   = 96
VELOCITA     = 300
RANGE_ATTACK = 60
PAVIMENTO    = 184   # uguale a player_sprite.center_y a terra in play.py
_HERE        = os.path.dirname(os.path.abspath(__file__))


class Nemico(SpriteAnimato):

    ANIMAZIONI = [
        ("idle",   "assets/IDLE.png",      10,  0.8, True,  True),
        ("run",    "assets/RUN.png",        16,  0.5, True,  False),
        ("attack", "assets/ATTACK 1.png",    7,  0.3, False, False),
        ("hurt",   "assets/HURT.png",        4,  0.3, False, False),
    ]

    def __init__(self, x: float, y: float):
        super().__init__()
        self.center_x     = x
        self.center_y     = y
        self.facing_right = True
        self.locked       = False
        self.vivo         = True
        self.attack_timer = 0.0
        self.change_y     = 0.0

        for nome, file, n_frame, durata, loop, default in self.ANIMAZIONI:
            percorso = os.path.join(_HERE, file)

            self.aggiungi_animazione(
                nome=nome + "_dx",
                percorso=percorso,
                frame_width=FRAME_SIZE, frame_height=FRAME_SIZE,
                num_frame=n_frame, colonne=n_frame,
                durata=durata,
                loop=loop,
                default=default,
            )
            self.aggiungi_animazione(
                nome=nome + "_sx",
                percorso=percorso,
                frame_width=FRAME_SIZE, frame_height=FRAME_SIZE,
                num_frame=n_frame, colonne=n_frame,
                durata=durata,
                loop=loop,
                default=default,
            )

        self.animazione_default = "idle_dx"
        # scala NON impostata qui — la imposta play.py con PLAYER_SCALE

    def _anim(self, nome: str) -> str:
        return nome + ("_dx" if self.facing_right else "_sx")

    def trigger_hurt(self):
        self.locked = True
        self.imposta_animazione(self._anim("hurt"))

    def update(self, player, delta_time: float = 1 / 60):
        if not self.vivo:
            return

        dx = player.center_x - self.center_x
        distanza = abs(dx)

        self.facing_right = dx > 0

        if not self.locked:
            if distanza <= RANGE_ATTACK:
                self.change_x = 0
                self.imposta_animazione(self._anim("idle"))
                self.attack_timer += delta_time
                if self.attack_timer >= 0.5:
                    self.attack_timer = 0.0
                    self.locked = True
                    self.imposta_animazione(self._anim("attack"))
            else:
                self.attack_timer = 0.0
                self.change_x = VELOCITA if dx > 0 else -VELOCITA
                self.imposta_animazione(self._anim("run"))

        self.center_x += self.change_x * delta_time

        # gravità
        self.change_y -= 0.5
        self.center_y += self.change_y
        if self.center_y <= PAVIMENTO:
            self.center_y = PAVIMENTO
            self.change_y = 0.0

    def update_animation(self, delta_time: float = 1 / 60):
        super().update_animation(delta_time)
        if self.locked and self.animazione_corrente in ("idle_dx", "idle_sx"):
            self.locked = False