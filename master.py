import arcade


# como esta dentro de una clase, la función se llama método. Python reconoce __init__ y cada vez que se
# crea un objeto, se va a ejecutar automáticamente lo que sigue despues de el __init__
# En la variable self se va a guardar la referencia al objeto que esté creando
# Super sirve para darle más importancia a una clase secundaria y poder ocuparla sin ocupar su nombre.

class VentanaJuego(arcade.Ventana):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.set_location(80, 50)


VentanaJuego(1280, 720, 'La ventana del juego')

arcade.run()

