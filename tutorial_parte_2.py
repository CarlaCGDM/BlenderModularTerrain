###############################################################################################
#                                                                                             #
#                         GENERADOR DE TERRENOS MODULARES EN BLENDER                          #
#                                                                                             #
#                                   github.com/CarlaCGDM                                      #
#                                                                                             #
###############################################################################################
###############################################################################################
#                                                                                             #
#                                  PREPARACIÓN DE MDÓULOS                                     #
#                                                                                             #
###############################################################################################

import bpy
import math
    
def comprobar_borde(modulo1,modulo2,direccion:tuple):
    
    #direcciones posibles: (0,1),(0,-1),(-1,0),(1,0)
    
    vertices_modulo1 = set()
    vertices_modulo2 = set()
    
    X,Y = direccion
    
    #izquierda y derecha
    if X == 0:
    
        for v in modulo1.data.vertices:
            y = round(v.co.y,1)
            if y == 0.5*Y:
                x = round(v.co.x,2)
                z = round(v.co.z,2)
                vertices_modulo1.add((x,z))
                
        for v in modulo2.data.vertices:
            y = round(v.co.y,1)
            if y == -0.5*Y:
                x = round(v.co.x,2)
                z = round(v.co.z,2)
                vertices_modulo2.add((x,z))
    
    #arriba y abajo      
    else:
        
        for v in modulo1.data.vertices:
            x = round(v.co.x,1)
            if x == 0.5*X:
                y = round(v.co.y,2)
                z = round(v.co.z,2)
                vertices_modulo1.add((y,z))
                
        for v in modulo2.data.vertices:
            x = round(v.co.x,1)
            if x == -0.5*X:
                y = round(v.co.y,2)
                z = round(v.co.z,2)
                vertices_modulo2.add((y,z))
            
    if vertices_modulo1 == vertices_modulo2:
        return True
    else:
        return False
    
def indice_conexiones(tileset:list):
    
    direcciones = [ (0,1), (0,-1), (1,0), (-1,0) ]
    indice = {}
    
    #rellenamos el indice
    for t in tileset:
        indice[t.name] = {}
        for dir in direcciones:
            indice[t.name][dir] = []
            for t2 in tileset:
                if comprobar_borde(t,t2,dir) == True:
                    indice[t.name][dir].append(t2.name)
        
    return indice


def rotaciones(tileset:list):
    
    #si ya existe la coleccion, borrarla:
    coll = bpy.data.collections.get("TilesetCompleto")
    if coll != None:
        for obj in coll.objects:
            m = obj.data
            bpy.data.objects.remove(obj)
            bpy.data.meshes.remove(m)
        bpy.data.collections.remove(coll)
    
    #colección para las rotaciones:
    coll = bpy.data.collections.new("TilesetCompleto")
    bpy.context.scene.collection.children.link(coll)

    
    #añadimos los objetos
    for t in tileset:
        
        t1 = bpy.data.objects.new(t.name + '_0', t.data.copy())
        coll.objects.link(t1)
        
        t2 = bpy.data.objects.new(t.name + '_90', t.data.copy())
        t2.rotation_euler[2] = math.radians(90)
        coll.objects.link(t2)
        
        t3 = bpy.data.objects.new(t.name + '_180', t.data.copy())
        t3.rotation_euler[2] = math.radians(180)
        coll.objects.link(t3)
        
        t4 = bpy.data.objects.new(t.name + '_270', t.data.copy())
        t4.rotation_euler[2] = math.radians(270)
        coll.objects.link(t4)
        
    #aplicamos la rotacion y los nombres de las mallas
    for obj in coll.objects:
        obj.data.name = obj.name
        obj.select_set(True)
        bpy.ops.object.transform_apply(rotation=True)
        
###############################################################################################
#                                                                                             #
#                                GENERACIÓN DE CUADRÍCULA                                     #
#                                                                                             #
###############################################################################################

import random

def grid_vacio(alto,ancho):
    
    #creamos la cuadrícula rellena de datos vacíos
    grid = []
    for i in range(alto):
        fila = []
        for j in range(ancho):
            fila.append("##No_Data##")
        grid.append(fila)
            
    return grid

def adyacentes_vacios(grid:list,celda:tuple):
    
    direcciones = [ (0,1), (0,-1), (1,0), (-1,0) ]
    vacios = []
    y,x = celda
    
    #por cada dirección, si la siguiente celda está vacía la guardamos
    for dir in direcciones:
        dy,dx = dir
        siguiente = (y+dy,x+dx)
        if siguiente[0] in range(len(grid)) and siguiente[1] in range(len(grid[0])):
            valor = grid[siguiente[0]][siguiente[1]]
            if valor == "##No_Data##":
                vacios.append(siguiente)
                
    return vacios

def adyacentes_ocupados(grid:list,celda:tuple):
    
    direcciones = [ (0,1), (0,-1), (1,0), (-1,0) ]
    ocupados = []
    
    #por cada dirección, si la siguiente celda está ocupada la guardamos junto con la dirección
    y,x = celda
    for dir in direcciones:
        dy,dx = dir
        siguiente = (y+dy,x+dx)
        if siguiente[0] in range(len(grid)) and siguiente[1] in range(len(grid[0])):
            valor = grid[siguiente[0]][siguiente[1]]
            if valor != "##No_Data##":
                ocupados.append(((-dy,-dx),valor)) 
                
    return ocupados

###############################################################################################
#                                                                                             #
#                                     PROGRAMA PRINCIPAL                                      #
#                                                                                             #
###############################################################################################

if __name__ == "__main__":
    
    #sets modulares
    tileset_inicial = []
    tileset_completo = []
    
    #rellenamos el primer set
    for obj in bpy.data.collections["TilesetInicial"].objects:
        tileset_inicial.append(obj)
    
    #generamos las rotaciones y rellenamos el segundo set
    rotaciones(tileset_inicial)
    
    for obj in bpy.data.collections["TilesetCompleto"].objects:
        tileset_completo.append(obj)

    #generamos el indice con la informacion de adyacencia
    indice = indice_conexiones(tileset_completo)
    
    #grid vacío
    alto,ancho = (10,10)
    grid = grid_vacio(alto,ancho)
    
    #colección para el terreno
    coll = bpy.data.collections.get("Terreno")
    if coll != None:
        for obj in coll.objects:
            bpy.data.objects.remove(obj)
        bpy.data.collections.remove(coll)
    
    terreno = bpy.data.collections.new('Terreno')
    bpy.context.scene.collection.children.link(terreno)
    
    #primera casilla
    inicio = (0,0)
    y,x = inicio
    
    modulo = random.choice(tileset_completo).data
    grid[y][x] = modulo.name
    obj = bpy.data.objects.new(modulo.name + '_Linked', modulo)
    terreno.objects.link(obj)
    obj.location = (x,y,0)
    
    #bucle de generación
    cola = []
    
    celdas_vecinas = adyacentes_vacios(grid,inicio)
    cola.extend(celdas_vecinas)
    
    while len(cola) > 0:
        
        siguiente = cola.pop()
        y,x = siguiente
        
        celdas_vecinas = adyacentes_ocupados(grid,siguiente)
        
        posibles = []
        
        # posibles = [["Esquina_270","Base_0",...],["Esquina_270"]]
        
        for cel in celdas_vecinas: # cel = ((0,-1),"Base_0") | (dirección,modulo)
            dir,nombre = cel 
            posibles.append(indice[nombre][dir])
            
        modulos_en_todos = list(set.intersection(*map(set, posibles)))
        
        #elegir el siguiente módulo al azar
        if len(modulos_en_todos) > 0:
            modulo = random.choice(modulos_en_todos)
            grid[y][x] = modulo
        
            #colocar una copia del modulo en el terreno
            modulo_m = bpy.data.objects[modulo].data
            obj = bpy.data.objects.new(modulo + '_Linked', modulo_m)
        
            terreno.objects.link(obj)
            obj.location = (y,x,0)
        
            #añadir sus adyacentes a la cola
            celdas_vecinas = adyacentes_vacios(grid,siguiente)
            for cel in celdas_vecinas:
                if cel not in cola:
                    cola.append(cel)
    
    #detalles sobre el terreno
    coll = bpy.data.collections.get("Detalles")
    if coll != None:
        for obj in coll.objects:
            bpy.data.objects.remove(obj)
        bpy.data.collections.remove(coll)
      
    detalles = bpy.data.collections.new('Detalles')
    bpy.context.scene.collection.children.link(detalles)
    
    assets = []
    
    #rellenamos la lista de opciones
    for obj in bpy.data.collections["Assets"].objects:
        assets.append(obj)
    
    
    for obj in bpy.data.collections.get('Terreno').objects:
        obj_loc = obj.location
        for face in obj.data.polygons:
            loc = obj_loc + face.center
            #si el material de la cara es el material hierba
            if face.material_index == 0:
                if random.randint(1,5) == 1:
                    #añadimos un asset al azar
                    asset = random.choice(assets).data
                    obj = bpy.data.objects.new(asset.name + "_Linked", asset)
                    detalles.objects.link(obj)
                    obj.location = loc
                    obj.rotation_euler[2] = math.radians(random.choice([0,90,180,270]))
    
    

        
