from node import Node

class Stack:
    def __init__(self):
        self.top = None

    def is_empty(self):
        """
        Verifica si la pila está vacía.

        Returns:
            bool: True si la pila está vacía, False en caso contrario.
        """
        return self.top is None

    def push(self, value):
        """
        Agrega un nuevo elemento a la pila.

        Args:
            value: El valor del elemento a agregar.
        """
        new_node = Node(value)
        new_node.next = self.top
        self.top = new_node

    def pop(self):
        """
        Elimina y devuelve el elemento en la parte superior de la pila.

        Returns:
            El valor del elemento eliminado.

        Raises:
            IndexError: Si la pila está vacía.
        """
        if self.is_empty():
            raise IndexError("La pila está vacía")
        value = self.top.value
        self.top = self.top.next
        return value

    def peek(self):
        """
        Devuelve el elemento en la parte superior de la pila sin eliminarlo.

        Returns:
            El valor del elemento en la parte superior.

        Raises:
            IndexError: Si la pila está vacía.
        """
        if self.is_empty():
            raise IndexError("La pila está vacía")
        return self.top.value

    def print(pila, nombre="Pila"):
        print(f"{nombre}: ", end='')
        elementos = []
        actual = pila.top
        while actual:
            elementos.append(str(actual.value))
            actual = actual.next
        print(" -> ".join(elementos) if elementos else "[vacía]")

