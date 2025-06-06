from typing import Dict, Any
from model.afd import AFD

def evaluar_cadena(afd: AFD, cadena : str) -> bool:
    """
    Evalúa si una cadena pertenece al lenguaje del AFD.

    Parámetros:
        afd (AFD): Autómata finito determinista generado.
        cadena (str): Cadena a evaluar.

    Retorna:
        bool: True si la cadena es aceptada, False en caso contrario.
    """
    estado_actual = afd.q0

    for simbolo in cadena:
        transicion = (estado_actual, simbolo)
        if transicion in afd.T:
            estado_actual = afd.T[transicion]
        else:
            # Transición no válida, la cadena no pertenece
            return False

    # La cadena es aceptada si termina en un estado final
    return estado_actual in afd.F

if __name__ == "__main__":
    cadena_prueba = "bbbab"
    aceptada = evaluar_cadena(afd, cadena_prueba)
    if aceptada:
        print(f"La cadena '{cadena_prueba}' es aceptada por el AFD.")
    else:
        print(f"La cadena '{cadena_prueba}' NO es aceptada por el AFD.")
