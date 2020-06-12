# consiste en crear una nueva clase a partir de otra
"""
class NombreSubClase(NombreClaseSuperior):

calss ClaseBase:
    Cuerpo de la clase base

class DerivadoClase(ClaseBase):
    Cuerpo de clase derivada

"""


class Pokemon:
    pass
    
    def __init__(self, nombre, tipo):
        self.nombre = nombre
        self.tipo = tipo

    def descripcion(self):
        return '{} es un pokemon del tipo {}'.format(self.nombre, self.tipo)


class Pikachu(Pokemon):  # enlazamos la clase pokemon con la pikachu (hijo) para poder usar sus parámetros
    def ataque(self, tipoataque):
        return '{} tipo de ataque: {}'.format(self.nombre, tipoataque)


class Charmander(Pokemon):  # otra clase hija
    def ataque(self, tipoataque):
        return '{} tipo de ataque: {}'.format(self.nombre, tipoataque)


nuevo_pokemon = Pikachu('boby', 'eléctrico')  # heredamos los atributos de la clase padre

print(nuevo_pokemon.descripcion())  # aca vemos que las características de la clase padre se heredan
print()
print(nuevo_pokemon.ataque(tipoataque='impacto trueno'))

