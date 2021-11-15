"""
| En este archivo hice una clase que se encargará de procesar las físicas del auto.
| Debe ser importado en la tarea principal para que funcione. 
| La idea de separarlo en otro script es para separar las responsabilidades de ambos códigos.

"""

__author__ = "Ignacio Pinto"
__license__ = "MIT"


import numpy as np

# [Adicional]
class Auto:
    def __init__(self,X: float,Y: float,Z: float) -> None:
        self.MAX_SPEED = 6                  # Velocidad máxima que permitiremos alcanzar al auto
        self.CAR_ACCELERATION = 3           # Poder de aceleración del auto, mientras mayor el valor más rápido se acelerará
        self.CAR_ROTATION_SPEED = 2.5       # Poder de rotación del auto, mientras mayor el valor más rápido se rotará
        self.CAR_FRICTION = 1.5             # Fricción del auto, esto  controla que tan rápido decrece la velocidad al no acelerar.
        self.X = X
        self.Y = Y
        self.Z = Z 
        self.direction = 0
        self.speed = 0

        self.acceleration = 0               # Variable para recibir el input del acelerador
        self.steering = 0                   # Variable para recibir el input del manubrio

    def accelerate(self,direction):
        """Método para pisar el acelerador del vehículo"""
        assert (direction in [-1,0,1])
        self.acceleration = self.CAR_ACCELERATION*direction

    def steer(self,direction):
        """Método para mover el volante hacia los lados"""
        assert (direction in [-1,0,1])
        self.steering = direction


    def step(self,dt: float) -> None:
        """Ejecuta un paso físico no-discreto, donde dt es el tiempo que se tiene que procesar."""
        self.X += self.speed*np.sin(self.direction)*dt + 0.5*self.acceleration*(dt**2)
        self.Z += self.speed*np.cos(self.direction)*dt + 0.5*self.acceleration*(dt**2)

        self.speed += self.acceleration*dt
        self.direction += self.steering*self.CAR_ROTATION_SPEED*dt

        # Se le coloca un máximo a la velocidad.
        if abs(self.speed) > self.MAX_SPEED:
            self.speed = self.MAX_SPEED*np.sign(self.speed)

        # Se emula una fricción para que al no estar acelerando o frenando el auto se detenga eventualmente.
        if self.speed != 0: 
                self.speed = np.sign(self.speed)*max(0,abs(self.speed)-self.CAR_FRICTION*dt)

    def get_pos(self):
        return (self.X,self.Z)

# 
def interpolate_vectors(xi,zi,xf,zf,t):
    """Método que interpola entre dos puntos, t debe ir de 0 a 1"""
    return (xi + (xf-xi)*t, zi + (zf-zi)*t)

def interpolate_scalar(a,b,t):
    """Método que interpola entre dos puntos, t debe ir de 0 a 1"""
    return a + (b-a)*t


# [Método que parametriza la curva]
# t -> (x,z)
def car_curve(t):
    """Método que parametriza la curva del auto"""
    real_t = t%(32)

    if real_t >= 0 and real_t < 3.5: # tramo de 3.5
        _t = real_t/3.5
        return interpolate_vectors(2,2,2,5.5,_t)

    if real_t >= 3.5 and real_t < 3.5+6:    # tramo de 2*pi
        theta = interpolate_scalar(np.pi/2, 3*np.pi/2,(real_t-3.5)/6)
        return (2*np.sin(theta), 5.5 - 2*np.cos(theta))

    if real_t >= 3.5+6 and real_t < 3.5+6+10:    # tramo de 10
        _t = (real_t-(3.5+6))/10
        return interpolate_vectors(-2,5.5,-2,-4.5,_t)

    if real_t >= 3.5+6+10 and real_t < 3.5+6+10+6:   # tramo de 2*pi
        theta = interpolate_scalar(-1*np.pi/2, np.pi/2,(real_t-(3.5+6+10))/6)
        return (2*np.sin(theta), -4.5 - 2*np.cos(theta))
    
    if real_t >= 3.5+6+10+6 and real_t < 3.5+6+10+6+6.5: # tramo de 6.5
        _t = (real_t-(3.5+6+10+6))/6.5
        return interpolate_vectors(2,-4.5,2,2,_t)

def point_direction(x1,z1,x2,z2):
    x = x2-x1
    z = z2-z1

    dir = np.arctan2(x,z)
    return dir
    

    








