import random as rd
from enum import Enum
from typing import List

# Enumeraciones para tipos de atributos y monstruos
class TipoAtributo(Enum):
    OSCURIDAD = "Oscuridad"
    LUZ = "Luz"
    TIERRA = "Tierra"
    AGUA = "Agua"
    FUEGO = "Fuego"
    VIENTO = "Viento"

class TipoMonstruo(Enum):
    LANZADOR_DE_CONJUROS = "Lanzador de Conjuros"
    DRAGON = "Dragón"
    ZOMBI = "Zombi"
    GUERRERO = "Guerrero"
    BESTIA = "Bestia"
    DEMONIO = "Demonio"

# Clase base Carta
class Carta:
    def __init__(self, nombre_carta: str, descripcion: str, jugador: 'Jugador'):
        self.__nombre_carta = nombre_carta
        self.__descripcion = descripcion
        self.__jugador = jugador

    def getNombreCarta(self):
        return self.__nombre_carta
    
    def setNombreCarta(self, nombre_carta: str):
        self.__nombre_carta = nombre_carta
    
    def getDescripcion(self):
        return self.__descripcion
    
    def getJugador(self):
        return self.__jugador
   

# Clase Monstruo que hereda de Carta
class Monstruo(Carta):
    def __init__(self, nombre_carta: str, descripcion: str, jugador: 'Jugador', ataque: int, defensa: int,
                 monstruo_tipo: TipoMonstruo, tipo_atributo: TipoAtributo):
        super().__init__(nombre_carta, descripcion, jugador)
        self._ataque = ataque
        self._defensa = defensa
        self._monstruo_tipo = monstruo_tipo
        self._tipo_atributo = tipo_atributo
        self._cartas_magicas: List['Magica'] = []
        self._cartas_trampa: List['Trampa'] = []

    def getAtaque(self):
        return self._ataque
    
    def getDefensa(self):
        return self._defensa
    
    def getTipoMonstruo(self):
        return self._tipo_monstruo
    
    def getTipoAtributo(self):
        return self._tipo_atributo
    
    def activar(self, en_ataque=True):
        # Activa la carta en ataque o defensa
        posicion = "ataque" if en_ataque else "defensa"
        print(f"{self.__nombre_carta} ha sido activada en {posicion} con {self._ataque} de ataque y {self._defensa} de defensa.")


# Clase Magica que hereda de Carta
class Magica(Carta):
    def __init__(self, nombre_carta: str, descripcion: str, incremento_ataque: int,
                 incremento_defensa: int, tipo_monstruo: Monstruo, es_equipable: bool, jugador: 'Jugador'):
        super().__init__(nombre_carta, descripcion, jugador)
        self._incremento_ataque = incremento_ataque
        self._incremento_defensa = incremento_defensa
        self._tipo_monstruo = tipo_monstruo
        self._es_equipable = es_equipable
    
    def getIncrementoAtaque(self):
        return self._incremento_ataque
    
    def getIncrementoDefensa(self):
        return self._incremento_defensa
    
    def getTipoMonstruo(self):
        return self._tipo_monstruo
    
    def getEsEquipable(self):
        return self._es_equipable

    def activar(self, carta_objetivo: Monstruo):
        # Aplica el incremento de ataque o defensa a una carta de monstruo
        if isinstance(carta_objetivo, Monstruo) and carta_objetivo.getTipoMonstruo() == self._tipo_monstruo:
            carta_objetivo._ataque += self._incremento_ataque
            carta_objetivo._defensa += self._incremento_defensa
            print(f"{self.__nombre_carta} activada: {carta_objetivo.__nombre_carta} incrementa su ataque en {self.incremento_ataque} y defensa en {self.incremento_defensa}.")
        else:
            print(f"{self.__nombre_carta} no tiene efecto en {carta_objetivo.__nombre_carta}.")

# Clase Trampa que hereda de Carta
class Trampa(Carta):
    def __init__(self, nombre_carta: str, descripcion: str, atributo_bloqueado: str,
                 efecto: str, activada: bool, tipo_monstruo: Monstruo, condicion_activacion: str, jugador: 'Jugador'):
        super().__init__(nombre_carta, descripcion, jugador)
        self._atributo_bloqueado = atributo_bloqueado
        self._activada = activada
        self._tipo_monstruo = tipo_monstruo
        self._condicion_activacion = condicion_activacion  
        
    def activar(self, carta_atacante: Monstruo):
        # Bloquea el ataque de un monstruo si su atributo coincide
        if carta_atacante.getTipoAtributo() == self._atributo_bloqueado:
            print(f"{self.__nombre_carta} activada: El ataque de {carta_atacante.__nombre_carta} ha sido bloqueado. {self.efecto}")
            return True
        else:
            print(f"{self.__nombre_carta} no tiene efecto en {carta_atacante.__nombre_carta}.")
            return False

# Clase Jugador

class Jugador:

    def __init__(self, nombre: str):
        self._nombre = nombre
        self._puntos_vida = 4000
        self._mazo = []
        self._mano_deck = []
        jugador1= Jugador("Andres")
        self._mazo.extend([
            Monstruo("Monstruo1", "dds",jugador1, 1500, 1000, TipoMonstruo.BESTIA, TipoAtributo.FUEGO)
            #Monstruo("Monstruo2", 1200),
            #Trampa("Trampa1"),
            #Magica("Magica1")
        ])

        self.crearDeck()
            
    def crearDeck(self):
        contadorMonstruo=0
        contadorTrampa=0
        contadorMagica=0
        while len(self.mano_deck)<15:
            for i in self.mazo:
                if isinstance(i, Monstruo) and contadorMonstruo<20:
                    self.mano_deck.append(i)
                    contadorMonstruo+=1
                elif isinstance(i, Trampa) and contadorTrampa<5:
                    self.mano_deck.append(i)
                    contadorTrampa+=1
                elif isinstance(i, Magica) and contadorMagica<5:
                    self.mano_deck.append(i)
                    contadorMagica+=1

    def getNombre(self):
        return self._nombre
    
    def getMazo(self):
        return self._mazo
    
    def getManoDeck(self):
        return self._mano_deck

    def robar_carta(self):
        if self._mazo:
            carta = self._mazo.pop(0)
            self._mano_deck.append(carta)
    
    def __str__(self):
        return f"Nombre:{self._nombre} \nVida: {self._puntos_vida} \nMazo: {self._mazo} \nDeck: {self._mano_deck}"

#Clase Tablero
class Tablero:
    def __init__(self, espacioCarta: List['Carta'], turno: int, jugador: List['Jugador']):
        self._espacioCarta = espacioCarta
        self._turno = turno
        self._jugador = jugador
    
    def getEspacioCarta(self):
        return self._espacioCarta
    
    def getTurno(self):
        return self._turno
    
    def getJugador(self):
        return self._jugador
    
#Cambios realizados 12/11/2024 22:33
#se eliminó toda la clase de maquina, ya que puede ser representado mejor por una instancia de jugador.
#se hicieron correcciones de tipo: modificardor de acceso
#se agregó atribustos faltantes a los super de las clases hijas
####Cambios realizados por Mero.



