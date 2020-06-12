# modificar un atributo


class Email:
    def __init__(self):
        self.enviado = False

    def enviar_correo(self):
        self.enviado = True


mi_correo = Email()

print(mi_correo.enviado)
print()
mi_correo.enviar_correo()  # especificamos la clase a la que nos queremos meter
print(mi_correo.enviado)
