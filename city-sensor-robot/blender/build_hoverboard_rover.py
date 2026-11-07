"""Hoverboard city rover (version C): build the model and render it.

Run headless:
    /Applications/Blender.app/Contents/MacOS/Blender -b -P build_hoverboard_rover.py

Writes rover.blend, renders/rover_hero.png, renders/rover_plain.png and
renders/label_anchors.json (2D pixel positions of each part, read by label_render.py).

Dimensions in metres, +X is the front. Concept model: proportions follow the parts list in
notes/2026-11-06-hoverboard-rover.md, details are simplified.
"""

import json
import math
import os

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
RENDERS = os.path.join(HERE, "..", "renders")
os.makedirs(RENDERS, exist_ok=True)

WHEEL_R, WHEEL_W = 0.108, 0.07          # 8.5" hoverboard hub motor
FRAME_X, FRAME_Y, FRAME_Z = 0.30, 0.20, 0.13
SHELL_TOP = 0.36
MAST_X, MAST_TOP = -0.10, 1.15
HEAD_Z = 0.80

ANCHORS = {}   # label -> world point


def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def material(name, color, roughness=0.5, metallic=0.0, emission=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    if emission:
        bsdf.inputs["Emission Color"].default_value = (*color, 1)
        bsdf.inputs["Emission Strength"].default_value = emission
    return mat


def finish(obj, name, mat, bevel=0.0, smooth=False):
    obj.name = name
    obj.data.materials.append(mat)
    if bevel:
        mod = obj.modifiers.new("bevel", "BEVEL")
        mod.width, mod.segments = bevel, 3
        mod.limit_method = "ANGLE"
    if smooth:
        bpy.ops.object.shade_smooth()
    return obj


def box(name, center, size, mat, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=center)
    o = bpy.context.active_object
    o.scale = size
    bpy.ops.object.transform_apply(scale=True)
    return finish(o, name, mat, bevel)


def cyl(name, center, radius, depth, mat, axis="Z", verts=48, bevel=0.0):
    rot = {"Z": (0, 0, 0), "Y": (math.radians(90), 0, 0), "X": (0, math.radians(90), 0)}[axis]
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, location=center,
                                        rotation=rot, vertices=verts)
    return finish(bpy.context.active_object, name, mat, bevel, smooth=True)


def sphere(name, center, radius, mat, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=center, segments=32,
                                         ring_count=16)
    o = bpy.context.active_object
    o.scale = scale
    return finish(o, name, mat, smooth=True)


def rod(name, a, b, radius, mat):
    a, b = Vector(a), Vector(b)
    d = b - a
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=d.length, vertices=24,
                                        location=(a + b) / 2)
    o = bpy.context.active_object
    o.rotation_mode = "QUATERNION"
    o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d.normalized())
    return finish(o, name, mat, smooth=True)


def tire(name, y, mats):
    """Hub-motor wheel: rubber torus-ish tire around an aluminium hub."""
    cyl(name + "_tire", (0.15, y, WHEEL_R), WHEEL_R, WHEEL_W, mats["rubber"], axis="Y",
        verts=64, bevel=0.025)
    side = 1 if y > 0 else -1
    cyl(name + "_hub", (0.15, y + side * 0.004, WHEEL_R), WHEEL_R * 0.62, WHEEL_W,
        mats["alu"], axis="Y", bevel=0.004)


def build(mats):
    # Drive: two hoverboard hub motors at the front, swivel caster at the rear
    for s in (1, -1):
        tire("wheel_L" if s > 0 else "wheel_R", s * (FRAME_Y + 0.055), mats)
    ANCHORS["Hoverboard hub motor, 350 W (x2)"] = (0.15, -(FRAME_Y + 0.09), WHEEL_R + 0.04)
    cyl("caster_wheel", (-0.25, 0, 0.045), 0.045, 0.03, mats["rubber"], axis="Y", bevel=0.01)
    box("caster_fork", (-0.25, 0, 0.095), (0.05, 0.05, 0.07), mats["steel"], bevel=0.004)
    ANCHORS["Swivel caster (rear, hidden)"] = (-0.25, -0.03, 0.05)

    # Frame: 2020 extrusion rectangle with three cross bars, deck plate on top
    for y in (FRAME_Y - 0.01, -(FRAME_Y - 0.01)):
        box("rail", (0, y, FRAME_Z), (2 * FRAME_X, 0.02, 0.02), mats["alu"], bevel=0.002)
    for x in (-FRAME_X + 0.01, 0.0, FRAME_X - 0.01):
        box("cross", (x, 0, FRAME_Z), (0.02, 2 * FRAME_Y, 0.02), mats["alu"], bevel=0.002)
    box("deck", (0, 0, FRAME_Z + 0.013), (2 * FRAME_X + 0.02, 2 * FRAME_Y + 0.02, 0.006),
        mats["alu"])
    ANCHORS["2020 aluminium frame"] = (FRAME_X - 0.05, -FRAME_Y, FRAME_Z)

    # Printed shell over the deck: batteries, Pi, power boxes live inside
    shell_z0 = FRAME_Z + 0.016
    box("shell", (0, 0, (shell_z0 + SHELL_TOP) / 2),
        (2 * FRAME_X + 0.02, 2 * FRAME_Y + 0.02, SHELL_TOP - shell_z0), mats["shell"],
        bevel=0.035)
    box("stripe", (0, 0, shell_z0 + 0.05),
        (2 * FRAME_X + 0.026, 2 * FRAME_Y + 0.026, 0.03), mats["orange"], bevel=0.01)
    ANCHORS["Printed shell (batteries, Pi 5 inside)"] = (-0.05, -FRAME_Y - 0.01, 0.30)

    # Lights front and rear
    for y in (0.13, -0.13):
        box("headlight", (FRAME_X + 0.012, y, 0.30), (0.006, 0.07, 0.025), mats["light"])
        box("taillight", (-FRAME_X - 0.012, y, 0.30), (0.006, 0.07, 0.025), mats["red_light"])
    ANCHORS["LED headlights"] = (FRAME_X + 0.012, -0.13, 0.30)

    # Ground-temperature IR thermometer under the nose
    cyl("mlx90614", (FRAME_X - 0.02, 0, shell_z0 - 0.01), 0.009, 0.02, mats["dark"])
    ANCHORS["Ground IR thermometer (MLX90614)"] = (FRAME_X - 0.02, 0, shell_z0 - 0.02)

    # Rain sensor plate on the nose, tilted
    box("rain_sensor", (FRAME_X - 0.06, 0.10, SHELL_TOP + 0.004), (0.06, 0.04, 0.003),
        mats["pcb"])
    ANCHORS["Rain sensor"] = (FRAME_X - 0.06, 0.10, SHELL_TOP + 0.005)

    # Top deck: e-stop, GNSS antenna, SDR whip
    cyl("estop_base", (-0.22, -0.13, SHELL_TOP + 0.02), 0.03, 0.04, mats["yellow"])
    cyl("estop_button", (-0.22, -0.13, SHELL_TOP + 0.05), 0.028, 0.02, mats["red"], bevel=0.008)
    ANCHORS["E-stop"] = (-0.22, -0.13, SHELL_TOP + 0.06)
    cyl("gnss_antenna", (-0.22, 0.13, SHELL_TOP + 0.008), 0.035, 0.016, mats["dark"], bevel=0.006)
    ANCHORS["GNSS antenna (behind mast)"] = (-0.22, 0.13, SHELL_TOP + 0.016)
    rod("sdr_whip", (-0.27, 0.05, SHELL_TOP), (-0.27, 0.05, SHELL_TOP + 0.32), 0.003, mats["dark"])
    ANCHORS["RTL-SDR antenna"] = (-0.27, 0.05, SHELL_TOP + 0.30)

    # Mast
    rod("mast", (MAST_X, 0, SHELL_TOP), (MAST_X, 0, MAST_TOP), 0.0125, mats["alu"])
    cyl("mast_clamp", (MAST_X, 0, SHELL_TOP + 0.015), 0.03, 0.03, mats["dark"])

    # Sensor head, facing forward
    hx = MAST_X + 0.07
    box("head", (hx, 0, HEAD_Z), (0.16, 0.22, 0.11), mats["shell"], bevel=0.015)
    face = hx + 0.08
    # OAK-D Lite bar with three lenses
    box("oakd", (face + 0.008, 0, HEAD_Z + 0.03), (0.017, 0.091, 0.028), mats["dark"], bevel=0.004)
    for y in (-0.037, 0.0, 0.037):
        cyl("oakd_lens", (face + 0.017, y, HEAD_Z + 0.03), 0.006, 0.004, mats["glass"], axis="X")
    ANCHORS["3D depth camera (OAK-D Lite)"] = (face + 0.02, 0.0, HEAD_Z + 0.03)
    # Thermal camera
    box("thermal", (face + 0.008, -0.055, HEAD_Z - 0.02), (0.016, 0.04, 0.04), mats["dark"], bevel=0.004)
    cyl("thermal_lens", (face + 0.017, -0.055, HEAD_Z - 0.02), 0.011, 0.005, mats["germanium"], axis="X")
    ANCHORS["Thermal camera"] = (face + 0.02, -0.055, HEAD_Z - 0.02)
    # NoIR night camera + IR illuminator ring
    box("noir", (face + 0.008, 0.035, HEAD_Z - 0.02), (0.016, 0.03, 0.03), mats["pcb"])
    cyl("noir_lens", (face + 0.017, 0.035, HEAD_Z - 0.02), 0.006, 0.006, mats["glass"], axis="X")
    cyl("ir_ring", (face + 0.008, 0.08, HEAD_Z - 0.02), 0.016, 0.012, mats["ir"], axis="X")
    ANCHORS["Night camera + IR light"] = (face + 0.02, 0.06, HEAD_Z - 0.02)

    # Head top: 4-mic array, UV and lux sensors
    cyl("mic_array", (hx - 0.01, 0, HEAD_Z + 0.062), 0.05, 0.012, mats["dark"], bevel=0.003)
    for i in range(4):
        a = i * math.pi / 2 + math.pi / 4
        cyl("mic", (hx - 0.01 + 0.035 * math.cos(a), 0.035 * math.sin(a), HEAD_Z + 0.069),
            0.004, 0.003, mats["alu"])
    ANCHORS["4-mic array (ReSpeaker XVF3800)"] = (hx - 0.01, -0.04, HEAD_Z + 0.07)
    sphere("uv_dome", (hx + 0.05, -0.08, HEAD_Z + 0.058), 0.012, mats["frost"], (1, 1, 0.7))
    ANCHORS["UV index sensor (LTR390)"] = (hx + 0.05, -0.08, HEAD_Z + 0.066)
    sphere("lux_dome", (hx + 0.05, 0.08, HEAD_Z + 0.058), 0.012, mats["frost"], (1, 1, 0.7))
    ANCHORS["Light sensor (TSL2591)"] = (hx + 0.05, 0.08, HEAD_Z + 0.066)

    # Lidar on top of the mast
    cyl("lidar_base", (MAST_X, 0, MAST_TOP + 0.02), 0.04, 0.04, mats["dark"], bevel=0.005)
    sphere("lidar_dome", (MAST_X, 0, MAST_TOP + 0.04), 0.038, mats["glass_dark"], (1, 1, 0.75))
    ANCHORS["Lidar (Unitree L2)"] = (MAST_X, -0.03, MAST_TOP + 0.05)

    # Air-quality radiation shield on an arm (+Y): SEN55, SCD41, Wi-Fi ESP32 inside
    arm_z = 0.98
    rod("shield_arm", (MAST_X, 0, arm_z), (MAST_X, 0.17, arm_z), 0.007, mats["alu"])
    for i in range(6):
        cyl("shield_plate", (MAST_X, 0.17, arm_z - 0.012 - i * 0.016), 0.05 - i * 0.002,
            0.006, mats["shell"], bevel=0.002)
    ANCHORS["Air shield: SEN55 + SCD41 CO2"] = (MAST_X, 0.21, arm_z - 0.05)

    # Anemometer on an arm (-Y)
    an_z = 1.05
    rod("anemo_arm", (MAST_X, 0, an_z), (MAST_X, -0.17, an_z), 0.007, mats["alu"])
    rod("anemo_spindle", (MAST_X, -0.17, an_z), (MAST_X, -0.17, an_z + 0.06), 0.005, mats["alu"])
    for i in range(3):
        a = i * math.tau / 3
        tip = (MAST_X + 0.06 * math.cos(a), -0.17 + 0.06 * math.sin(a), an_z + 0.06)
        rod("anemo_spoke", (MAST_X, -0.17, an_z + 0.06), tip, 0.0025, mats["alu"])
        sphere("anemo_cup", tip, 0.018, mats["shell"], (1, 1, 0.9))
    ANCHORS["Wind: cup anemometer"] = (MAST_X, -0.23, an_z + 0.06)

    # ESP32 Wi-Fi scanner box on the mast
    box("esp32_box", (MAST_X - 0.025, 0, 0.55), (0.03, 0.06, 0.08), mats["dark"], bevel=0.004)
    ANCHORS["Wi-Fi / Bluetooth scanner (ESP32-S3)"] = (MAST_X - 0.04, -0.03, 0.55)

    # Safety flag
    rod("flag_pole", (-FRAME_X + 0.03, 0.17, SHELL_TOP), (-FRAME_X + 0.03, 0.17, 1.45), 0.004,
        mats["dark"])
    bpy.ops.mesh.primitive_plane_add(size=1)
    flag = bpy.context.active_object
    me = flag.data
    me.vertices[0].co = (0, 0, 0)
    me.vertices[1].co = (0, 0, 0)
    me.vertices[2].co = (0, -0.0, -0.12)
    me.vertices[3].co = (-0.16, 0, -0.06)
    flag.location = (-FRAME_X + 0.03, 0.17, 1.45)
    finish(flag, "flag", mats["orange"])
    ANCHORS["Safety flag"] = (-FRAME_X - 0.05, 0.17, 1.40)


def stage():
    scene = bpy.context.scene
    mats = {
        "rubber": material("Rubber", (0.025, 0.025, 0.025), 0.85),
        "alu": material("Aluminium", (0.72, 0.73, 0.75), 0.32, metallic=1.0),
        "steel": material("Steel", (0.35, 0.35, 0.36), 0.4, metallic=1.0),
        "shell": material("PETG shell", (0.62, 0.63, 0.62), 0.45),
        "orange": material("Safety orange", (0.95, 0.30, 0.03), 0.5),
        "dark": material("Black plastic", (0.03, 0.03, 0.035), 0.4),
        "pcb": material("PCB", (0.02, 0.18, 0.08), 0.5),
        "glass": material("Lens", (0.01, 0.01, 0.02), 0.05),
        "glass_dark": material("Lidar window", (0.02, 0.02, 0.03), 0.08, metallic=0.3),
        "germanium": material("Germanium", (0.15, 0.16, 0.18), 0.15, metallic=0.8),
        "frost": material("Frosted dome", (0.92, 0.92, 0.94), 0.35),
        "ir": material("IR LEDs", (0.25, 0.05, 0.05), 0.3),
        "yellow": material("E-stop base", (0.95, 0.75, 0.05), 0.5),
        "red": material("E-stop", (0.75, 0.03, 0.03), 0.35),
        "light": material("Headlight", (1.0, 0.97, 0.9), 0.2, emission=6),
        "red_light": material("Taillight", (1.0, 0.05, 0.03), 0.2, emission=4),
        "ground": material("Sidewalk", (0.30, 0.30, 0.29), 0.8),
    }
    build(mats)

    bpy.ops.mesh.primitive_plane_add(size=12, location=(0, 0, 0))
    bpy.context.active_object.data.materials.append(mats["ground"])

    bpy.ops.object.light_add(type="AREA", location=(1.8, -1.6, 2.2))
    key = bpy.context.active_object
    key.data.energy, key.data.size = 320, 2.0
    key.rotation_euler = (Vector((0, 0, 0.6)) - key.location).to_track_quat("-Z", "Y").to_euler()
    bpy.ops.object.light_add(type="SUN", location=(0, 0, 5))
    sun = bpy.context.active_object
    sun.data.energy, sun.data.angle = 1.6, math.radians(6)
    sun.rotation_euler = (math.radians(50), math.radians(15), math.radians(-30))

    world = bpy.data.worlds.new("World")
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.75, 0.78, 0.82, 1)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.3
    scene.world = world

    bpy.ops.object.camera_add(location=(2.15, -2.05, 1.15))
    cam = bpy.context.active_object
    cam.data.lens = 50
    target = Vector((0.0, 0.0, 0.66))
    cam.rotation_euler = (target - cam.location).to_track_quat("-Z", "Y").to_euler()
    scene.camera = cam


def render(path, samples=96):
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    prefs = bpy.context.preferences.addons["cycles"].preferences
    try:
        prefs.compute_device_type = "METAL"
        prefs.get_devices()
        for d in prefs.devices:
            d.use = True
        scene.cycles.device = "GPU"
    except Exception:
        scene.cycles.device = "CPU"
    scene.cycles.samples = samples
    scene.cycles.use_denoising = True
    scene.render.resolution_x, scene.render.resolution_y = 1600, 1200
    scene.view_settings.view_transform = "AgX"
    scene.render.filepath = path
    bpy.ops.render.render(write_still=True)


def write_anchors(path):
    scene = bpy.context.scene
    w, h = scene.render.resolution_x, scene.render.resolution_y
    out = {}
    for label, p in ANCHORS.items():
        co = world_to_camera_view(scene, scene.camera, Vector(p))
        out[label] = [round(co.x * w), round((1 - co.y) * h)]
    with open(path, "w") as f:
        json.dump({"size": [w, h], "anchors": out}, f, indent=1)


if __name__ == "__main__":
    reset_scene()
    stage()
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, "rover.blend"))
    scene = bpy.context.scene
    scene.render.resolution_x, scene.render.resolution_y = 1600, 1200
    write_anchors(os.path.join(RENDERS, "label_anchors.json"))
    render(os.path.join(RENDERS, "rover_plain.png"))
