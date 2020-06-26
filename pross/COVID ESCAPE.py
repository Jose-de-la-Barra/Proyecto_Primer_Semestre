import arcade
import random
import time
import os

SCREE_WIDHT = 1300
SCREE_HEIGHT = 700
SCREE_TITLE = "COVID ESCAPE"

# constantes para escalar sprites

escala_personaje = 0.7



escala_virus = 0.12
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


# Cuántos píxeles para mantener como margen mínimo entre el personaje
# y el borde de la pantalla.
# LEFT_VIEWPORT_MARGIN = 0
# RIGHT_VIEWPORT_MARGIN = 0
# BOTTOM_VIEWPORT_MARGIN = 0
# TOP_VIEWPORT_MARGIN = 0


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


class MyGame(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.ALICE_BLUE)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.player_list = None  # LISTA QUE CONTIENE PERSONAJE
        self.virus_list = None  # ...
        self.pisos_list = None
        self.objetos_list = None
        self.decoracion_list = None

        self.player_sprite = None  # VARIABLE DEL SPRITE
        self.virus_sprite = None  # VARIABLE DEL SPRITE
        self.pisos_sprite = None  # ...
        self.objetos_sprite = None
        self.decoracion_sprite = None

        self.physics_engine = None  # le damos características de la función physics_engine a nuestro objeto
        self.wall_list = None  # creamos esta característica para más adelante poder identificar ciertos objetos que no se pueden atravesar (piso, piso flotante).

        self.collect_objetos_sound = arcade.load_sound("Recoger.mp3")  # Sonido cuando toma cosas el personaje
        self.jump_sound = arcade.load_sound("salto.mp3")  # Efecto de sonido cuando salta el personaje

        # Se utiliza para realizar un seguimiento de nuestro desplazamiento
        self.view_bottom = 0
        self.view_left = 0

        self.score = 0  # Lleva un registro de la puntuaciónç

    def setup(self):  # inicializar las listas
        self.player_list = arcade.SpriteList()  # VA PERMITIR CONTROLAR COLISIONES/MOVIMIENTO
        self.virus_list = arcade.SpriteList()
        self.pisos_list = arcade.SpriteList()
        self.objetos_list = arcade.SpriteList()
        self.decoracion_list = arcade.SpriteList()

        #        self.player_list.append(self.player_sprite)
        self.wall_list = arcade.SpriteList()
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
            pasto.center_y = 93
            self.decoracion_list.append(pasto)

        # Crear personaje
        personaje = "adventurer_swim1.png"
        self.player_sprite = arcade.Sprite(personaje, escala_personaje)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 400
        self.player_list.append(self.player_sprite)

        # CREAR VIRUS
        virus = Virus("virus.png", escala_virus)  # hereda las características de la clase Virus
        virus.center_x = 1107
        virus.center_y = 105
        self.virus_list.append(virus)

        # crear piso con un loop de la imagen
        for i in range(320, 470, 64):
            piso = arcade.Sprite("grassMid.png", escala_piso)
            piso.center_x = i
            piso.center_y = 32
            self.pisos_list.append(piso)
            self.wall_list.append(piso)
            # el ciclo de arriba y este de abajo es para el piso con pastito
        for i in range(736, 1500, 64):
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
            self.pisos_list.append(piso)

        # ciclo para la tierra superior con pasto
        for i in range(0, 100, 64):
            piso = arcade.Sprite("grassMid.png", escala_piso)
            piso.center_x = i
            piso.center_y = 224
            self.pisos_list.append(piso)
            self.wall_list.append(piso)  # el piso no se puede atravesar
        # los 3 siguietes ciclos son para la tieraa sin pasto
        for p in range(0, 256, 64):
            piso = arcade.Sprite("grassCenter.png", escala_piso)
            piso.center_x = p
            piso.center_y = 32
            self.pisos_list.append(piso)
            self.wall_list.append(piso)

        for p in range(0, 128, 64):
            piso = arcade.Sprite("grassCenter.png", escala_piso)
            piso.center_x = p
            piso.center_y = 160
            self.pisos_list.append(piso)
            self.wall_list.append(piso)

        for p in range(0, 192, 64):
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


        coordenas_pisoflotante = [[40,460], [210, 550],[600, 390],[730,550],[185,360] ,[330, 440],[1020, 330], [480, 550], [840, 430],[400,230], [820,230],[1200,250],[1250,550],[1140,435],[1000,550]]
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
                self.wall_list.append(pisoaire) # el piso flotante no se puede atravesar

                n += 1





        for i in range(8):
            k = random.choice(coordenas_para_los_objetos)
            coordenas_para_los_objetos.remove(k)
            o = random.choice(cosas)

            if o == "alcohol gel.png":
                material = arcade.Sprite(o, escala_gel)
                material.position = k[0], k[1]+cte_eje_y
                self.objetos_list.append(material)
            elif o == "guantes.png":
                material = arcade.Sprite(o, escala_guantes)
                material.position = k[0], k[1]+cte_eje_y
                self.objetos_list.append(material)
            elif o == "mascara.png":
                material = arcade.Sprite(o, escala_mask)
                material.position = k[0], k[1]+cte_eje_y
                self.objetos_list.append(material)



        # le agregamos gravedad a nuestro personaje sin permitirle atravesar el piso ni el piso flotante.
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list)

    def gravedad(self):
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             gravity_constant=GRAVITY)

    def on_draw(self):
        arcade.start_render()
        self.decoracion_list.draw()
        arcade.draw_text("PELIGRO!\nCOVID-19", 1100, 111, arcade.color.DARK_CANDY_APPLE_RED, 15, width=100,
                         align="center",
                         anchor_x="center", anchor_y="center")
        self.player_list.draw()
        self.pisos_list.draw()
        self.objetos_list.draw()
        self.wall_list.draw()
        self.virus_list.draw()

        # Dibuja nuestro puntaje en la pantalla, desplazándolo con la ventana gráfica
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10, 10, arcade.csscolor.WHITE, 18)

    def on_key_press(self, key, modifiers):  # se llama cada vez que presionamos una tecla

        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = JUMP_SPEED
                arcade.play_sound(self.jump_sound)  # Efecto sonido de salto cuando se presiona la tecla "UP"
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):  # para cuando el usuario suelta la tecla
        """Called when the user releases a key. """
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):  # Actualización

        self.physics_engine.update()
        virus_hit = arcade.check_for_collision_with_list(self.player_sprite, self.virus_list)

        # Mira si golpeamos algun objeto
        objetos_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.objetos_list)
        # Recorre cada objeto que golpeamos (si hay alguno) y lo retira el objeto de  para monedas en objetos_hit_list:
        for objetos in objetos_hit_list:
            # Remueve el objeto
            objetos.remove_from_sprite_lists()
            # Hace un sonido al "tomar" el objeto
            arcade.play_sound(self.collect_objetos_sound)
            self.score += 1  # Agrega uno al puntaje





        for virus in self.virus_list:
            virus.follow_sprite(self.player_sprite)

        if self.score == 8:
            cordenada_vacuna = [[40,460], [210, 550],[600, 390],[730,550],[185,360] ,[330, 440],[1020, 330], [480, 550], [840, 430],[400,230], [820,230],[1200,250],[1250,550],[1140,435],[1000,550]]
            k = random.choice(cordenada_vacuna)
            vacuna = arcade.Sprite("VACUNA.png", 0.1)
            vacuna.position = k[0] , k[1] + 50
            self.objetos_list.append(vacuna)
            self.score = 9

        if (self.score < 10) and virus_hit:
            view = GameOverView()
            self.window.show_view(view)
        #elif self.score == 8:

            #cordenada_vacuna = [[40, 460], [210, 550], [600, 390]]
            #k = random.choice(cordenada_vacuna)
            #vacuna = arcade.Sprite("VACUNA.png", 0.1)
            #vacuna.position = k[0], k[1]+50
            #self.objetos_list.append(vacuna)
                
        elif self.score == 10 and virus_hit:
            view = Ventana_Ganador()
            self.window.show_view(view)



class GameOverView(arcade.View):
    """ View to show when game is over """

    def __init__(self):
        """ This is run once when we switch to this view """
        super().__init__()
        self.texture = arcade.load_texture("Restart.png")

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREE_WIDHT - 1, 0, SCREE_HEIGHT - 1)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        self.texture.draw_sized(SCREE_WIDHT / 2, SCREE_HEIGHT / 2,
                                SCREE_WIDHT, SCREE_HEIGHT)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, re-start the game. """
        game_view = MyGame()
        game_view.setup()
        self.window.show_view(game_view)


class Ventana_Ganador(arcade.View):
    """ View to show when game is over """

    def __init__(self):
        """ This is run once when we switch to this view """
        super().__init__()
        self.texture = arcade.load_texture("ganador.jpg")

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREE_WIDHT - 1, 0, SCREE_HEIGHT - 1)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        self.texture.draw_sized(SCREE_WIDHT / 2, SCREE_HEIGHT / 2,
                                SCREE_WIDHT, SCREE_HEIGHT)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, re-start the game. """
        game_view = MyGame()
        game_view.setup()
        self.window.show_view(game_view)


#        if self.score == 9:
#            view = Ventana_Ganador()
#            self.window.show_view(view)

# --- Administrar desplazamiento ---

# Rastrear si necesitamos cambiar la ventana gráfica
# changed = False

# Desplazarse a la izquierda
# left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
# if self.player_sprite.left < left_boundary:
# self.view_left -= left_boundary - self.player_sprite.left
# changed = True

# Desplazarse a la derecha
# right_boundary = self.view_left + SCREE_WIDHT - RIGHT_VIEWPORT_MARGIN
# if self.player_sprite.right > right_boundary:
# self.view_left += self.player_sprite.right - right_boundary
# changed = True

# Desplazarse hacia arriba
# top_boundary = self.view_bottom + SCREE_HEIGHT - TOP_VIEWPORT_MARGIN
# if self.player_sprite.top > top_boundary:
# self.view_bottom += self.player_sprite.top - top_boundary
# changed = True

# Desplazarse hacia abajo
# bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
# if self.player_sprite.bottom < bottom_boundary:
# self.view_bottom -= bottom_boundary - self.player_sprite.bottom
# changed = True

# if changed:
# Solo desplazamiento en enteros. De lo contrario, terminamos con píxeles que
# no se alineen en la pantalla
# self.view_bottom = int(self.view_bottom)
# self.view_left = int(self.view_left)

# Do the scrolling
# arcade.set_viewport(self.view_left,
# SCREE_WIDHT + self.view_left,
# self.view_bottom,
# SCREE_HEIGHT + self.view_bottom)


def main():
    window = arcade.Window(SCREE_WIDHT, SCREE_HEIGHT, SCREE_TITLE)
    start_view = MyGame()
    window.show_view(start_view)
    start_view.setup()
    arcade.run()


if __name__ == "__main__":
    main()

