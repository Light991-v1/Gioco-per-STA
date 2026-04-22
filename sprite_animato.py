import arcade


class SpriteAnimato(arcade.Sprite):
    def __init__(self, scala: float = 1.0):
        super().__init__(scale=scala)
        # dizionario che contiene tutte le animazioni disponibili per questo sprite
        self.animazioni = {}
        self.animazione_corrente = None
        self.animazione_default = None
        # contatori per sapere a che punto siamo nell'animazione
        self.tempo_frame = 0.0
        self.indice_frame = 0

    def aggiungi_animazione(self, nome, percorso, frame_width, frame_height,
                             num_frame, colonne, durata, loop=True, default=False, riga=0):
        # carica il foglio di sprite dal file
        sheet = arcade.load_spritesheet(percorso)
        # se l'animazione è in una riga diversa dalla prima, salta i frame prima di essa
        offset = riga * colonne
        tutti = sheet.get_texture_grid(
            size=(frame_width, frame_height),
            columns=colonne,
            count=offset + num_frame,
        )
        # prendi solo i frame che ci interessano e fa l'animazione
        self._registra(nome, tutti[offset:], durata, loop, default)

    def _registra(self, nome, textures, durata, loop, default=False):
        # salva l'animazione con i suoi frame e quanto deve durare ogni immagine
        self.animazioni[nome] = {
            "textures": textures,
            "durata_frame": durata / len(textures),
            "loop": loop,
        }
        # se è quella di default, segnala come animazione di riposo
        if default or self.animazione_default is None:
            self.animazione_default = nome
        # se non c'è ancora nessuna animazione attiva, parti con questa
        if self.animazione_corrente is None:
            self._vai(nome)

    def imposta_animazione(self, nome: str):
        # cambia animazione solo se è diversa da quella che sta già girando
        if nome != self.animazione_corrente:
            self._vai(nome)

    def _vai(self, nome: str):
        # resetta tutto e parte dal primo frame della nuova animazione
        self.animazione_corrente = nome
        self.indice_frame = 0
        self.tempo_frame = 0.0
        self.texture = self.animazioni[nome]["textures"][0]

    def update_animation(self, delta_time: float = 1 / 60):
        anim = self.animazioni[self.animazione_corrente]
        # accumula il tempo passato dall'ultimo cambio di frame
        self.tempo_frame += delta_time
        # se non è ancora il momento di cambiare frame, non fare niente
        if self.tempo_frame < anim["durata_frame"]:
            return
        self.tempo_frame -= anim["durata_frame"]
        prossimo = self.indice_frame + 1
        if prossimo < len(anim["textures"]):
            # vai al frame successivo normalmente
            self.indice_frame = prossimo
        elif anim["loop"]:
            # siamo arrivati alla fine, ricomincia dall'inizio
            self.indice_frame = 0
        else:
            # animazione finita e non si ripete, torna a quella di riposo
            self._vai(self.animazione_default)
            return
        # aggiorna l'immagine mostrata sullo schermo
        self.texture = anim["textures"][self.indice_frame]