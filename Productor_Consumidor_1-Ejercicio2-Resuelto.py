import threading
import random
import logging
import time

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

"""
    Clase listaFinita, extiende la clase list ([]) de modo que puede establecerse un limite máximo
    al tamaño (cantidad de objetos) de la lista.

    Uso:
    Declaración
    lista = listaFinita(Numero_Maximo_Items)
    # Crea una lista VACIA que admitirá hasta un máximo de Numero_Maximo_Items items

    El acceso a los elementos es igual que en una lista standard, la diferencia es que
    si se intenta agregar un elemento cuando la lista tiene Numero_Maximo_Items items, dara
    un mensaje de error y terminara el programa.

    Ejemplos
    Acceso al elemento i:

    a = lista[i]

    insertar un elemento en la posicón i.
    lista.insert(i, dato)  # si i es mayor que Numero_Maximo_Items termina el programa y da error

    o

    lista[i] = dato   # Si i es mayor que Numero_Maximo_Items termina el programa y da error.

    agregar un elemento al final de la lista

    lista.append(dato)  # Si la lista tiene Numero_Maximo_Items termina el programa y da error.

"""

class listaFinita(list):

    def __init__(self, max_elementos):
            self.max_elementos = max_elementos
            super().__init__()

    def pop(self, index):
        assert len(self) != 0, "lista vacia"
        return super().pop(index)

    def append(self, item):
        assert len(self) < self.max_elementos,"lista llena"
        super().append(item)

    def insert(self, index, item):
        assert index < self.max_elementos, "indice invalido"
        super().insert(index, item)

    def full(self):
        if len(self) == self.max_elementos:
            return True
        else:
            return False


class Productor(threading.Thread):
    paises = [("España","Madrid"),("Francia","Paris"),("Italia","Roma"),("Inglaterra","Londres"),("Alemania","Berlin"),("Rusia","Moscu"),
              ("Turquia","Istambul"),("China","Pekin"),("Japon","Tokio"),("Emiratos Arabes","Dubai"),("Argentina","Buenos Aires"),
              ("Brasil","Brasilia"),("Colombia","Bogota"),("Uruguay","Montevideo")]

    def __init__(self, lista, lockLleno):
        super().__init__()
        self.lista = lista
        self.lockLleno = lockLleno

    #Seccion critica debido a, al igual que productor y consumidor del ejercicio anterior, productor quiere consumir un recurso que no se produjo
    def run(self):
        while True:
            self.lockLleno.acquire()
            try:
                while self.lista.full():
                    pass
                self.lista.append(self.paises[random.randint(0,len(self.paises)-1)])
                logging.info(f'produjo el item: {self.lista[-1]}')
                time.sleep(random.randint(1,5))
            finally:
                self.lockLleno.release()


class Consumidor(threading.Thread):
    def __init__(self, lista, lockVacio):
        super().__init__()
        self.lista = lista
        self.lockVacio = lockVacio


    def run(self):
        while True:
            self.lockVacio.acquire()
            try:
                while len(self.lista) == 0:
                    pass
                elemento = self.lista.pop(0)
                logging.info(f'La capital de {elemento[0]} es {elemento[1]}')
                time.sleep(random.randint(1,5))
            finally:
                self.lockVacio.release()

def main():
    hilos = []
    lista = listaFinita(4)
    #a diferencia del consumidor ejecicio primario, en este se realiza de forma polimofica, y se colocan dos Lock
    #en los runs de la clases, para que el productor pueda llenar la lista se aplica antes de que pueda cargar y despues para entregar el recurso
    #se pregunta si esta lleno desactiva el lock
    #a cambio de consumidorque libera una vez el tamaño de la lista sea = 0
    lockLleno = threading.Lock()
    lockVacio = threading.Lock()

    for i in range(4):
        productor = Productor(lista, lockLleno)
        consumidor = Consumidor(lista, lockVacio)
        hilos.append(productor)
        hilos.append(consumidor)
        #con logging info, se busca los valores del thread que se pasa como paramentro en la Clase
        logging.info(f'Arrancando productor {productor.name}')
        productor.start()

        logging.info(f'Arrancando productor {consumidor.name}')
        consumidor.start()
    #los treads se agregan a una lista, despues iteramos la lista de threads para poder ejec join para que corran juntos
    for h in hilos:
        h.join()


if __name__ == '__main__':
    main()
