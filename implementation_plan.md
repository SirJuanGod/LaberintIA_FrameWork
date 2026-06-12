# Reestructuración del Workspace ROS 2 LaberintIA para Gazebo + RL Training

## Contexto

El proyecto consta de un robot de tracción diferencial (2 ruedas + base) diseñado en Onshape y exportado con `onshape-to-robot`. El objetivo es entrenarlo mediante Reinforcement Learning (TD3) en un entorno de laberinto en Gazebo. Actualmente hay **múltiples problemas críticos** que impiden su funcionamiento y la arquitectura requiere una actualización a ROS 2.

## Diagnóstico de Problemas Encontrados

### 🔴 Problemas Críticos (Bloquean compilación y ejecución)

| # | Problema | Ubicación | Impacto |
|---|---------|-----------|---------|
| 1 | **URIs absolutas de Windows** en el SDF: `model://d:\USC\Proyectos\...` | [Robot.sdf](file:///d:/USC/Proyectos/LaberintIA/LaberintIA_FrameWork/model/Robot.sdf) | Gazebo no encuentra las meshes |
| 2 | **Package name incorrecto** `package://tu_paquete/meshes/...` | [base.xacro](file:///d:/USC/Proyectos/LaberintIA/LaberintIA_FrameWork/rbt_ws/src/laberintia_crtll/xacro/laberintia/base.xacro) y [wheel.xacro](file:///d:/USC/Proyectos/LaberintIA/LaberintIA_FrameWork/rbt_ws/src/laberintia_crtll/xacro/laberintia/wheel.xacro) | xacro no resuelve las meshes |
| 3 | **base.xacro usa geometría placeholder** (box genérica 0.2x0.15x0.1) en vez de las meshes STL reales | [base.xacro](file:///d:/USC/Proyectos/LaberintIA/LaberintIA_FrameWork/rbt_ws/src/laberintia_crtll/xacro/laberintia/base.xacro) | Robot no se ve como el diseño CAD |
| 4 | **No hay plugins de Gazebo** en la descripción del robot (diff_drive, sensores) | Xacros | Robot no acepta comandos de velocidad ni percibe el entorno |
| 5 | **El entrenamiento usa ROS 1** (`rospy`, `roslaunch`) | [environment.py](file:///d:/USC/Proyectos/LaberintIA/LaberintIA_FrameWork/lbrintia/environment.py) | Incompatible con ROS 2 |
| 6 | **setup.py no instala subdirectorios de meshes** | [setup.py](file:///d:/USC/Proyectos/LaberintIA/LaberintIA_FrameWork/rbt_ws/src/laberintia_crtll/setup.py) L23-27 | Las carpetas de meshes no se copian al instalar el paquete |
| 7 | **robot.xacro fija base al mundo** con joint fixed | [robot.xacro](file:///d:/USC/Proyectos/LaberintIA/LaberintIA_FrameWork/rbt_ws/src/laberintia_crtll/xacro/laberintia/robot.xacro) L8-14 | Robot no puede moverse |

### 🟡 Problemas Secundarios y Limpieza

1. **Archivos MuJoCo**: Hay una mezcla de simuladores. Según las indicaciones, se eliminará todo lo relacionado con MuJoCo.
2. **Duplicación de carpetas**: `robot/` es una copia de referencia y sus archivos útiles ya están en `rbt_ws`.
3. **Archivos innecesarios**: `.part` de Onshape y carpetas de build/install cacheadas que deben regenerarse.
4. **Escala del laberinto**: Las paredes del laberinto en `TD3.world` (ej. -2.15, 1.85, 3.2, etc.) indican un área de aproximadamente +/- 4 metros. El robot es pequeño (~15cm). La lógica de penalización en `environment.py` verifica un área de +/- 10m y evita zonas específicas. La escala es aceptable para entrenamiento, pero requerirá validar que las coordenadas de obstáculos en `check_pos()` correspondan a las del mundo.

---

## User Review Required

> [!IMPORTANT]
> **Compatibilidad ROS 2**: Se actualizará el código de `environment.py` y `train.py` a la sintaxis y librerías de ROS 2 (`rclpy`).

> [!IMPORTANT]
> **Sensor de Distancia (HC-SR04)**: En lugar de usar o simular el masivo Velodyne, agregaré a la descripción del robot (xacro) un sensor Ray (láser de un solo haz o cono muy estrecho) configurado para actuar como un sensor ultrasónico HC-SR04 real (rango 0.02 a 4.0 metros, FOV estrecho). Esto simplificará la red neuronal, que dejará de necesitar reducir el array de PointCloud y trabajará directamente con los valores de distancia de este sensor simple.

## Open Questions

- ¿Cuántos sensores HC-SR04 tiene el robot físico y dónde están ubicados (ej: 1 al frente, o 1 frente, 1 izq, 1 der)? El código base usaba las lecturas de un Velodyne 360° dividido en bins. Modificaré el código de la red neuronal para tomar la lectura exacta de los HC-SR04 que definamos. Asumiré por ahora 1 al frente y 2 a los lados (total 3 lecturas), según lo que vi en `sensors.xacro` donde defines esferas roja, azul y verde (front, left, right).

---

## Proposed Changes

### Fase 1: Limpieza Estricta del Repositorio

Se eliminarán los siguientes archivos y carpetas que generan conflicto o son código muerto:

#### [DELETE] Archivos y carpetas a eliminar
```
# Carpeta de referencia de GitHub
robot/

# Archivos sueltos innecesarios
model_sdf/
model/Robot.xml
model/HexaBot.xml
model/Laberinto.xml
model/scene.xml
model/assets/*.part
laberinto_mujoco.xml
confi_cad.ipynb

# Referencias a MuJoCo dentro del workspace
rbt_ws/src/laberintia_crtll/mujoco_env.py
rbt_ws/src/laberintia_crtll/mujoco_model/

# Submódulos o paquetes innecesarios
rbt_ws/src/velodyne/

# Carpetas compiladas que estorban
rbt_ws/build/
rbt_ws/install/
rbt_ws/log/
__pycache__/
```

---

### Fase 2: Corrección del Modelo URDF/Xacro

#### [MODIFY] [base.xacro](file:///d:/USC/Proyectos/LaberintIA/LaberintIA_FrameWork/rbt_ws/src/laberintia_crtll/xacro/laberintia/base.xacro)

Se integrarán las meshes reales STL en lugar de la caja genérica.

#### [MODIFY] [wheel.xacro](file:///d:/USC/Proyectos/LaberintIA/LaberintIA_FrameWork/rbt_ws/src/laberintia_crtll/xacro/laberintia/wheel.xacro)

Corrección de la ruta `tu_paquete` a `laberintia_crtll`.

#### [MODIFY] [robot.xacro](file:///d:/USC/Proyectos/LaberintIA/LaberintIA_FrameWork/rbt_ws/src/laberintia_crtll/xacro/laberintia/robot.xacro)

- Eliminar joint `fixed` hacia el world.
- Añadir el plugin Gazebo `diff_drive` para habilitar el tópico `/cmd_vel` y `/odom`.

#### [MODIFY] [sensors.xacro](file:///d:/USC/Proyectos/LaberintIA/LaberintIA_FrameWork/rbt_ws/src/laberintia_crtll/xacro/laberintia/sensors.xacro)

Reemplazar las esferas visuales por plugins `<sensor type="ray">` configurados con las propiedades del HC-SR04:
- Resolución angular baja.
- Rango min: 0.02m, max: 4.0m.
- Actualización: 10 Hz.

---

### Fase 3: Build System y Launch

#### [MODIFY] [setup.py](file:///d:/USC/Proyectos/LaberintIA/LaberintIA_FrameWork/rbt_ws/src/laberintia_crtll/setup.py)

Arreglar el empaquetado para que copie recursivamente todos los STL de la subcarpeta de meshes y detecte los mundos correctamente.

#### [MODIFY] [laberintia.gazebo.launch.py](file:///d:/USC/Proyectos/LaberintIA/LaberintIA_FrameWork/rbt_ws/src/laberintia_crtll/launch/laberintia.gazebo.launch.py)

Ajustar para cargar adecuadamente el entorno y exponer los tópicos del robot usando `ros_gz_bridge` (si se usa Gazebo Ignition/Harmonic) o configurando correctamente `gazebo_ros`.

---

### Fase 4: Migración del Entrenamiento a ROS 2 (Python)

#### [MODIFY] [environment.py](file:///d:/USC/Proyectos/LaberintIA/LaberintIA_FrameWork/lbrintia/environment.py)

- Migración a `rclpy`.
- Envolver `GazeboEnv` en un `rclpy.node.Node` o manejar la inicialización del nodo independientemente.
- Actualizar subscripciones: De `PointCloud2` a `sensor_msgs/msg/Range` o `LaserScan` de acuerdo al sensor de distancia HC-SR04 configurado.
- Reemplazar servicios antiguos de `gazebo_msgs` y usar `ros2 launch` nativo a través del sistema de subprocesos.
- Ajustar lógica de penalización y recompensas para el array simplificado de distancias.

#### [MODIFY] [train.py](file:///d:/USC/Proyectos/LaberintIA/LaberintIA_FrameWork/lbrintia/train.py)

- Ajustar el tamaño del estado de entrada de la red (Critic y Actor) considerando que ahora tenemos lecturas directas del HC-SR04 (ej. 3 sensores de distancia) + la odometría (distancia a meta, ángulo), reduciendo significativamente la dimensionalidad y acelerando el entrenamiento.

#### [MODIFY] [robot_scenario.launch](file:///d:/USC/Proyectos/LaberintIA/LaberintIA_FrameWork/lbrintia/assets/robot_scenario.launch)

Eliminar este archivo de ROS 1 y usar un nuevo script de launch en ROS 2 o simplemente invocar el launch file configurado en el paquete `laberintia_crtll`.

---

## Verification Plan

### Automated Tests
```bash
# 1. Limpieza y Build
cd d:\USC\Proyectos\LaberintIA\LaberintIA_FrameWork\rbt_ws
colcon build --symlink-install

# 2. Validación de modelo
source install/setup.bat
ros2 run xacro xacro $(ros2 pkg prefix laberintia_crtll)/share/laberintia_crtll/xacro/laberintia/robot.xacro > debug_robot.urdf

# 3. Lanzar la simulación base en Gazebo
ros2 launch laberintia_crtll laberintia.gazebo.launch.py
```

### Manual Verification
1. Observar en Gazebo que el robot se renderice con su forma real (piezas STL), no como una caja.
2. Enviar comandos de movimiento (`ros2 topic pub /cmd_vel`) y comprobar su tracción diferencial.
3. Verificar lecturas de los sensores de ultrasonido usando `ros2 topic echo`.
4. Ejecutar el código de entrenamiento `python train.py` y constatar que el flujo de episodios RL, reseteo del entorno, y captura de estado no produce errores de ROS 2.
