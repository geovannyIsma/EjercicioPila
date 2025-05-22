# main.py
from stack import Stack
import tkinter as tk
from tkinter import messagebox

precedencia = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    '^': 3,
    '√': 4
}

def infija_a_postfija(expresion):
    operadores = Stack()
    salida = []
    elementos = expresion.split()

    for elemento in elementos:
        if elemento.isdigit():
            salida.append(elemento)
        elif elemento in "+-*/^√":
            while (not operadores.is_empty() and
                   operadores.peek() != '(' and
                   ((elemento != '^' and precedencia[operadores.peek()] >= precedencia[elemento]) or
                    (elemento == '^' and precedencia[operadores.peek()] > precedencia[elemento]))):
                salida.append(operadores.pop())
            operadores.push(elemento)
        elif elemento == '(':
            operadores.push(elemento)
        elif elemento == ')':
            while not operadores.is_empty() and operadores.peek() != '(':
                salida.append(operadores.pop())
            operadores.pop()

    while not operadores.is_empty():
        salida.append(operadores.pop())

    return salida

def evaluar_postfija(postfija):
    pila = Stack()

    for caracter in postfija:
        if caracter.isdigit():
            pila.push(int(caracter))
        elif caracter == '√':
            a = pila.pop()
            resultado = a ** 0.5
            pila.push(resultado)
        else:
            b = pila.pop()
            a = pila.pop()
            if caracter == '+':
                resultado = a + b
            elif caracter == '-':
                resultado = a - b
            elif caracter == '*':
                resultado = a * b
            elif caracter == '/':
                resultado = a / b
            elif caracter == '^':
                resultado = a ** b
            pila.push(resultado)

        print(f"\nDespués de procesar '{caracter}', estado de la pila:")
        pila.print()

    return pila.pop()

class PilaGUI:
    def __init__(self, master):
        self.master = master
        master.title("Visualización Interactiva de Pila")
        master.geometry("700x750")  # Reducir altura de la ventana

        font_label = ("Arial", 16)
        font_entry = ("Arial", 16)
        font_button = ("Arial", 14, "bold")
        font_result = ("Arial", 16, "bold")
        font_canvas = ("Arial", 14, "bold")  # Reducir tamaño de fuente para elementos de pila
        font_base = ("Arial", 12)

        self.label = tk.Label(master, text="Ingrese expresión infija (separada por espacios):", font=font_label)
        self.label.pack(pady=(20, 10))

        self.entry = tk.Entry(master, width=50, font=font_entry)
        self.entry.pack(pady=(0, 15))

        self.convertir_btn = tk.Button(master, text="Convertir a Postfija", command=self.convertir, font=font_button, height=2, width=20)
        self.convertir_btn.pack(pady=(0, 15))

        self.postfija_label = tk.Label(master, text="Expresión postfija:", font=font_label)
        self.postfija_label.pack(pady=(0, 10))
        
        # Contenedor para ambas pilas
        pilas_frame = tk.Frame(master)
        pilas_frame.pack(pady=10, fill=tk.X)
        
        # Marco para la pila de evaluación
        pila_eval_frame = tk.Frame(pilas_frame)
        pila_eval_frame.pack(side=tk.LEFT, padx=10, expand=True)
        
        tk.Label(pila_eval_frame, text="Pila de evaluación:", font=font_label).pack()
        self.canvas = tk.Canvas(pila_eval_frame, width=200, height=300, bg="white")  # Reducir dimensiones
        self.canvas.pack(pady=10)
        
        # Marco para la pila de expresión postfija
        pila_postfija_frame = tk.Frame(pilas_frame)
        pila_postfija_frame.pack(side=tk.RIGHT, padx=10, expand=True)
        
        tk.Label(pila_postfija_frame, text="Expresion postfijos:", font=font_label).pack()
        self.postfija_canvas = tk.Canvas(pila_postfija_frame, width=200, height=300, bg="white")  # Reducir dimensiones
        self.postfija_canvas.pack(pady=10)

        self.resultado_label = tk.Label(master, text="Resultado:", font=font_result)
        self.resultado_label.pack(pady=(10, 10))

        frame_botones = tk.Frame(master)
        frame_botones.pack(pady=(10, 0))

        self.step_btn = tk.Button(frame_botones, text="Siguiente paso", command=self.siguiente_paso, state='disabled', font=font_button, height=2, width=15)
        self.step_btn.pack(side=tk.LEFT, padx=20)
        self.reset_btn = tk.Button(frame_botones, text="Reiniciar", command=self.reiniciar, state='disabled', font=font_button, height=2, width=15)
        self.reset_btn.pack(side=tk.LEFT, padx=20)

        self.pasos = []
        self.paso_actual = 0
        self.pila = None
        self.postfija = []
        self.resultado = None
        
    def convertir(self):
        expresion = self.entry.get()
        if not expresion:
            messagebox.showerror("Error", "Ingrese una expresión.")
            return
        try:
            self.postfija = infija_a_postfija(expresion)
            self.postfija_label.config(text="Expresión postfija: " + ' '.join(self.postfija))
            self.resultado_label.config(text="Resultado:")
            self.pila = Stack()
            self.pasos = self.generar_pasos(self.postfija)
            self.paso_actual = 0
            self.dibujar_pila([])
            self.dibujar_postfija([])
            self.step_btn.config(state='normal')
            self.reset_btn.config(state='normal')
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def generar_pasos(self, postfija):
        pasos = []
        pila = []
        for caracter in postfija:
            accion = ""
            if caracter.isdigit():
                pila.append(int(caracter))
                accion = f"Push {caracter}"
            elif caracter == '√':
                a = pila.pop()
                resultado = a ** 0.5
                pila.append(resultado)
                accion = f"Pop {a} y push {resultado} (√{a})"
            else:
                b = pila.pop()
                a = pila.pop()
                if caracter == '+':
                    resultado = a + b
                elif caracter == '-':
                    resultado = a - b
                elif caracter == '*':
                    resultado = a * b
                elif caracter == '/':
                    resultado = a / b
                elif caracter == '^':
                    resultado = a ** b
                pila.append(resultado)
                accion = f"Pop {a}, {b} y push {resultado} ({a} {caracter} {b})"
            pasos.append((list(pila), accion, caracter))
        return pasos

    def siguiente_paso(self):
        if self.paso_actual < len(self.pasos):
            pila_estado, accion, token = self.pasos[self.paso_actual]
            self.dibujar_pila(pila_estado)
            
            tokens_procesados = self.postfija[:self.paso_actual + 1]
            self.dibujar_postfija(tokens_procesados)
            
            self.resultado_label.config(text=f"Paso {self.paso_actual+1}: {accion}")
            self.paso_actual += 1
            if self.paso_actual == len(self.pasos):
                self.resultado_label.config(text=f"Resultado: {pila_estado[-1]}")
                self.step_btn.config(state='disabled')

    def reiniciar(self):
        self.paso_actual = 0
        self.dibujar_pila([])
        self.dibujar_postfija([])
        self.resultado_label.config(text="Resultado:")
        self.step_btn.config(state='normal')

    def dibujar_pila(self, elementos):
        self.canvas.delete("all")
        x0, y0, x1, y1 = 50, 250, 150, 280  # Reducir tamaño y ajustar posición de elementos
        for i, elem in enumerate(elementos):
            self.canvas.create_rectangle(x0, y0 - i*40, x1, y1 - i*40, fill="#90caf9")  # Reducir espaciado vertical
            self.canvas.create_text((x0+x1)//2, (y0+y1)//2 - i*40, text=str(elem), font=("Arial", 14, "bold"))  # Reducir tamaño de fuente


    def dibujar_postfija(self, elementos):
        self.postfija_canvas.delete("all")
        x0, y0, x1, y1 = 50, 250, 150, 280  # Reducir tamaño y ajustar posición de elementos
        
        # Dibujar todos los elementos de la expresión postfija
        for i, elem in enumerate(self.postfija):
            color = "#90caf9" if i < len(elementos) else "#e0e0e0"  # Azul para procesados, gris para pendientes
            self.postfija_canvas.create_rectangle(x0, y0 - i*40, x1, y1 - i*40, fill=color)  # Reducir espaciado vertical
            self.postfija_canvas.create_text((x0+x1)//2, (y0+y1)//2 - i*40, text=str(elem), font=("Arial", 14, "bold"))  # Reducir tamaño de fuente
        
        # Indicar cuál es el elemento actual que se está procesando
        if elementos and len(elementos) < len(self.postfija):
            idx = len(elementos) - 1
            self.postfija_canvas.create_rectangle(x0-3, y0-3 - idx*40, x1+3, y1+3 - idx*40, outline="red", width=2)  # Ajustar el borde resaltado
        
if __name__ == "__main__":
    root = tk.Tk()
    gui = PilaGUI(root)
    root.mainloop()
