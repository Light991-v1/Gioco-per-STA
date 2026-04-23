import os
import arcade
from sprite_animato import SpriteAnimato

FRAME_SIZE   = 96
VELOCITA     = 300
RANGE_ATTACK = 60
PAVIMENTO    = 184   # uguale a player_sprite.center_y a terra in play.py
_HERE        = os.path.dirname(os.path.abspath(__file__))


class Nemico(SpriteAnimato):

    # stesse animazioni del player, il nemico usa gli stessi file
    ANIMAZIONI = [
        ("idle",   "assets/IDLEn.png",      10,  0.8, True,  True),
        ("run",    "assets/RUNn.png",        16,  0.5, True,  False),
        ("attack", "assets/ATTACK-n.png",    7,  0.3, False, False),
        ("hurt",   "assets/HURTn.png",        4,  0.3, False, False),
    ]

    def __init__(self, x: float, y: float):
        super().__init__()
        # posiziona il nemico dove viene spawanto
        self.center_x     = x
        self.center_y     = y
        self.facing_right = True
        # locked = True significa che sta facendo un'animazione che non si interrompe
        self.locked       = False
        self.vivo         = True
        # timer per decidere ogni quanto il nemico può attaccare di nuovo
        self.attack_timer = 0.0
        self.change_y     = 0.0

        # carica tutte le animazioni in versione destra e sinistra
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
        # la scala non viene messa qui, la decide play.py quando spawna il nemico

    def _anim(self, nome: str) -> str:
        # restituisce il nome dell'animazione con il lato giusto attaccato in fondo
        return nome + ("_dx" if self.facing_right else "_sx")

    def trigger_hurt(self):
        # blocca il nemico e fallo fare l'animazione del colpo ricevuto
        self.locked = True
        self.imposta_animazione(self._anim("hurt"))

    def update(self, player, delta_time: float = 1 / 60):
        # se il nemico è morto non fare niente
        if not self.vivo:
            return

        # calcola quanto è lontano il player e da che parte sta
        dx = player.center_x - self.center_x
        distanza = abs(dx)

        # il nemico guarda sempre verso il player
        self.facing_right = dx > 0

        if not self.locked:
            if distanza <= RANGE_ATTACK:
                # il player è abbastanza vicino, fermati e preparati ad attaccare
                self.change_x = 0
                self.imposta_animazione(self._anim("idle"))
                self.attack_timer += delta_time
                if self.attack_timer >= 0.5:
                    # è passato abbastanza tempo, attacca!
                    self.attack_timer = 0.0
                    self.locked = True
                    self.imposta_animazione(self._anim("attack"))
            else:
                # il player è lontano, corri verso di lui
                self.attack_timer = 0.0
                self.change_x = VELOCITA if dx > 0 else -VELOCITA
                self.imposta_animazione(self._anim("run"))

        # sposta fisicamente il nemico in base alla velocità
        self.center_x += self.change_x * delta_time

        # gravità fatta a mano: tira il nemico verso il basso ogni frame
        self.change_y -= 0.5
        self.center_y += self.change_y
        if self.center_y <= PAVIMENTO:
            # è arrivato a terra, bloccalo al pavimento e ferma la caduta
            self.center_y = PAVIMENTO
            self.change_y = 0.0

    def update_animation(self, delta_time: float = 1 / 60):
        # fai avanzare l'animazione di un frame
        super().update_animation(delta_time)
        # se l'animazione di attacco o dolore è finita, sblocca il nemico
        if self.locked and self.animazione_corrente in ("idle_dx", "idle_sx"):
            self.locked = False