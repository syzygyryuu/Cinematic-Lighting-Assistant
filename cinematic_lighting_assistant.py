bl_info = {
    "name": "Cinematic Lighting Assistant",
    "blender": (3, 0, 0),
    "category": "Lighting",
    "author": "Syzygyryuu",
    "description": "Advanced cinematic lighting setups with customizable parameters and a dropdown menu.",
    "version": (9, 0, 0),
}

import bpy
import math


# --- Helper Functions ---
def clear_lights(scene):
    """Remove all lights in the scene."""
    for obj in scene.objects:
        if obj.type == 'LIGHT':
            bpy.data.objects.remove(obj)


def create_light(scene, name, light_type, energy, color, location, size=None, spot_size=None):
    """Helper function to create a light with customizable parameters."""
    light_data = bpy.data.lights.new(name=name, type=light_type)
    light_data.energy = energy
    light_data.color = color
    if size:
        light_data.size = size
    if spot_size and light_type == 'SPOT':
        light_data.spot_size = math.radians(spot_size)

    light_obj = bpy.data.objects.new(name=name, object_data=light_data)
    scene.collection.objects.link(light_obj)
    light_obj.location = location

    return light_obj


# --- Lighting Techniques ---
def create_three_point_lighting(scene, energy, color, spot_size):
    clear_lights(scene)

    # Key Light
    create_light(scene, "KeyLight", 'SPOT', energy, color, (3, 3, 5), spot_size=spot_size)

    # Fill Light
    create_light(scene, "FillLight", 'AREA', energy * 0.5, color, (-3, 3, 3))

    # Back Light
    create_light(scene, "BackLight", 'SPOT', energy * 0.8, color, (0, -3, 5), spot_size=spot_size)

    return "Three-Point Lighting Applied!"


def create_rembrandt_lighting(scene, energy, color, spot_size):
    clear_lights(scene)

    # Key Light
    create_light(scene, "RembrandtKey", 'SPOT', energy, color, (2, 2, 5), spot_size=spot_size)

    # Fill Light
    create_light(scene, "RembrandtFill", 'POINT', energy * 0.3, color, (-1, 2, 2))

    return "Rembrandt Lighting Applied!"


def create_chiaroscuro_lighting(scene, energy, color, spot_size):
    clear_lights(scene)

    # Key Light
    create_light(scene, "ChiaroscuroKey", 'SPOT', energy, color, (2, 2, 5), spot_size=spot_size)

    # Fill Light (low-intensity)
    create_light(scene, "ChiaroscuroFill", 'AREA', energy * 0.2, color, (-2, 2, 3))

    return "Chiaroscuro Lighting Applied!"


def create_motivated_lighting(scene, energy, color):
    clear_lights(scene)

    # Key Light (motivated by practical)
    create_light(scene, "MotivatedKey", 'POINT', energy, color, (2, 1, 2))

    # Practical Light
    create_light(scene, "PracticalLight", 'POINT', energy * 0.5, color, (2, 1, 0))

    return "Motivated Lighting Applied!"


def create_practical_lighting(scene, energy, color):
    clear_lights(scene)

    # Practical Lights
    create_light(scene, "Practical1", 'POINT', energy * 0.5, color, (1, 1, 1))
    create_light(scene, "Practical2", 'POINT', energy * 0.5, color, (-1, 1, 1))

    return "Practical Lighting Applied!"


def create_studio_lighting(scene, energy, color):
    clear_lights(scene)

    # Top Light
    create_light(scene, "StudioTop", 'AREA', energy, color, (0, 0, 5), size=5)

    # Side Lights
    create_light(scene, "StudioLeft", 'AREA', energy * 0.8, color, (-5, 0, 2), size=5)
    create_light(scene, "StudioRight", 'AREA', energy * 0.8, color, (5, 0, 2), size=5)

    return "Studio Lighting Applied!"


def create_ambient_lighting(scene, energy, color):
    clear_lights(scene)

    # Ambient Light (large area light)
    create_light(scene, "AmbientLight", 'AREA', energy, color, (0, 0, 10), size=10)

    return "Ambient Lighting Applied!"


def create_diffused_lighting(scene, energy, color):
    clear_lights(scene)

    # Diffused Lights from multiple directions
    create_light(scene, "DiffuseTop", 'AREA', energy * 0.7, color, (0, 0, 5), size=5)
    create_light(scene, "DiffuseFront", 'AREA', energy * 0.5, color, (0, -5, 3), size=5)
    create_light(scene, "DiffuseSide", 'AREA', energy * 0.5, color, (-5, 0, 3), size=5)

    return "Diffused Lighting Applied!"


# --- Property Group for Customization ---
class LightingAssistantProperties(bpy.types.PropertyGroup):
    """Properties for customizable lighting."""
    lighting_type: bpy.props.EnumProperty(
        name="Lighting Type",
        description="Select a cinematic lighting technique",
        items=[
            ("THREE_POINT", "Three-Point", "Key, Fill, and Back lights for cinematic lighting"),
            ("REMBRANDT", "Rembrandt", "Cinematic portrait lighting with shadows and highlights"),
            ("CHIAROSCURO", "Chiaroscuro", "High contrast lighting with strong shadows"),
            ("MOTIVATED", "Motivated", "Lighting inspired by practical light sources"),
            ("PRACTICAL", "Practical", "Practical light sources"),
            ("STUDIO", "Studio", "Professional studio lighting setup"),
            ("AMBIENT", "Ambient", "Soft, even ambient lighting"),
            ("DIFFUSED", "Diffused", "Gentle, scattered lighting for soft effects"),
        ],
        default="THREE_POINT"
    )
    energy: bpy.props.FloatProperty(
        name="Intensity",
        description="Light intensity (energy)",
        default=1000.0,
        min=0.0,
        max=5000.0
    )
    color: bpy.props.FloatVectorProperty(
        name="Color",
        description="Light color",
        subtype='COLOR',
        min=0.0,
        max=1.0,
        default=(1.0, 1.0, 1.0)
    )
    spot_size: bpy.props.FloatProperty(
        name="Spot Size",
        description="Spotlight size (degrees)",
        default=45.0,
        min=1.0,
        max=90.0
    )


# --- Operator Classes ---
class ApplyFilmLightingOperator(bpy.types.Operator):
    """Apply Selected Film Lighting Technique"""
    bl_idname = "lighting.apply_film_lighting"
    bl_label = "Apply Film Lighting"

    def execute(self, context):
        props = context.scene.lighting_assistant
        energy = props.energy
        color = props.color
        spot_size = props.spot_size

        if props.lighting_type == "THREE_POINT":
            message = create_three_point_lighting(context.scene, energy, color, spot_size)
        elif props.lighting_type == "REMBRANDT":
            message = create_rembrandt_lighting(context.scene, energy, color, spot_size)
        elif props.lighting_type == "CHIAROSCURO":
            message = create_chiaroscuro_lighting(context.scene, energy, color, spot_size)
        elif props.lighting_type == "MOTIVATED":
            message = create_motivated_lighting(context.scene, energy, color)
        elif props.lighting_type == "PRACTICAL":
            message = create_practical_lighting(context.scene, energy, color)
        elif props.lighting_type == "STUDIO":
            message = create_studio_lighting(context.scene, energy, color)
        elif props.lighting_type == "AMBIENT":
            message = create_ambient_lighting(context.scene, energy, color)
        elif props.lighting_type == "DIFFUSED":
            message = create_diffused_lighting(context.scene, energy, color)
        else:
            message = "Invalid Lighting Type!"
        self.report({'INFO'}, message)
        return {'FINISHED'}


# --- Panel ---
class LightingAssistantPanel(bpy.types.Panel):
    """Main Panel for Cinematic Lighting Assistant"""
    bl_label = "Cinematic Lighting Assistant"
    bl_idname = "SCENE_PT_cinematic_lighting"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        props = context.scene.lighting_assistant

        layout.label(text="Customizable Parameters:")
        layout.prop(props, "lighting_type")
        layout.prop(props, "energy", slider=True)
        layout.prop(props, "color")
        layout.prop(props, "spot_size", slider=True)

        layout.separator()
        layout.operator("lighting.apply_film_lighting", text="Apply Lighting")


# --- Registration ---
classes = [
    LightingAssistantProperties,
    ApplyFilmLightingOperator,
    LightingAssistantPanel,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.lighting_assistant = bpy.props.PointerProperty(type=LightingAssistantProperties)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.lighting_assistant


if __name__ == "__main__":
    register()