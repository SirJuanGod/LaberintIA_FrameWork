from OpenGL.GL.ARB import fragment_layer_viewport
import random
import numpy as np

def generar_laberinto_paredes(m, n):
    visited = np.zeros((m, n), dtype=bool)

    vertical_walls = np.ones((m, n + 1), dtype=bool)
    horizontal_walls = np.ones((m + 1, n), dtype=bool)

    def vecinos(i, j):
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(dirs)
        for di, dj in dirs:
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n and not visited[ni, nj]:
                yield ni, nj

    def quitar_pared(i, j, ni, nj):
        if ni == i and nj == j + 1:
            vertical_walls[i, j + 1] = False
        elif ni == i and nj == j - 1:
            vertical_walls[i, j] = False
        elif ni == i + 1 and nj == j:
            horizontal_walls[i + 1, j] = False
        elif ni == i - 1 and nj == j:
            horizontal_walls[i, j] = False

    def dfs(i, j):
        visited[i, j] = True
        for ni, nj in vecinos(i, j):
            if not visited[ni, nj]:
                quitar_pared(i, j, ni, nj)
                dfs(ni, nj)

    dfs(0, 0)

    return vertical_walls, horizontal_walls

def generar_xml_mujoco_desde_paredes(vertical_walls, horizontal_walls,
                                     escala=1.0, grosor=0.05, altura=0.4, suelo_size=10):
    m, n1 = vertical_walls.shape
    n = n1 - 1

    ancho_total = n * escala
    alto_total = m * escala

    origen_x = -ancho_total / 2
    origen_y = alto_total / 2

    xml = []
    xml.append('<mujoco model="laberinto_generado">')
    xml.append('    <compiler coordinate="local" inertiafromgeom="true"/>')
    xml.append('')
    xml.append('    <asset>')
    xml.append('        <texture name="suelo_textura" type="2d" builtin="checker" rgb1=".2 .3 .4" rgb2=".1 .2 .3" width="512" height="512" mark="none"/>')
    xml.append('        <material name="suelo_material" texture="suelo_textura" texrepeat="2 2" texuniform="true"/>')
    xml.append('    </asset>')
    xml.append('')
    xml.append('    <worldbody>')
    xml.append('        <light pos="0 0 5" dir="0 0 -1" directional="true"/>')
    xml.append(f'        <geom name="suelo" type="plane" pos="0 0 0" size="{suelo_size} {suelo_size} 0.1" material="suelo_material"/>')
    xml.append('')

    wall_id = 0

    # paredes verticales
    for i in range(m):
        for j in range(n + 1):
            if vertical_walls[i, j]:
                x = origen_x + j * escala
                y = origen_y - (i + 0.5) * escala

                xml.append(
                    f'        <geom name="vwall_{wall_id}" type="box" '
                    f'pos="{x} {y} {altura/2}" '
                    f'size="{grosor/2} {escala/2} {altura/2}" '
                    f'rgba="0.7 0.7 0.7 1"/>'
                )
                wall_id += 1

    # paredes horizontales
    for i in range(m + 1):
        for j in range(n):
            if horizontal_walls[i, j]:
                x = origen_x + (j + 0.5) * escala
                y = origen_y - i * escala

                xml.append(
                    f'        <geom name="hwall_{wall_id}" type="box" '
                    f'pos="{x} {y} {altura/2}" '
                    f'size="{escala/2} {grosor/2} {altura/2}" '
                    f'rgba="0.7 0.7 0.7 1"/>'
                )
                wall_id += 1

    xml.append(f'        <geom name="agente" type="box" pos="{origen_x + 0.5*escala} {origen_y - 0.5*escala} 0.2" size="0.15 0.15 0.15" rgba="1 0 0 1"/>')
    xml.append('    </worldbody>')
    xml.append('</mujoco>')

    return "\n".join(xml)

# === USAR ESTE CÓDIGO ===
if __name__ == "__main__":
    random.seed(42)

    m, n = 10, 10

    vertical_walls, horizontal_walls = generar_laberinto_paredes(m, n)

    xml_mujoco = generar_xml_mujoco_desde_paredes(
        vertical_walls,
        horizontal_walls,
        escala=1.0,
        grosor=0.1,
        altura=0.2,
        suelo_size=10
    )

    with open("laberinto_mujoco.xml", "w", encoding="utf-8") as f:
        f.write(xml_mujoco)