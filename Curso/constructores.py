# __init__() cumple una función especial al igual que todas las funciones que tienen guión bajo
# a este tipo de funciones se les llama constructor


class Persona:
    pass  # se coloca para no tener ningun inconveniente. Le estoy diciendo que acá no están los atributos, sino que están más abajo

    def __init__(self, nombre, año):
        self.nombre = nombre  # se repiten para poder identificar cada uno de los valores y usarlos despues
        self.año = año

    def descripcion(self):  # Creamos métodos aparte del constructor
        return '{} tiene {} años'.format(self.nombre, self.año)  # la primera llave corresponde al primer elemento despues de format y lo mismo con la segunda

    # para ocupar un atributo que no este en la primera definición
    def comentario(self, frase):
        return '{} dice: {}'.format(self.nombre, frase)


doctor = Persona('PEDRO', 26)


print(doctor.nombre)
print()
print(doctor.descripcion())
print()
print(doctor.comentario('me gusta...'))
