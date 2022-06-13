###############################################################################################
#                                                                                             #
#                         GENERADOR DE TERRENOS MODULARES EN BLENDER                          #
#                                                                                             #
#                                   github.com/CarlaCGDM                                      #
#                                                                                             #
###############################################################################################
###############################################################################################
#                                                                                             #
#                                    FUNCIONES AUXILIARES                                     #
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
    
    direcciones = [
        (0,1),
        (0,-1),
        (1,0),
        (-1,0)
    ]
    
    indice = {}
    
    #rellenamos el indice
    for t in tileset:
        indice[t.name] = {}
        for d in direcciones:
            indice[t.name][d] = []
            for t2 in tileset:
                if comprobar_borde(t,t2,d) == True:
                    indice[t.name][d].append(t2.name)
        
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
    
    print(indice)
    
    
