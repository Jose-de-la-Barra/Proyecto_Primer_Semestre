# un MÉTODO es una función que está dentro de una clase
# determina una accion o un comportamiento
# se llama a un método con el nómbre de DEF
# SELF es para referirse al objeto
# def.NombredelMetodo = algoritmo o valor específico

"""
class Matematica:
    def suma(self):
        self.n1 = 2  # variable n1 refiriendose al objeto de suma
        self.n2 = 3


# (s es un objeto al cual le vamos a aplicar funciones que estan dentro de la clase matematica)
s = Matematica() # objeto s que metemos dentro de la función Matemática
s.suma()
print(s.n1 + s.n2)  # estoy haciendo la suma fuera de la clase
"""

# __init__ (método que cumple una funcion de constructor) se puede calificar con el nombre de 'iniciar' o 'calificar'
# gracias a init vamos a poder realizar cualquier tipo de trabajo

class Ropa:
    def __init__(self):
        # creamos atributos
        self.marca = 'willow'
        self.talla = 'M'
        self.color = 'rojo'


camisa = Ropa()
print(camisa.talla)
print(camisa.marca)
print(camisa.color)

print()


class Calculadora:
    def __init__(self, n1, n2):
        self.suma = n1 + n2
        self.resta = n1 - n2
        self.mult = n1 * n2
        self.div = n1 / n2


operacion = Calculadora(2, 3)
print(operacion.div)
print(operacion.suma)
print(operacion.resta)
print(operacion.mult)
