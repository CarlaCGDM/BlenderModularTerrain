# ModTerrain (Alpha)
Blender addon to generate procedural terrain from a modular tileset. Supports per-tile weight assignation to control frequency and distribution.

![ezgif com-gif-maker (2)](https://user-images.githubusercontent.com/92323990/174450132-d821260f-fc2e-4591-9d4a-02a2044221ec.gif)

## How to use
1. Download the ModTerrain.zip file and install, then activate the addon inside Blender.
2. Prepare a tileset where each tile is a 1m square object with the origin placed at the centre. Tiles that are meant to be placed next to each other must have matching geometry on that edge.
3. Put all your tiles in a collection and write the name of the collection in the textbox.
4. Hit the checkmark button to generate an adjacency index.
5. Set the size for your terrain (you can change it later without needing to regenerate the index).
6. Hit the generate button to generate your terrain.
7. Additionally, if you want to increase the frequency of a particular tile, select it and increase the number in the first panel property. This is the same as manually duplicating your tile to increase its odds of appearing on the final terrain.

## How it works
The core of the generator lies in reading each tile's 4 edges (north, south, east and west) to generate an index with the information of what tiles can be placed next to each other in each direction. Two tiles can be placed next to each other if the set of vertices on the matching edges are identical, as determined by the code snippet below.

![image](https://user-images.githubusercontent.com/92323990/174450654-37e7652e-58df-43cc-85e5-98d65d2dc3d8.png)


```python
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
```
I was inspired to create this system after watching Martin Donald's [wave function collapse algorithm video](https://www.youtube.com/watch?v=2SuvO4Gi7uY) (though this generator does not use WFC).

### V.1.0 (Alpha)
- I don't recommend using the detail generator yet (just place the smaller assets manually in the tiles before generating the index instead). If you really do want to use it, just put your detail assets in a collection called "Assets" and make sure the material you use for your the floors of your tiles is the first material in your tile. 
