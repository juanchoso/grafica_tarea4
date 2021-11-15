# coding=utf-8
"""Tarea 3"""

from Auto import Auto, car_curve, point_direction
import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.scene_graph as sg
import grafica.easy_shaders as es
import grafica.lighting_shaders as ls
import grafica.performance_monitor as pm
import grafica.text_renderer as tx
from grafica.assets_path import getAssetPath
from operator import add
from auxiliarT4 import *

__author__ = "Ivan Sipiran"
__license__ = "MIT"

# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.showAxis = True
        self.viewPos = np.array([12,12,12])
        self.at = np.array([0,0,0])
        self.camUp = np.array([0, 1, 0])
        self.distance = 20

#TAREA4: Esta clase contiene todos los parámetros de una luz Spotlight. Sirve principalmente para tener
# un orden sobre los atributos de las luces
class Spotlight:
    def __init__(self):
        self.ambient = np.array([0,0,0])
        self.diffuse = np.array([0,0,0])
        self.specular = np.array([0,0,0])
        self.constant = 0
        self.linear = 0
        self.quadratic = 0
        self.position = np.array([0,0,0])
        self.direction = np.array([0,0,0])
        self.cutOff = 0
        self.outerCutOff = 0

controller = Controller()
#TAREA4: aquí se crea el pool de luces spotlight (como un diccionario)
spotlightsPool = dict()

#TAREA4: Esta función ejemplifica cómo podemos crear luces para nuestra escena. En este caso creamos 2 luces con diferentes 
# parámetros
def setLights():
    #TAREA4: Primera luz spotlight
    spot1 = Spotlight()
    spot1.ambient = np.array([0.0, 0.0, 0.0])
    spot1.diffuse = np.array([1.0, 1.0, 1.0])
    spot1.specular = np.array([1.0, 1.0, 1.0])
    spot1.constant = 1.0
    spot1.linear = 0.09
    spot1.quadratic = 0.032
    spot1.position = np.array([2, 5, 0]) #TAREA4: esta ubicada en esta posición
    spot1.direction = np.array([0, -1, 0]) #TAREA4: está apuntando perpendicularmente hacia el terreno (Y-, o sea hacia abajo)
    spot1.cutOff = np.cos(np.radians(12.5)) #TAREA4: corte del ángulo para la luz
    spot1.outerCutOff = np.cos(np.radians(45)) #TAREA4: la apertura permitida de la luz es de 45°
                                                #mientras más alto es este ángulo, más se difumina su efecto
    
    spotlightsPool['spot1'] = spot1 #TAREA4: almacenamos la luz en el diccionario, con una clave única

    #TAREA4: Segunda luz spotlight
    spot2 = Spotlight()
    spot2.ambient = np.array([0.0, 0.0, 0.0])
    spot2.diffuse = np.array([1.0, 1.0, 1.0])
    spot2.specular = np.array([1.0, 1.0, 1.0])
    spot2.constant = 1.0
    spot2.linear = 0.09
    spot2.quadratic = 0.032
    spot2.position = np.array([-2, 5, 0]) #TAREA4: Está ubicada en esta posición
    spot2.direction = np.array([0, -1, 0]) #TAREA4: también apunta hacia abajo
    spot2.cutOff = np.cos(np.radians(12.5))
    spot2.outerCutOff = np.cos(np.radians(15)) #TAREA4: Esta luz tiene menos apertura, por eso es más focalizada
    spotlightsPool['spot2'] = spot2 #TAREA4: almacenamos la luz en el diccionario

    # luz 1 auto 1
    spot3 = Spotlight()
    spot3.ambient = np.array([0.0, 0.0, 0.0])
    spot3.diffuse = np.array([1.0, 1.0, 1.0])
    spot3.specular = np.array([1.0, 1.0, 1.0])
    spot3.constant = 0.1
    spot3.linear = 0.09
    spot3.quadratic = 0.032
    spot3.position = np.array([-2, 5, 0]) #TAREA4: Está ubicada en esta posición
    spot3.direction = np.array([0, -1, 0]) #TAREA4: también apunta hacia abajo
    spot3.cutOff = np.cos(np.radians(12.5))
    spot3.outerCutOff = np.cos(np.radians(15)) #TAREA4: Esta luz tiene menos apertura, por eso es más focalizada
    spotlightsPool['spot3'] = spot3 #TAREA4: almacenamos la luz en el diccionario

    # luz 2 auto 1
    spot4 = Spotlight()
    spot4.ambient = np.array([0.0, 0.0, 0.0])
    spot4.diffuse = np.array([1.0, 1.0, 1.0])
    spot4.specular = np.array([1.0, 1.0, 1.0])
    spot4.constant = 0.1
    spot4.linear = 0.09
    spot4.quadratic = 0.032
    spot4.position = np.array([-2, 5, 0]) #TAREA4: Está ubicada en esta posición
    spot4.direction = np.array([0, -1, 0]) #TAREA4: también apunta hacia abajo
    spot4.cutOff = np.cos(np.radians(12.5))
    spot4.outerCutOff = np.cos(np.radians(15)) #TAREA4: Esta luz tiene menos apertura, por eso es más focalizada
    spotlightsPool['spot4'] = spot4 #TAREA4: almacenamos la luz en el diccionario

    # luz 1 auto 2
    spot5 = Spotlight()
    spot5.ambient = np.array([0.0, 0.0, 0.0])
    spot5.diffuse = np.array([1.0, 1.0, 1.0])
    spot5.specular = np.array([1.0, 1.0, 1.0])
    spot5.constant = 0.1
    spot5.linear = 0.09
    spot5.quadratic = 0.032
    spot5.position = np.array([-2, 5, 0]) #TAREA4: Está ubicada en esta posición
    spot5.direction = np.array([0, -1, 0]) #TAREA4: también apunta hacia abajo
    spot5.cutOff = np.cos(np.radians(12.5))
    spot5.outerCutOff = np.cos(np.radians(15)) #TAREA4: Esta luz tiene menos apertura, por eso es más focalizada
    spotlightsPool['spot5'] = spot5 #TAREA4: almacenamos la luz en el diccionario

    # luz 2 auto 2
    spot6 = Spotlight()
    spot6.ambient = np.array([0.0, 0.0, 0.0])
    spot6.diffuse = np.array([1.0, 1.0, 1.0])
    spot6.specular = np.array([1.0, 1.0, 1.0])
    spot6.constant = 0.1
    spot6.linear = 0.09
    spot6.quadratic = 0.032
    spot6.position = np.array([-2, 5, 0]) #TAREA4: Está ubicada en esta posición
    spot6.direction = np.array([0, -1, 0]) #TAREA4: también apunta hacia abajo
    spot6.cutOff = np.cos(np.radians(12.5))
    spot6.outerCutOff = np.cos(np.radians(15)) #TAREA4: Esta luz tiene menos apertura, por eso es más focalizada
    spotlightsPool['spot6'] = spot6 #TAREA4: almacenamos la luz en el diccionario


#TAREA4: modificamos esta función para poder configurar todas las luces del pool
def setPlot(texPipeline, axisPipeline, lightPipeline):
    projection = tr.perspective(60, float(width)/float(height), 0.1, 100) #el primer parametro se cambia a 60 para que se vea más escena

    glUseProgram(axisPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(axisPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

    #TAREA4: Como tenemos 2 shaders con múltiples luces, tenemos que enviar toda esa información a cada shader
    #TAREA4: Primero al shader de color
    glUseProgram(lightPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(lightPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
    
    #TAREA4: Enviamos la información de la luz puntual y del material
    #TAREA4: La luz puntual está desactivada por defecto (ya que su componente ambiente es 0.0, 0.0, 0.0), pero pueden usarla
    # para añadir más realismo a la escena
    AMBIENT = 0.25
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].ambient"), AMBIENT, AMBIENT, AMBIENT)
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].diffuse"), 0.0, 0.0, 0.0)
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].specular"), 0.0, 0.0, 0.0)
    glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].constant"), 0.1)
    glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].linear"), 0.1)
    glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].quadratic"), 0.01)
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].position"), 5, 5, 5)

    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "material.ambient"), 0.2, 0.2, 0.2)
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "material.diffuse"), 0.9, 0.9, 0.9)
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "material.specular"), 1.0, 1.0, 1.0)
    glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, "material.shininess"), 32)

    #TAREA4: Aprovechamos que las luces spotlight están almacenadas en el diccionario para mandarlas al shader
    for i, (k,v) in enumerate(spotlightsPool.items()):
        baseString = "spotLights[" + str(i) + "]."
        glUniform3fv(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "ambient"), 1, v.ambient)
        glUniform3fv(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "diffuse"), 1, v.diffuse)
        glUniform3fv(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "specular"), 1, v.specular)
        glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "constant"), v.constant)
        glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "linear"), v.linear)
        glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "quadratic"), v.quadratic)
        glUniform3fv(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "position"), 1, v.position)
        glUniform3fv(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "direction"), 1, v.direction)
        glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "cutOff"), v.cutOff)
        glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "outerCutOff"), v.outerCutOff)

    #TAREA4: Ahora repetimos todo el proceso para el shader de texturas con mútiples luces
    glUseProgram(texPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(texPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
    

    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].ambient"), AMBIENT, AMBIENT, AMBIENT)
    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].diffuse"), 0.0, 0.0, 0.0)
    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].specular"), 0.0, 0.0, 0.0)
    glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].constant"), 0.1)
    glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].linear"), 0.1)
    glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].quadratic"), 0.01)
    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].position"), 5, 5, 5)

    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "material.ambient"), 0.2, 0.2, 0.2)
    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "material.diffuse"), 0.9, 0.9, 0.9)
    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "material.specular"), 1.0, 1.0, 1.0)
    glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, "material.shininess"), 32)

    for i, (k,v) in enumerate(spotlightsPool.items()):
        baseString = "spotLights[" + str(i) + "]."
        glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "ambient"), 1, v.ambient)
        glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "diffuse"), 1, v.diffuse)
        glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "specular"), 1, v.specular)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "constant"), v.constant)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "linear"), v.linear)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "quadratic"), v.quadratic)
        glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "position"), 1, v.position)
        glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "direction"), 1, v.direction)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "cutOff"), v.cutOff)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "outerCutOff"), v.outerCutOff)




def setView(texPipeline, axisPipeline, lightPipeline):
    view = tr.lookAt(
            controller.viewPos,
            controller.at,
            controller.camUp
        )

    glUseProgram(axisPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(axisPipeline.shaderProgram, "view"), 1, GL_TRUE, view)

    glUseProgram(texPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(texPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "viewPosition"), controller.viewPos[0], controller.viewPos[1], controller.viewPos[2])

    glUseProgram(lightPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(lightPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
    

def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_LEFT_CONTROL:
        controller.showAxis = not controller.showAxis

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)

if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 800
    height = 800
    title = "Tarea 3"
    window = glfw.create_window(width, height, title, None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Assembling the shader program (pipeline) with both shaders
    axisPipeline = es.SimpleModelViewProjectionShaderProgram()
    texPipeline = ls.MultipleLightTexturePhongShaderProgram()
    lightPipeline = ls.MultipleLightPhongShaderProgram()
    textPipeline = tx.TextureTextRendererShaderProgram()
    
    # Telling OpenGL to use our shader program
    glUseProgram(axisPipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory
    cpuAxis = bs.createAxis(7)
    gpuAxis = es.GPUShape().initBuffers()
    axisPipeline.setupVAO(gpuAxis)
    gpuAxis.fillBuffers(cpuAxis.vertices, cpuAxis.indices, GL_STATIC_DRAW)

    #NOTA: Aqui creas un objeto con tu escena
    #TAREA4: Se cargan las texturas y se configuran las luces
    loadTextures()
    setLights()

    dibujo = createStaticScene(texPipeline)
    car =createCarScene(lightPipeline)
    car_cpu = createCarScene(lightPipeline)
    casa = createHouse(texPipeline)
    
    
    # --- GRAFO DE ESCENA PARA LOS MUROS ---
    muros = createWall(texPipeline)

    

    setPlot(texPipeline, axisPipeline,lightPipeline)

    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)
    
    # ============ Velocímetro =============
    textTexture = tx.generateTextBitsTexture()
    gpuTexture = tx.toOpenGLTexture(textTexture)
    gpuSpeedometer = es.GPUShape().initBuffers()
    speedShape = tx.textToShape("0.0 mph",0.05,0.05)
    textPipeline.setupVAO(gpuSpeedometer)
    gpuSpeedometer.fillBuffers(speedShape.vertices, speedShape.indices, GL_STREAM_DRAW)
    gpuSpeedometer.texture = gpuTexture



    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)


    # ===========================================================
    # Variables globales
    # ===========================================================

    # Variables globales para almacenar la posición del auto y determinar las transformaciones a aplicar para la cámara
    auto_cpu = Auto(2.0, -0.037409, 2.0)
    auto = Auto(2.0, -0.037409, 5.0)

    auto_X = 2.0
    auto_Y = -0.037409
    auto_Z = 5.0
    car_theta = 0

    cam_X = 0
    cam_Y = 0
    cam_Z = 0

    # <======= Propiedades ajustables ========>
    camera_height = 0.75
    cam_radius = 2
    cam_angle = 0
    cam_fangle = 0

    # =========
    originalTime = 0
    t0 = glfw.get_time()

    while not glfw.window_should_close(window):

        # Measuring performance
        perfMonitor.update(glfw.get_time())
        glfw.set_window_title(window, title + str(perfMonitor))

        # Using GLFW to check for input events
        glfw.poll_events()

        # <===== Controlador =======>
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1 
        originalTime += dt

        # <============ Input: maniobrar (rotar) ===============>
        auto.steer(0)
        if (glfw.get_key(window, glfw.KEY_A) == glfw.PRESS):
            auto.steer(1)
        if (glfw.get_key(window, glfw.KEY_D) == glfw.PRESS):
            auto.steer(-1)
        
        #  <================= Input: acelerar ==================>
        pressed = False
        if (glfw.get_key(window, glfw.KEY_W) == glfw.PRESS):
            auto.accelerate(1)
            pressed = True
            
        if (glfw.get_key(window, glfw.KEY_S) == glfw.PRESS):
            auto.accelerate(-1)
            pressed = True
        
        if not pressed:
            auto.accelerate(0)

        auto.step(dt)
        newPos = car_curve(originalTime*3)
        dir = point_direction(auto_cpu.X,auto_cpu.Z,newPos[0],newPos[1])
        
        (auto_cpu.X,auto_cpu.Z) = newPos
        auto_cpu.direction = dir

        # Luz izquierda del auto
        
        angle_offset = 0.08         # Qué tan "chuecas" deben quedar las luces de los focos hacia afuera
        vertical_inclination = 0.03 # Inclinación hacia abajo de los focos
        light_separation = 0.10     # Separación de los focos contando desde el centro de la parte frontal del auto 
        forward_radius = 0.1        # Qué tan adelante se ubican los focos
        cutoff_angle = 10          # umbral de angulo mínimo
        outercutoff_angle = 14     # umbral de angulo máximo y difuminación

        target = auto   # Se define el auto sobre el cual trabajar

        lightL = spotlightsPool['spot3']
        l_X = target.X + forward_radius*np.sin(target.direction) + light_separation*np.sin(target.direction - np.pi/2)
        l_Z = target.Z + forward_radius*np.cos(target.direction) + light_separation*np.cos(target.direction - np.pi/2)
        lightL.cutOff = np.cos(np.radians(cutoff_angle))
        lightL.outerCutOff = np.cos(np.radians(outercutoff_angle))
        lightL.position = (l_X , target.Y + 0.1, l_Z )
        lightL.direction = (np.sin(target.direction - angle_offset), -vertical_inclination ,np.cos(target.direction - angle_offset))

        # Luz derecha del auto
        lightL = spotlightsPool['spot4']
        l_X = target.X + forward_radius*np.sin(target.direction) + light_separation*np.sin(target.direction + np.pi/2)
        l_Z = target.Z + forward_radius*np.cos(target.direction) + light_separation*np.cos(target.direction + np.pi/2)
        lightL.cutOff = np.cos(np.radians(cutoff_angle))
        lightL.outerCutOff = np.cos(np.radians(outercutoff_angle))
        lightL.position = (l_X , target.Y + 0.1, l_Z )
        lightL.direction = (np.sin(target.direction + angle_offset), -vertical_inclination , np.cos(target.direction + angle_offset))
        
        # <====== AUTO CONTROLADO POR LA CPU ====== >
        target = auto_cpu   # Se define el auto sobre el cual trabajar

        lightL = spotlightsPool['spot5']
        l_X = target.X + forward_radius*np.sin(target.direction) + light_separation*np.sin(target.direction - np.pi/2)
        l_Z = target.Z + forward_radius*np.cos(target.direction) + light_separation*np.cos(target.direction - np.pi/2)
        lightL.cutOff = np.cos(np.radians(cutoff_angle))
        lightL.outerCutOff = np.cos(np.radians(outercutoff_angle))
        lightL.position = (l_X , target.Y + 0.1, l_Z )
        lightL.direction = (np.sin(target.direction - angle_offset), -vertical_inclination ,np.cos(target.direction - angle_offset))

        # Luz derecha del auto
        lightL = spotlightsPool['spot6']
        l_X = target.X + forward_radius*np.sin(target.direction) + light_separation*np.sin(target.direction + np.pi/2)
        l_Z = target.Z + forward_radius*np.cos(target.direction) + light_separation*np.cos(target.direction + np.pi/2)
        lightL.cutOff = np.cos(np.radians(cutoff_angle))
        lightL.outerCutOff = np.cos(np.radians(outercutoff_angle))
        lightL.position = (l_X , target.Y + 0.1, l_Z )
        lightL.direction = (np.sin(target.direction + angle_offset), -vertical_inclination , np.cos(target.direction + angle_offset))


        
        # (auto.X,auto.Z) = car_curve(originalTime*3)


        car.transform = tr.matmul([tr.translate(auto.X,auto.Y,auto.Z), tr.rotationY(auto.direction)])
        car_cpu.transform = tr.matmul([tr.translate(auto_cpu.X,auto_cpu.Y,auto_cpu.Z), tr.rotationY(auto_cpu.direction)])
        
        # Efecto de suavizado de movimiento de cámara
        # [Adicional]
        cam_angle = auto.direction+np.pi

        # <===== Input: presionar botón F para ver en reversa =======>
        # [Adicional]
        if (glfw.get_key(window, glfw.KEY_F) == glfw.PRESS):
            cam_angle = auto.direction
        
        # <=========== Suavizado de cámara =============>
        # [Adicional]d
        if cam_fangle != cam_angle:
            cam_fangle += dt*7.5*(cam_angle-cam_fangle)

        cam_X = auto.X + (cam_radius * np.sin(cam_fangle))
        cam_Z = auto.Z + (cam_radius * np.cos(cam_fangle))
        cam_Y = auto.Y + camera_height
        
        controller.viewPos = np.array([cam_X,cam_Y,cam_Z])
        controller.at = np.array([auto.X, auto.Y, auto.Z])
        up = np.array([0,1,0])

        # <===== Controlador =======>

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        #TAREA4: Ojo aquí! Se configura la cámara y el dibujo en cada iteración. Esto es porque necesitamos que en cada iteración
        # las luces de los faros de los carros se actualicen en posición y dirección
        setView(texPipeline, axisPipeline, lightPipeline)
        setPlot(texPipeline, axisPipeline,lightPipeline)

        if controller.showAxis:
            glUseProgram(axisPipeline.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(axisPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
            axisPipeline.drawCall(gpuAxis, GL_LINES)

        #NOTA: Aquí dibujas tu objeto de escena
        glUseProgram(texPipeline.shaderProgram)
        sg.drawSceneGraphNode(dibujo, texPipeline, "model")
        sg.drawSceneGraphNode(casa, texPipeline, "model")
        sg.drawSceneGraphNode(muros, texPipeline, "model")


        glUseProgram(lightPipeline.shaderProgram)
        sg.drawSceneGraphNode(car, lightPipeline, "model")
        sg.drawSceneGraphNode(car_cpu, lightPipeline, "model")
        
        
        color = [1.0,1.0,1.0]
        speedometer_value = abs(round(auto.speed,1))

        # <=== Efecto de vibración en el velocímetro cuando la velocidad es mucha ===>
        # [Adicional]
        offsets = [(np.random.rand()*2) - 1,(np.random.rand()*2) - 1]
        shakeMag = 0
        if speedometer_value > 5:
            shakeMag = (speedometer_value-5)*0.02

        # [Adicional]
        # < ==== Velocímetro ==== >
        speedShape = tx.textToShape(f"{speedometer_value} mph",0.1,0.1)
        gpuSpeedometer.fillBuffers(speedShape.vertices, speedShape.indices, GL_STREAM_DRAW)
        gpuSpeedometer.texture = gpuTexture

        glUseProgram(textPipeline.shaderProgram)
        glUniform4f(glGetUniformLocation(textPipeline.shaderProgram, "fontColor"), color[0], color[1], color[2], 1.0)
        glUniform4f(glGetUniformLocation(textPipeline.shaderProgram, "backColor"), 1-color[0], 1-color[1], 1-color[2],0)
        glUniformMatrix4fv(glGetUniformLocation(textPipeline.shaderProgram, "transform"), 1, GL_TRUE,
            tr.translate(-0.9 + shakeMag*offsets[0], -0.9 + shakeMag*offsets[1], 0))
        textPipeline.drawCall(gpuSpeedometer)

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    # freeing GPU memory
    gpuAxis.clear()
    gpuSpeedometer.clear()
    dibujo.clear()
    

    glfw.terminate()