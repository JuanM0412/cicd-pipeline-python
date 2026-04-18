"""
Módulo que proporciona funciones para operaciones matemáticas básicas.
"""

# IMPORTANTE: Reemplaza con tu nombre completo (debe coincidir con el nombre
# que uses en cualquier otro identificador del proyecto.
# Sugerencia: Usuario de correo de EAFIT)
AUTOR = "jmgomezp, mahoyosv, asjimenezm"


def sumar(a, b):
    """Suma dos números retornando su resultado."""
    return a + b


def restar(a, b):
    """Resta el segundo número al primero y devuelve el resultado."""
    return a - b


def multiplicar(a, b):
    """Multiplica dos números y devuelve el resultado."""
    return a * b


def dividir(a, b):
    """
    Divide el primer número por el segundo.
    Genera un error ZeroDivisionError si el segundo número es 0.
    """
    if b == 0:
        raise ZeroDivisionError("No se puede dividir por cero")
    return a / b
