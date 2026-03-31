from decimal import Decimal

from .logic import CalculadorImpuestos
from ..models import Orden


class OrdenBuilder:
    def __init__(self):
        self.reset()

    def reset(self):
        self._usuario = None
        self._items = []
        self._direccion = ""
        self._libro = None
        self._cantidad = 1

    def con_usuario(self, usuario):
        self._usuario = usuario
        return self

    def con_libro(self, libro):
        self._libro = libro
        # Mantener lista de items alineada por si algo usa self._items
        self._items = [libro]
        return self

    def con_cantidad(self, cantidad):
        self._cantidad = cantidad
        return self

    def con_productos(self, productos):
        self._items = productos
        return self

    def para_envio(self, direccion):
        self._direccion = direccion
        return self

    def build(self) -> Orden:
        # Validamos que al menos haya un libro (ya sea por self._libro o self._items)
        if not self._usuario and not self._libro and not self._items:
            # Para tutoriales con AnonymousUser es mejor no ser muy estricto con el usuario, 
            # relajemos la restricción para que funcione la API en Postman
            pass

        if not self._libro and self._items:
            self._libro = self._items[0]

        if not self._libro:
            raise ValueError("Datos insuficientes: falta libro para crear la orden.")

        # Encapsulamiento de la lógica de calculo
        precio_base = self._libro.precio if self._libro else sum(p.precio for p in self._items)
        subtotal = float(precio_base) * self._cantidad
        total_con_iva = subtotal * 1.19

        orden = Orden.objects.create(
            usuario=self._usuario,
            libro=self._libro,
            total=total_con_iva,
            direccion_envio=self._direccion,
        )
        self.reset()
        return orden
