import arcade
import random
import time
import os


# Dimensiones pantalla
SCREE_WIDHT = 1300
SCREE_HEIGHT = 700
SCREE_TITLE = "COVID ESCAPE"

# constantes para escalar sprites
escala_personaje = 0.7
escala_virus = 0.12
escala_virus2 = 0.2
escala_piso = 0.5
escala_pisovolador = 0.43
escala_guantes = 0.05
escala_mask = 0.10
escala_gel = 0.07
escala_sol = 0.5

# características de la fisica del juego
JUMP_SPEED = 15
GRAVITY = 3
MOVEMENT_SPEED = 5
VIRUS_SPEED = 2
VIRUS2_SPEED = 2.5

# Cuántos píxeles para mantener como margen mínimo entre el personaje
# y el borde de la pantalla.
LEFT_VIEWPORT_MARGIN = 200
RIGHT_VIEWPORT_MARGIN = 250
BOTTOM_VIEWPORT_MARGIN = 0
TOP_VIEWPORT_MARGIN = 0

MUSIC_VOLUME = 0.03
MUSIC_VOLUME_HIGH = 0.25


class InstructionView(arcade.View):

    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("Instrucciones.jpg")
        # Restablecer la ventana gráfica, necesaria si tenemos un juego de desplazamiento y necesitamos
        # para restablecer la ventana gráfica al inicio para que podamos ver lo que dibujamos.
        arcade.set_viewport(0, SCREE_WIDHT - 1, 0, SCREE_HEIGHT - 1)

    def on_draw(self):
        """ Dibuja esta vista """
        arcade.start_render()
        self.texture.draw_sized(SCREE_WIDHT / 2, SCREE_HEIGHT / 2,
                                SCREE_WIDHT, SCREE_HEIGHT)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ Si el usuario presiona el botón del mouse, inicia el juego. """
        game_view = MyGame()
        game_view.setup()
        self.window.show_view(game_view)


class Virus(arcade.Sprite):

    def follow_sprite(self, player_sprite):
        # Esta función es para que el virus (self) se mueva hacia el personaje (player.sprite).

        if self.center_y < player_sprite.center_y:
            self.center_y += min(VIRUS_SPEED, player_sprite.center_y - self.center_y)
        elif self.center_y > player_sprite.center_y:
            self.center_y -= min(VIRUS_SPEED, self.center_y - player_sprite.center_y)

        if self.center_x < player_sprite.center_x:
            self.center_x += min(VIRUS_SPEED, player_sprite.center_x - self.center_x)
        elif self.center_x > player_sprite.center_x:
            self.center_x -= min(VIRUS_SPEED, self.center_x - player_sprite.center_x)


class Virus2(arcade.Sprite):

    def follow_sprite(self, player_sprite):
        # Esta función es para que el virus (self) se mueva hacia el personaje (player.sprite).

        if self.center_y < player_sprite.center_y:
            self.center_y += min(VIRUS2_SPEED, player_sprite.center_y - self.center_y)
        elif self.center_y > player_sprite.center_y:
            self.center_y -= min(VIRUS2_SPEED, self.center_y - player_sprite.center_y)

        if self.center_x < player_sprite.center_x:
            self.center_x += min(VIRUS2_SPEED, player_sprite.center_x - self.center_x)
        elif self.center_x > player_sprite.center_x:
            self.center_x -= min(VIRUS2_SPEED, self.center_x - player_sprite.center_x)


class MyGame(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.ALICE_BLUE)

        self.player_list = None  # LISTA QUE CONTIENE PERSONAJE
        self.virus_list = None  # ...
        self.virus2_list = None  # ...
        self.pisos_list = None
        self.agua_list = None
        self.lava_list = None
        self.objetos_list = None
        self.decoracion_list = None
        self.vacuna_list = None
        self.muralla_list = None

        self.player_sprite = None  # VARIABLE DEL SPRITE
        self.virus_sprite = None  # VARIABLE DEL SPRITE
        self.virus2_sprite = None  # VARIABLE DEL SPRITE
        self.pisos_sprite = None  # ...
        self.objetos_sprite = None
        self.decoracion_sprite = None
        self.muralla_sprite = None
        self.vacuna_sprite = None

        self.physics_engine = None  # le damos características de la función physics_engine a nuestro objeto
        self.wall_list = None  # creamos esta característica para más adelante poder identificar ciertos objetos que no se pueden atravesar (piso, piso flotante).

        self.music = None
        self.current_song = 0
        self.music_list = []

        # Se utiliza para realizar un seguimiento de nuestro desplazamiento
        self.view_bottom = 0
        self.view_left = 0

        self.score = 0  # Lleva un registro de la puntuación

    def setup(self):  # inicializar las listas
        self.player_list = arcade.SpriteList()  # VA PERMITIR CONTROLAR COLISIONES/MOVIMIENTO
        self.virus_list = arcade.SpriteList()
        self.virus2_list = arcade.SpriteList()
        self.pisos_list = arcade.SpriteList()
        self.agua_list = arcade.SpriteList()
        self.lava_list = arcade.SpriteList()
        self.objetos_list = arcade.SpriteList()
        self.decoracion_list = arcade.SpriteList()
        self.player_sprite = arcade.AnimatedWalkingSprite()
        self.muralla_list = arcade.SpriteList()
        self.vacuna_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # con lo siguiente creamos el personaje y le damos movimiento animado(148 - 166)
        self.player_sprite.stand_right_textures = []
        self.player_sprite.stand_right_textures.append(arcade.load_texture("adventurer_stand.png"))

        self.player_sprite.stand_left_textures = []
        self.player_sprite.stand_left_textures.append(arcade.load_texture("adventurer_stand.png", mirrored=True))

        self.player_sprite.walk_right_textures = []
        self.player_sprite.walk_right_textures.append(arcade.load_texture("adventurer_walk1.png"))
        self.player_sprite.walk_right_textures.append(arcade.load_texture("adventurer_walk2.png"))

        self.player_sprite.walk_left_textures = []
        self.player_sprite.walk_left_textures.append(arcade.load_texture("adventurer_walk1.png", mirrored=True))
        self.player_sprite.walk_left_textures.append(arcade.load_texture("adventurer_walk2.png", mirrored=True))

        self.player_sprite.scale = escala_personaje
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 400
        self.player_list.append(self.player_sprite)

        # AMBIENTE
        sol = "sun1.png"
        self.decoracion_sprite = arcade.Sprite(sol, 1)
        self.decoracion_sprite.center_x = 50
        self.decoracion_sprite.center_y = 690
        self.decoracion_list.append(self.decoracion_sprite)

        letrero = "sign.png"
        self.decoracion_sprite = arcade.Sprite(letrero, 0.7)
        self.decoracion_sprite.center_x = 1100
        self.decoracion_sprite.center_y = 108
        self.decoracion_list.append(self.decoracion_sprite)

        piedra_x = [350, 900]
        for k in range(len(piedra_x)):
            piedra = "rock.png"
            self.decoracion_sprite = arcade.Sprite(piedra, 0.3)
            self.decoracion_sprite.center_x = piedra_x[k]
            self.decoracion_sprite.center_y = 80
            self.decoracion_list.append(self.decoracion_sprite)

        # Se utiliza para realizar un seguimiento de nuestro desplazamiento
        self.view_bottom = 0
        self.view_left = 0

        # Puntuación
        self.score = 0  # Lleva un registro de la puntuación

        for i in range(800, 1500, 150):
            pasto = arcade.Sprite("grass.png", escala_sol)
            pasto.center_x = i
            pasto.center_y = 937

        # CREAR VIRUS
        virus = Virus("virus.png", escala_virus)  # hereda las características de la clase Virus
        virus.center_x = 1107
        virus.center_y = 105
        self.virus_list.append(virus)

        # Segundo virus
        virus2 = Virus2("virus2.png", escala_virus2)  # hereda las características de la clase Virus
        virus2.center_x = 2100
        virus2.center_y = 105
        self.virus2_list.append(virus2)

        # crear piso con un loop de la imagen
        for i in range(320, 470, 64):
            piso = arcade.Sprite("grassMid.png", escala_piso)
            piso.center_x = i
            piso.center_y = 32
            self.pisos_list.append(piso)
            self.wall_list.append(piso)
        # el ciclo de arriba y este de abajo es para el piso con pastito
        for i in range(736, 1350, 64):
            piso = arcade.Sprite("grassMid.png", escala_piso)
            piso.center_x = i
            piso.center_y = 32
            self.pisos_list.append(piso)
            self.wall_list.append(piso)

        # ciclo para el agua
        for i in range(510, 710, 64):
            piso = arcade.Sprite("waterTop_high.png", escala_piso)
            piso.center_x = i
            piso.center_y = 32
            self.agua_list.append(piso)

        # tope del mapa por la izquierda
        n = 0
        while n <= 192:
            for k in range(0, 800, 64):
                pared = arcade.Sprite("grassCenter.png", escala_piso)
                pared.center_x = -128 - n
                pared.center_y = k
                self.wall_list.append(pared)
            n += 64

        # ciclo para la tierra superior con pasto
        for i in range(-64, 100, 64):
            piso = arcade.Sprite("grassMid.png", escala_piso)
            piso.center_x = i
            piso.center_y = 224
            self.pisos_list.append(piso)
            self.wall_list.append(piso)  # el piso no se puede atravesar

        # los 3 siguietes ciclos son para la tieraa sin pasto
        for p in range(-64, 256, 64):
            piso = arcade.Sprite("grassCenter.png", escala_piso)
            piso.center_x = p
            piso.center_y = 32
            self.pisos_list.append(piso)
            self.wall_list.append(piso)

        for p in range(-64, 128, 64):
            piso = arcade.Sprite("grassCenter.png", escala_piso)
            piso.center_x = p
            piso.center_y = 160
            self.pisos_list.append(piso)
            self.wall_list.append(piso)

        for p in range(-64, 192, 64):
            piso = arcade.Sprite("grassCenter.png", escala_piso)
            piso.center_x = p
            piso.center_y = 96
            self.pisos_list.append(piso)
            self.wall_list.append(piso)

        # sprite que muestra como si estuviera en bajada
        descenso = [[128, 224], [192, 160], [256, 96]]
        for p in range(len(descenso)):
            piso = arcade.Sprite("grassHill_left.png", escala_piso)
            piso.position = descenso[p]
            self.pisos_list.append(piso)
            self.wall_list.append(piso)

        # esquinas del piso
        esquinas = [[128, 160], [192, 96], [256, 32]]
        for p in range(len(esquinas)):
            piso = arcade.Sprite("grassCorner_left.png", escala_piso)
            piso.position = esquinas[p]
            self.pisos_list.append(piso)
            self.wall_list.append(piso)

        # asignar coordenadas fijas a el piso flotante
        coordenas_pisoflotante = [[40, 460], [185, 360], [210, 550], [330, 440], [400, 230], [480, 550], [600, 390],
                                  [730, 550], [820, 230], [840, 430], [1000, 550], [1020, 330], [1140, 435],
                                  [1200, 250], [1250, 550]]
        coordenas_para_los_objetos = []
        n = 1
        cosas = ["alcohol gel.png", "guantes.png", "mascara.png"]
        cte_eje_y = 50
        while n <= 11:
            coordenas__choicepisoflotante = random.choice(coordenas_pisoflotante)
            coordenas_pisoflotante.remove(coordenas__choicepisoflotante)

            cordenadas_lista = [coordenas__choicepisoflotante]
            coordenas_para_los_objetos.append(coordenas__choicepisoflotante)

            for p in cordenadas_lista:
                pisoaire = arcade.Sprite("ground_grass_small_broken.png", escala_pisovolador)
                pisoaire.position = p
                self.pisos_list.append(pisoaire)
                self.wall_list.append(pisoaire)  # el piso flotante no se puede atravesar

                n += 1

        for i in range(8):
            k = random.choice(coordenas_para_los_objetos)
            coordenas_para_los_objetos.remove(k)
            o = random.choice(cosas)

            if o == "alcohol gel.png":
                material = arcade.Sprite(o, escala_gel)
                material.position = k[0], k[1] + cte_eje_y
                self.objetos_list.append(material)
            elif o == "guantes.png":
                material = arcade.Sprite(o, escala_guantes)
                material.position = k[0], k[1] + cte_eje_y
                self.objetos_list.append(material)
            elif o == "mascara.png":
                material = arcade.Sprite(o, escala_mask)
                material.position = k[0], k[1] + cte_eje_y
                self.objetos_list.append(material)

        # carteles de flecha
        cont = 0
        for i in range(2):
            letrero_flecha = "signRight.png"
            self.decoracion_sprite = arcade.Sprite(letrero_flecha, 0.5)
            self.decoracion_sprite.center_x = 400 + cont
            self.decoracion_sprite.center_y = 95
            self.decoracion_list.append(self.decoracion_sprite)
            cont = 850

        for i in range(94, 1080, 80):
            muralla = arcade.Sprite("columna.png", escala_piso)
            muralla.center_x = 1325
            muralla.center_y = i
            self.muralla_list.append(muralla)
            self.wall_list.append(muralla)

        # SEGUNDA PIEZA
        # piso
        for i in range(1350, 1930, 64):
            piso = arcade.Sprite("stoneMid.png", escala_piso)
            piso.center_x = i
            piso.center_y = 32
            self.pisos_list.append(piso)
            self.wall_list.append(piso)

        for i in range(2196, 2390, 64):
            piso = arcade.Sprite("stoneMid.png", escala_piso)
            piso.center_x = i
            piso.center_y = 32
            self.pisos_list.append(piso)
            self.wall_list.append(piso)

        # lava
        for i in range(1940, 2140, 64):
            lava = arcade.Sprite("lavaTop_high.png", escala_piso)
            lava.center_x = i
            lava.center_y = 32
            self.lava_list.append(lava)

        # parte cemento
        for i in range(2586, 2750, 64):
            piso2 = arcade.Sprite("stoneMid.png", escala_piso)
            piso2.center_x = i
            piso2.center_y = 224
            self.pisos_list.append(piso2)
            self.wall_list.append(piso2)

        for i in range(2586, 2750, 64):
            piso = arcade.Sprite("stoneCenter.png", escala_piso)
            piso.center_x = i
            piso.center_y = 160
            self.pisos_list.append(piso)
            self.wall_list.append(piso)

        for i in range(2522, 2750, 64):
            piso = arcade.Sprite("stoneCenter.png", escala_piso)
            piso.center_x = i
            piso.center_y = 96
            self.pisos_list.append(piso)
            self.wall_list.append(piso)

        for p in range(2394, 2750, 64):
            piso = arcade.Sprite("stoneCenter.png", escala_piso)
            piso.center_x = p
            piso.center_y = 32
            self.pisos_list.append(piso)
            self.wall_list.append(piso)

        acenso = [[2522, 224], [2458, 160], [2394, 96]]
        for p in range(len(acenso)):
            piso = arcade.Sprite("stoneHill_right.png", escala_piso)
            piso.position = acenso[p]
            self.pisos_list.append(piso)
            self.wall_list.append(piso)

        esquinas2 = [[2522, 160], [2458, 96], [2394, 32]]
        for p in range(len(esquinas2)):
            piso = arcade.Sprite("stoneCorner_right.png", escala_piso)
            piso.position = esquinas2[p]
            self.pisos_list.append(piso)
            self.wall_list.append(piso)

        # tope del mapa por la derecha
        n = 0
        while n <= 192:
            for k in range(0, 800, 64):
                pared = arcade.Sprite("stoneCenter.png", escala_piso)
                pared.center_x = 2777 + n
                pared.center_y = k
                self.wall_list.append(pared)
            n += 64

        # plataformas
        agr_x = 1350

        coordenas_pisoflotante2 = [[1260 + agr_x, 460], [1115 + agr_x, 360], [1090 + agr_x, 550], [970 + agr_x, 440],
                                   [900 + agr_x, 230], [820 + agr_x, 550], [700 + agr_x, 390], [570 + agr_x, 550],
                                   [480 + agr_x, 230], [460 + agr_x, 430], [300 + agr_x, 550], [280 + agr_x, 330],
                                   [160 + agr_x, 435], [100 + agr_x, 250], [60 + agr_x, 550]]

        coordenas_para_los_objetos = []
        n = 1
        cosas = ["alcohol gel.png", "guantes.png", "mascara.png"]
        cte_eje_y = 50
        while n <= 11:
            coordenas__choicepisoflotante = random.choice(coordenas_pisoflotante2)
            coordenas_pisoflotante2.remove(coordenas__choicepisoflotante)
            cordenadas_lista = [coordenas__choicepisoflotante]
            coordenas_para_los_objetos.append(coordenas__choicepisoflotante)

            for p in cordenadas_lista:
                pisoaire = arcade.Sprite("ground_stone_small_broken.png", escala_pisovolador)
                pisoaire.position = p
                self.pisos_list.append(pisoaire)
                self.wall_list.append(pisoaire)  # el piso flotante no se puede atravesar
                n += 1

        for i in range(8):
            k = random.choice(coordenas_para_los_objetos)
            coordenas_para_los_objetos.remove(k)
            o = random.choice(cosas)

            if o == "alcohol gel.png":
                material = arcade.Sprite(o, escala_gel)
                material.position = k[0], k[1] + cte_eje_y
                self.objetos_list.append(material)
            elif o == "guantes.png":
                material = arcade.Sprite(o, escala_guantes)
                material.position = k[0], k[1] + cte_eje_y
                self.objetos_list.append(material)
            elif o == "mascara.png":
                material = arcade.Sprite(o, escala_mask)
                material.position = k[0], k[1] + cte_eje_y
                self.objetos_list.append(material)

        # le agregamos gravedad a nuestro personaje sin permitirle atravesar el piso ni el piso flotante.
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list)

        Audio().solo_una_vez("TheVirusIsComing.mp3")

    def gravedad(self):
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             gravity_constant=GRAVITY)

    def on_draw(self):
        # Se aclara todo lo que aparecerá en pantalla
        arcade.start_render()
        self.decoracion_list.draw()
        arcade.draw_text("PELIGRO!\nCOVID-19", 1100, 111, arcade.color.DARK_CANDY_APPLE_RED, 15, width=100,
                         align="center",
                         anchor_x="center", anchor_y="center")
        self.player_list.draw()
        self.pisos_list.draw()
        self.agua_list.draw()
        self.lava_list.draw()
        self.objetos_list.draw()
        self.wall_list.draw()
        self.virus_list.draw()
        self.virus2_list.draw()
        self.vacuna_list.draw()

        # Dibuja nuestro puntaje en la pantalla, desplazándolo con la ventana gráfica
#        score_text = f"Score: {self.score}"
#        arcade.draw_text(score_text, 10, 10, arcade.csscolor.WHITE, 18)

    def on_key_press(self, key, modifiers):  # se llama cada vez que presionamos una tecla

        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = JUMP_SPEED
                salto = Audio()  # Efecto sonido de salto cuando se presiona la tecla "UP"
                salto.solo_una_vez("salto.mp3")
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):  # para cuando el usuario suelta la tecla
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):  # Actualización

        self.player_list.update_animation()
        self.physics_engine.update()
        virus_hit = arcade.check_for_collision_with_list(self.player_sprite, self.virus_list)
        virus_hit2 = arcade.check_for_collision_with_list(self.player_sprite, self.virus2_list)
        # Mira si golpeamos algun objeto
        objetos_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.objetos_list)

        # Recorre cada objeto que golpeamos (si hay alguno) y lo retira el objeto de  para monedas en objetos_hit_list:
        for objetos in objetos_hit_list:
            # Remueve el objeto
            objetos.remove_from_sprite_lists()
            # Hace un sonido al "tomar" el objeto
            Audio().solo_una_vez("Recoger.mp3")
            self.score += 1  # Agrega uno al puntaje
        vacunas_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.vacuna_list)
        for objetos in vacunas_hit_list:
            # Remueve el objeto
            objetos.remove_from_sprite_lists()
            # Hace un sonido al "tomar" el objeto
            Audio().solo_una_vez("vacuna.mp3")
            self.score += 1  # Agrega uno al puntaje

            Audio().solo_una_vez("Gokillthevirus.mp3")

        if self.score >= 10:
            for virus2 in self.virus2_list:
                virus2.follow_sprite(self.player_sprite)

        for virus in self.virus_list:
            virus.follow_sprite(self.player_sprite)

        if self.score == 10 and virus_hit:
            Audio().solo_una_vez("TheSeconVirusIsComing.mp3")
            Audio().solo_una_vez("boing.mp3")
            for i in self.virus_list:
                i.remove_from_sprite_lists()
            for k in self.muralla_list:
                k.remove_from_sprite_lists()

        if self.score == 8:  # para que aparezca la vacuna
            cordenada_vacuna = [[40, 460], [210, 550], [600, 390], [730, 550], [185, 360], [330, 440], [1020, 330],
                                [480, 550], [840, 430], [400, 230], [820, 230], [1200, 250], [1250, 550], [1140, 435],
                                [1000, 550]]
            k = random.choice(cordenada_vacuna)
            vacuna = arcade.Sprite("VACUNA.png", 0.1)
            vacuna.position = k[0], k[1] + 50
            self.vacuna_list.append(vacuna)
            Audio().solo_una_vez("LookForTheVaccine.mp3")
            self.score = 9

        agr_x = 1350
        cte_eje_y = 64
        if self.score == 18:  # para que aparezca la vacuna
            cordenada_vacuna2 = [[1260 + agr_x, 460], [1115 + agr_x, 360], [1090 + agr_x, 550], [970 + agr_x, 440],
                                 [900 + agr_x, 230], [820 + agr_x, 550], [700 + agr_x, 390], [570 + agr_x, 550],
                                 [480 + agr_x, 230], [460 + agr_x, 430], [300 + agr_x, 550], [280 + agr_x, 330],
                                 [160 + agr_x, 435], [100 + agr_x, 250], [60 + agr_x, 550]]
            k = random.choice(cordenada_vacuna2)
            vacuna2 = arcade.Sprite("VACUNA.png", 0.1)
            vacuna2.position = k[0], k[1] + cte_eje_y
            self.vacuna_list.append(vacuna2)
            Audio().solo_una_vez("LookForTheVaccine.mp3")
            self.score = 19

        if (self.score < 10) and virus_hit:
            view = GameOverView("game-over.jpg")
            self.window.show_view(view)

        elif (self.score < 20) and virus_hit2:
            view = GameOverView("game-over.jpg")
            self.window.show_view(view)

        elif self.score == 20 and virus_hit2:
            view = Ventana_Ganador("WINNER.jpg")
            Audio().solo_una_vez("boing.mp3")
            self.window.show_view(view)

        # Para que pierda cuando toque el agua
        agua_hit = arcade.check_for_collision_with_list(self.player_sprite, self.agua_list)
        if agua_hit:
            time.sleep(.3)
            view = GameOverView("looser-agua.jpg")
            self.window.show_view(view)

        # Para que pierda cuando toque la lava
        lava_hit = arcade.check_for_collision_with_list(self.player_sprite, self.lava_list)
        if lava_hit:
            time.sleep(.3)
            view = GameOverView("looser-lava.jpg")
            self.window.show_view(view)

        # --- Administrar desplazamiento ---
        # Rastrear si necesitamos cambiar la ventana gráfica
        changed = False
        # Desplazarse a la izquierda
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        # Desplazarse a la derecha
        right_boundary = self.view_left + SCREE_WIDHT - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        if changed:
            # Solo desplazamiento en enteros. De lo contrario, terminamos con píxeles que
            # no se alineen en la pantalla
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

        # Hacer el seguimiento
        arcade.set_viewport(self.view_left,
                            SCREE_WIDHT + self.view_left,
                            self.view_bottom,
                            SCREE_HEIGHT + self.view_bottom)


class Audio:
    def __init__(self):
        super().__init__()
        # crear variables
        self.reproduce = None
        self.music = []
        self.rep = None
        self.indice = 0

    def solo_una_vez(self, archivo_audio):
        if self.reproduce:  # parar la música que se esta reproduciendo actualmente
            self.reproduce.stop()
        self.reproduce = arcade.Sound(archivo_audio, streaming=True)

        # definir volumen distinto para cada archivo
        if archivo_audio == "Musica_ganador.mp3" or archivo_audio == "vacuna.mp3" or archivo_audio == "salto.mp3" or\
                archivo_audio == "Recoger.mp3" or archivo_audio == "cancion.mp3":
            self.reproduce.play(MUSIC_VOLUME)
        else:
            self.reproduce.play(MUSIC_VOLUME_HIGH)
        time.sleep(0.03)


class GameOverView(arcade.View):

    def __init__(self, archivo_de_imagen):
        # Ver para mostrar cuando el juego termine
        super().__init__()
        self.texture = arcade.load_texture(archivo_de_imagen)
        Audio().solo_una_vez("GameOver.mp3")

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        # para restablecer la ventana gráfica al inicio para que podamos ver lo que dibujamos.
        arcade.set_viewport(0, SCREE_WIDHT, 0, SCREE_HEIGHT)
        # dibujar esta vista
        self.texture.draw_sized(SCREE_WIDHT/2, SCREE_HEIGHT/2, SCREE_WIDHT, SCREE_HEIGHT)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        # Si el usuario presiona el botón del mouse, reinicie el juego
        game_view = MyGame()
        game_view.setup()
        self.window.show_view(game_view)


class Ventana_Ganador(arcade.View):
    """ Ver para mostrar cuando gane el juego """

    def __init__(self, archivo_de_imagen):
        # Ver para mostrar cuando el juego termine
        super().__init__()
        self.texture = arcade.load_texture(archivo_de_imagen)
        Audio().solo_una_vez("YouWin.mp3")

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        # para restablecer la ventana gráfica al inicio para que podamos ver lo que dibujamos.
        arcade.set_viewport(0, SCREE_WIDHT, 0, SCREE_HEIGHT)
        # dibujar esta vista
        self.texture.draw_sized(SCREE_WIDHT / 2, SCREE_HEIGHT / 2,
                                SCREE_WIDHT, SCREE_HEIGHT)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        # Si el usuario presiona el botón del mouse, reinicie el juego
        game_view = MyGame()
        game_view.setup()
        self.window.show_view(game_view)


Audio().solo_una_vez("cancion.mp3")


def main():
    window = arcade.Window(SCREE_WIDHT, SCREE_HEIGHT, SCREE_TITLE)
    start_view = InstructionView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
