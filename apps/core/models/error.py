class NotSolvable(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("El modelo no tiene solución. Revise el tiempo de tránsito, rutas y fecha de entrega.", *args[1:])