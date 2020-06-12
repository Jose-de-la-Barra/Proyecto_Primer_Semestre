class Persona:
    edad = 27
    nombre = 'franco'
    pais = 'brasil'


doctor = Persona()  # a doctor le doy los aributos de Persona


print(f'La edad es: {doctor.edad}')
print('La edad es:', getattr(doctor, 'edad'))
print()

print('el doctor tine una edad?', hasattr(doctor, 'edad'))
print('el doctor tine una edad?', hasattr(doctor, 'apellido'))
print()

print(doctor.nombre)
setattr(doctor, 'nombre', 'hector')  # cabia el valor de lo que le indique en las primeras comillas por lo de las segundas.
print(doctor.nombre)
print()

print(doctor.pais)
delattr(Persona, 'pais')  # elimino el atributo país
# print(doctor.pais)  # me da error porque lo elimine
