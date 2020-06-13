import arcade
import random
import time

SCREE_WIDHT = 1200
SCREE_HEIGHT = 600
SCREE_TITLE = "COVID ESCAPE"

# constantes para escalar sprites
escala_personaje = 0.20
escala_virus = 0.17
escala_piso = 0.30
escala_pisovolador = 0.30
escala_guantes = 0.05
escala_mask = 0.10
escala_gel = 0.05

MOVEMENT_SPEED = 5


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREE_WIDHT, SCREE_HEIGHT, SCREE_TITLE)
        arcade.set_background_color(arcade.color.ALICE_BLUE)

        self.player_list = None  # LISTA QUE CONTIENE PERSONAJE
        self.virus_list = None
        self.pisos_list = None
        self.objetos_list = None

        self.player_sprite = None  # VARIABLE DEL SPRITE
        self.virus_sprite = None  # VARIABLE DEL SPRITE
        self.pisos_sprite = None
        self.objetos_sprite = None

        self.physics_engine = None
        self.wall_list = None

    def setup(self):  # inicializar las listas
        self.player_list = arcade.SpriteList()  # VA PERMITIR CONTROLAR COLISIONES/MOVIMIENTO
        self.virus_list = arcade.SpriteList()
        self.pisos_list = arcade.SpriteList()
        self.objetos_list = arcade.SpriteList()

#        self.player_list.append(self.player_sprite)
        self.wall_list = arcade.SpriteList()

        # Crear personaje
        personaje = "monito.png"
        self.player_sprite = arcade.Sprite(personaje, escala_personaje)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 93
        self.player_list.append(self.player_sprite)

        # CREAR VIRUS
        virus = "virus.png"
        self.virus_sprite = arcade.Sprite(virus, escala_virus)
        self.virus_sprite.center_x = 1107
        self.virus_sprite.center_y = 105
        self.virus_list.append(self.virus_sprite)

        # crear piso
        for i in range(0, 1300, 114):
            piso = arcade.Sprite("piso.png", escala_piso)
            piso.center_x = i
            piso.center_y = 32
            self.pisos_list.append(piso)
            self.wall_list.append(piso)

        coordenas_pisoflotante = [[600, 430], [255, 200], [945, 200], [420, 320], [780, 320], [180, 460], [1107, 450]]
        for p in coordenas_pisoflotante:
            pisoaire = arcade.Sprite("Piso flotante.png", escala_pisovolador)
            pisoaire.position = p
            self.pisos_list.append(pisoaire)
            self.wall_list.append(pisoaire)

        # crear objetos

        cordenadas_objetos = [[600, 480], [255, 250], [945, 250], [420, 370], [780, 370], [180, 510], [1107, 500]]
        cosas = ["alcohol gel.png", "guantes.png", "mascara.png"]

        for j in cordenadas_objetos:
            o = random.choice(cosas)

            if o == "alcohol gel.png":
                material = arcade.Sprite(o, escala_gel)
                material.position = j
                self.objetos_list.append(material)

            elif o == "guantes.png":
                material = arcade.Sprite(o, escala_guantes)
                material.position = j
                self.objetos_list.append(material)

            elif o == "mascara.png":
                material = arcade.Sprite(o, escala_mask)
                material.position = j
                self.objetos_list.append(material)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                         self.wall_list)


        #random objetos
        #k=1
#        while k<=10:
 #           coordenas_objetos= [[random.randint(0,1200),random.randint(40,550)]]
  #          cosas = ["alcohol gel.png", "guantes.png", "mascara.png"]
   #         o=random.choice(cosas)
    #        for j in coordenas_objetos:
     #           if o=="alcohol gel.png":
      #              material=arcade.Sprite(o,escala_gel)
       #             material.position=j
        #            self.objetos_list.append(material)
         #           k+=1
          #      elif o=="guantes.png":
           #         material = arcade.Sprite(o, escala_guantes)
            #        material.position = j
             #       self.objetos_list.append(material)
              #      k += 1
               # elif o=="mascara.png":
                #    material = arcade.Sprite(o, escala_mask)
                 #   material.position = j
                  #  self.objetos_list.append(material)
                   # k += 1


        #MAPA ALEATORIO
#        n=1
 #       while n<=4:
  #          coordenas_pisoflotante = [[random.randint(0, 1200), random.randint(200, 450)]]
   #         for p in coordenas_pisoflotante:
    #            pisoaire=arcade.Sprite("Piso flotante.png",escala_pisovolador)
     #           pisoaire.position=p
      #          self.pisos_list.append(pisoaire)
       #         n=n+1
        #        print(p)

    def on_draw(self):
        arcade.start_render()
        self.player_list.draw()
        self.virus_list.draw()
        self.pisos_list.draw()
        self.objetos_list.draw()
        self.wall_list.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.physics_engine.update()


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()