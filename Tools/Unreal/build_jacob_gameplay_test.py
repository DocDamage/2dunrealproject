import unreal
import os
from pathlib import Path


LEVEL_PATH = "/Game/NocturneSignal/Slice01/Maps/L_Slice01GameplayTest"
PLAYER_CLASS_PATH = "/Script/NocturneSignal.NocturnePlayerCharacter"
ANCHOR_CLASS_PATH = "/Script/NocturneSignal.GrappleAnchor"
PARALLAX_LAYER_CLASS_PATH = "/Script/NocturneSignal.NocturneParallaxLayer"
CUBE_PATH = "/Engine/BasicShapes/Cube.Cube"
PLANE_PATH = "/Engine/BasicShapes/Plane.Plane"
SPHERE_PATH = "/Engine/BasicShapes/Sphere.Sphere"
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SAKURA_SOURCE_ROOT = Path(
    os.environ.get(
        "NOCTURNE_SAKURA_TEMPLE_SOURCE",
        r"G:\Nocturne Signal\asset_intake\extracted\Sakura Temple Asset Pack",
    )
)
SAKURA_CROP_SOURCE_ROOT = PROJECT_ROOT / "SourceArt" / "SakuraTempleCrops"
SAKURA_PARALLAX_SOURCE_ROOT = PROJECT_ROOT / "SourceArt" / "SakuraParallax"
SAKURA_ASSET_ROOT = "/Game/NocturneSignal/Environments/SakuraTemple"
SAKURA_CROP_TEXTURE_ROOT = SAKURA_ASSET_ROOT + "/CropTextures"
SAKURA_PARALLAX_TEXTURE_ROOT = SAKURA_ASSET_ROOT + "/ParallaxTextures"
SAKURA_MATERIAL_ROOT = SAKURA_ASSET_ROOT + "/Materials"
SAKURA_MASTER_MATERIAL_PATH = SAKURA_MATERIAL_ROOT + "/M_SakuraPlaneRGBA"
SAKURA_SHEET_SIZE = (1536, 1024)
PLAY_PLANE_Y = 0.0
ART_PLANE_Y = 35.0
TEXT_PLANE_Y = -80.0
PARALLAX_TILE_OFFSETS = (0,)
SHOW_DEBUG_LABELS = False
SHOW_ANCHOR_MARKERS = False
_SAKURA_MASTER_MATERIAL = None

SPRITE_MATERIAL_CANDIDATES = (
    "/Paper2D/MaskedUnlitSpriteMaterial.MaskedUnlitSpriteMaterial",
    "/Paper2D/TranslucentUnlitSpriteMaterial.TranslucentUnlitSpriteMaterial",
    "/Paper2D/DefaultSpriteMaterial.DefaultSpriteMaterial",
)
SAKURA_MASTER_MATERIAL_CANDIDATES = (
    SAKURA_MASTER_MATERIAL_PATH + ".M_SakuraPlaneRGBA",
    "/Paper2D/MaskedUnlitSpriteMaterial.MaskedUnlitSpriteMaterial",
    "/Paper2D/TranslucentUnlitSpriteMaterial.TranslucentUnlitSpriteMaterial",
    "/Paper2D/DefaultSpriteMaterial.DefaultSpriteMaterial",
)

SAKURA_TEXTURES = {
    "FloorTiles": SAKURA_SOURCE_ROOT / "Floor tiles" / "Floor tiles.png",
    "ShrineGates": SAKURA_SOURCE_ROOT / "Shrine Gates" / "Shrine Gates.png",
    "SakuraTrees": SAKURA_SOURCE_ROOT / "Sakura trees" / "Sakura trees.png",
    "TempleParts": SAKURA_SOURCE_ROOT / "temple building parts" / "temple building parts.png",
    "PlantsBushes": SAKURA_SOURCE_ROOT / "Plants and bushes" / "Plants and bushes.png",
    "LanternsLights": SAKURA_SOURCE_ROOT / "Lanterns and lights" / "Lanterns and lights.png",
}

COLLISION_SCALE_FLOOR_MAIN = unreal.Vector(38.0, 0.6, 0.35)
COLLISION_SCALE_PLATFORM_LOW = unreal.Vector(3.2, 0.6, 0.3)
COLLISION_SCALE_PLATFORM_HIGH = unreal.Vector(2.8, 0.6, 0.3)
COLLISION_SCALE_SLIDE_CEILING = unreal.Vector(3.0, 0.6, 0.22)
COLLISION_SCALE_SLIDE_MARKER = unreal.Vector(3.0, 0.6, 0.08)
COLLISION_SCALE_PLAYABLE_BOUND = unreal.Vector(0.3, 0.6, 4.8)
BASIC_CUBE_HALF_EXTENT = 50.0
MAIN_FLOOR_LOCATION_Z = -50.0
DEFAULT_CHARACTER_CAPSULE_HALF_HEIGHT = 88.0
PLAYER_GROUND_CLEARANCE = 2.0
PLAYABLE_BOUNDS_MIN_X = -1500.0
PLAYABLE_BOUNDS_MAX_X = 1500.0
PLAYER_START_Z = (
    MAIN_FLOOR_LOCATION_Z
    + BASIC_CUBE_HALF_EXTENT * COLLISION_SCALE_FLOOR_MAIN.z
    + DEFAULT_CHARACTER_CAPSULE_HALF_HEIGHT
    + PLAYER_GROUND_CLEARANCE
)
VISIBLE_FLOOR_TILE_EXTENT_X = 1900.0
VISIBLE_FLOOR_TILE_SCALE = 1.0
VISIBLE_FLOOR_TILE_LAYER = -20
VISIBLE_FLOOR_TILE_PATTERN = ("SP_SakuraFloorPlain", "SP_SakuraFloorBlossom", "SP_SakuraFloorBorder")

SAKURA_SPRITES = {
    "SP_SakuraFloorPlain": ("FloorTiles", (270, 238), (160, 156)),
    "SP_SakuraFloorBlossom": ("FloorTiles", (59, 239), (168, 156)),
    "SP_SakuraFloorBorder": ("FloorTiles", (673, 466), (162, 156)),
    "SP_SakuraTempleLarge": ("TempleParts", (53, 168), (358, 224)),
    "SP_SakuraTempleSmall": ("TempleParts", (1095, 626), (188, 124)),
    "SP_SakuraTreeLarge": ("SakuraTrees", (82, 163), (318, 355)),
    "SP_SakuraTreeSmall": ("SakuraTrees", (480, 551), (205, 257)),
    "SP_SakuraGateRed": ("ShrineGates", (170, 158), (135, 157)),
    "SP_SakuraGateGrand": ("ShrineGates", (785, 386), (148, 180)),
    "SP_SakuraLantern": ("ShrineGates", (784, 878), (54, 108)),
}

SAKURA_PARALLAX_LAYERS = (
    {
        "name": "SkyClouds",
        "file": "SakuraParallax_SkyClouds.png",
        "source_dimension": (1876, 926),
        "location": (0.0, 330.0, -620.0),
        "scale_x": 3.0,
        "scale_z": 2.22,
        "sort_priority": -100,
    },
    {
        "name": "DistantTemples",
        "file": "SakuraParallax_DistantTemples.png",
        "source_dimension": (1876, 926),
        "location": (0.0, 240.0, -330.0),
        "scale_x": 3.0,
        "scale_z": 1.55,
        "sort_priority": -80,
    },
    {
        "name": "MidgroundGarden",
        "file": "SakuraParallax_MidgroundGarden.png",
        "source_dimension": (1876, 926),
        "location": (0.0, 185.0, -210.0),
        "scale_x": 3.0,
        "scale_z": 1.55,
        "sort_priority": -60,
    },
    {
        "name": "ForegroundRuins",
        "file": "SakuraParallax_ForegroundRuins.png",
        "source_dimension": (1876, 926),
        "location": (0.0, 165.0, -85.0),
        "scale_x": 3.0,
        "scale_z": 1.55,
        "sort_priority": -40,
    },
)


def log(message):
    unreal.log("[NocturneSlice01GameplayTest] " + str(message))


def load_asset(path):
    asset = unreal.EditorAssetLibrary.load_asset(path)
    if not asset:
        raise RuntimeError("Could not load asset: " + path)
    return asset


def load_optional_asset(path):
    try:
        return unreal.EditorAssetLibrary.load_asset(path)
    except Exception:
        return None


def side_location(x, z, y=PLAY_PLANE_Y):
    return unreal.Vector(float(x), float(y), float(z))


def get_sprite_material():
    for material_path in SPRITE_MATERIAL_CANDIDATES:
        material = load_optional_asset(material_path)
        if material:
            return material
    return None


def set_component_movable(component):
    try:
        component.set_editor_property("mobility", unreal.ComponentMobility.MOVABLE)
    except Exception:
        pass


def disable_static_lighting_for_level():
    world = unreal.EditorLevelLibrary.get_editor_world()
    if not world:
        return
    world_settings = world.get_world_settings()
    for property_name in ("force_no_precomputed_lighting", "b_force_no_precomputed_lighting"):
        try:
            world_settings.set_editor_property(property_name, True)
            return
        except Exception:
            pass


def get_level_editor_subsystem():
    subsystem_type = getattr(unreal, "LevelEditorSubsystem", None)
    return unreal.get_editor_subsystem(subsystem_type) if subsystem_type else None


def validate_sakura_source_and_sprites():
    missing_sources = [
        str(source_path)
        for source_path in SAKURA_TEXTURES.values()
        if not source_path.exists()
    ]
    if missing_sources:
        raise RuntimeError("Missing Sakura Temple source textures: " + "; ".join(missing_sources))

    sheet_width, sheet_height = SAKURA_SHEET_SIZE
    invalid_sprites = []
    for sprite_name, (texture_name, source_uv, source_dimension) in SAKURA_SPRITES.items():
        if texture_name not in SAKURA_TEXTURES:
            invalid_sprites.append(sprite_name + " references unknown texture " + texture_name)
            continue

        x, y = source_uv
        width, height = source_dimension
        if x < 0 or y < 0 or width <= 0 or height <= 0 or x + width > sheet_width or y + height > sheet_height:
            invalid_sprites.append(
                "{} crop {}+{} exceeds sheet {}x{}".format(
                    sprite_name,
                    source_uv,
                    source_dimension,
                    sheet_width,
                    sheet_height,
                )
            )

    if invalid_sprites:
        raise RuntimeError("Invalid Sakura sprite crop data: " + "; ".join(invalid_sprites))


def import_sakura_textures():
    validate_sakura_source_and_sprites()
    unreal.EditorAssetLibrary.make_directory(SAKURA_ASSET_ROOT + "/Textures")
    tasks = []
    for asset_name, source_path in SAKURA_TEXTURES.items():
        destination_asset = SAKURA_ASSET_ROOT + "/Textures/T_" + asset_name
        if unreal.EditorAssetLibrary.does_asset_exist(destination_asset):
            continue
        if not source_path.exists():
            raise RuntimeError("Missing Sakura Temple source texture: " + str(source_path))

        task = unreal.AssetImportTask()
        task.set_editor_property("filename", str(source_path))
        task.set_editor_property("destination_path", SAKURA_ASSET_ROOT + "/Textures")
        task.set_editor_property("destination_name", "T_" + asset_name)
        task.set_editor_property("automated", True)
        task.set_editor_property("save", False)
        task.set_editor_property("replace_existing", True)
        task.set_editor_property("factory", unreal.TextureFactory())
        tasks.append(task)

    if tasks:
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)

    textures = {}
    for asset_name in SAKURA_TEXTURES:
        texture = load_asset(SAKURA_ASSET_ROOT + "/Textures/T_" + asset_name)
        try:
            texture.set_editor_property("compression_settings", unreal.TextureCompressionSettings.TC_EDITOR_ICON)
            texture.set_editor_property("filter", unreal.TextureFilter.TF_NEAREST)
            texture.set_editor_property("compression_no_alpha", False)
        except Exception:
            pass
        unreal.EditorAssetLibrary.save_loaded_asset(texture)
        textures[asset_name] = texture
    return textures


def get_or_create_sakura_sprite(sprite_name, texture, source_uv, source_dimension):
    unreal.EditorAssetLibrary.make_directory(SAKURA_ASSET_ROOT + "/Sprites")
    sprite_path = SAKURA_ASSET_ROOT + "/Sprites/" + sprite_name
    sprite = unreal.EditorAssetLibrary.load_asset(sprite_path)
    if not sprite:
        sprite = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
            sprite_name,
            SAKURA_ASSET_ROOT + "/Sprites",
            unreal.PaperSprite,
            unreal.PaperSpriteFactory(),
        )
    if not sprite:
        raise RuntimeError("Could not create Sakura sprite: " + sprite_name)

    sprite.set_editor_property("source_texture", texture)
    sprite.set_editor_property("source_uv", unreal.Vector2D(float(source_uv[0]), float(source_uv[1])))
    sprite.set_editor_property(
        "source_dimension",
        unreal.Vector2D(float(source_dimension[0]), float(source_dimension[1])),
    )
    sprite.set_editor_property("pixels_per_unreal_unit", 1.0)
    sprite.set_editor_property("pivot_mode", unreal.SpritePivotMode.BOTTOM_CENTER)
    unreal.EditorAssetLibrary.save_loaded_asset(sprite)
    return sprite


def build_sakura_sprite_library():
    textures = import_sakura_textures()
    sprites = {}
    for sprite_name, (texture_name, source_uv, source_dimension) in SAKURA_SPRITES.items():
        sprites[sprite_name] = get_or_create_sakura_sprite(
            sprite_name,
            textures[texture_name],
            source_uv,
            source_dimension,
        )
    return sprites


def import_sakura_crop_textures():
    unreal.EditorAssetLibrary.make_directory(SAKURA_CROP_TEXTURE_ROOT)
    tasks = []
    for sprite_name in SAKURA_SPRITES:
        source_path = SAKURA_CROP_SOURCE_ROOT / (sprite_name + ".png")
        destination_asset = SAKURA_CROP_TEXTURE_ROOT + "/T_" + sprite_name
        if unreal.EditorAssetLibrary.does_asset_exist(destination_asset):
            continue
        if not source_path.exists():
            raise RuntimeError(
                "Missing cropped Sakura texture: {}. Regenerate SourceArt/SakuraTempleCrops before building.".format(
                    source_path
                )
            )

        task = unreal.AssetImportTask()
        task.set_editor_property("filename", str(source_path))
        task.set_editor_property("destination_path", SAKURA_CROP_TEXTURE_ROOT)
        task.set_editor_property("destination_name", "T_" + sprite_name)
        task.set_editor_property("automated", True)
        task.set_editor_property("save", False)
        task.set_editor_property("replace_existing", True)
        task.set_editor_property("factory", unreal.TextureFactory())
        tasks.append(task)

    if tasks:
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)

    textures = {}
    for sprite_name in SAKURA_SPRITES:
        texture = load_asset(SAKURA_CROP_TEXTURE_ROOT + "/T_" + sprite_name)
        try:
            texture.set_editor_property("compression_settings", unreal.TextureCompressionSettings.TC_EDITOR_ICON)
            texture.set_editor_property("filter", unreal.TextureFilter.TF_NEAREST)
            texture.set_editor_property("compression_no_alpha", False)
        except Exception:
            pass
        unreal.EditorAssetLibrary.save_loaded_asset(texture)
        textures[sprite_name] = texture
    return textures


def get_sakura_master_material():
    global _SAKURA_MASTER_MATERIAL
    if _SAKURA_MASTER_MATERIAL:
        return _SAKURA_MASTER_MATERIAL

    unreal.EditorAssetLibrary.make_directory(SAKURA_MATERIAL_ROOT)
    if not unreal.EditorAssetLibrary.does_asset_exist(SAKURA_MASTER_MATERIAL_PATH):
        material = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
            "M_SakuraPlaneRGBA",
            SAKURA_MATERIAL_ROOT,
            unreal.Material,
            unreal.MaterialFactoryNew(),
        )
        if material:
            configure_sakura_master_material(material)
    else:
        material = unreal.EditorAssetLibrary.load_asset(SAKURA_MASTER_MATERIAL_PATH)
        if material:
            configure_sakura_master_material(material)

    for material_path in SAKURA_MASTER_MATERIAL_CANDIDATES:
        material = load_optional_asset(material_path)
        if material:
            _SAKURA_MASTER_MATERIAL = material
            return material
    return None


def configure_sakura_master_material(material):
    try:
        material.set_editor_property("blend_mode", unreal.BlendMode.BLEND_MASKED)
        material.set_editor_property("shading_model", unreal.MaterialShadingModel.MSM_UNLIT)
        material.set_editor_property("two_sided", True)
        material.set_editor_property("opacity_mask_clip_value", 0.1)
    except Exception as exc:
        log("Could not configure Sakura master material properties: {}".format(exc))

    try:
        unreal.MaterialEditingLibrary.delete_all_material_expressions(material)
        texture_sample = unreal.MaterialEditingLibrary.create_material_expression(
            material,
            unreal.MaterialExpressionTextureSampleParameter2D,
            -420,
            0,
        )
        texture_sample.set_editor_property("parameter_name", "SpriteTexture")
        unreal.MaterialEditingLibrary.connect_material_property(
            texture_sample,
            "RGB",
            unreal.MaterialProperty.MP_EMISSIVE_COLOR,
        )
        unreal.MaterialEditingLibrary.connect_material_property(
            texture_sample,
            "A",
            unreal.MaterialProperty.MP_OPACITY_MASK,
        )
        unreal.MaterialEditingLibrary.layout_material_expressions(material)
        unreal.MaterialEditingLibrary.recompile_material(material)
        unreal.EditorAssetLibrary.save_loaded_asset(material)
    except Exception as exc:
        log("Could not configure Sakura master material graph: {}".format(exc))


def get_or_create_sakura_material(sprite_name, texture):
    unreal.EditorAssetLibrary.make_directory(SAKURA_MATERIAL_ROOT)
    material_path = SAKURA_MATERIAL_ROOT + "/MI_" + sprite_name
    material = (
        unreal.EditorAssetLibrary.load_asset(material_path)
        if unreal.EditorAssetLibrary.does_asset_exist(material_path)
        else None
    )
    if not material:
        material = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
            "MI_" + sprite_name,
            SAKURA_MATERIAL_ROOT,
            unreal.MaterialInstanceConstant,
            unreal.MaterialInstanceConstantFactoryNew(),
        )
    if not material:
        raise RuntimeError("Could not create Sakura material instance: " + sprite_name)

    parent = get_sakura_master_material()
    if parent:
        material.set_editor_property("parent", parent)
    try:
        unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(
            material,
            "SpriteTexture",
            texture,
        )
    except Exception as exc:
        log("Could not set SpriteTexture on {}: {}".format(sprite_name, exc))
    unreal.EditorAssetLibrary.save_loaded_asset(material)
    return material


def build_sakura_plane_library():
    textures = import_sakura_crop_textures()
    planes = {}
    for sprite_name, (_, _, source_dimension) in SAKURA_SPRITES.items():
        planes[sprite_name] = {
            "material": get_or_create_sakura_material(sprite_name, textures[sprite_name]),
            "width": float(source_dimension[0]),
            "height": float(source_dimension[1]),
        }
    return planes


def import_sakura_parallax_textures():
    unreal.EditorAssetLibrary.make_directory(SAKURA_PARALLAX_TEXTURE_ROOT)
    tasks = []
    for layer in SAKURA_PARALLAX_LAYERS:
        source_path = SAKURA_PARALLAX_SOURCE_ROOT / layer["file"]
        asset_name = "T_SakuraParallax_" + layer["name"]
        if not source_path.exists():
            raise RuntimeError("Missing Sakura parallax source texture: " + str(source_path))

        task = unreal.AssetImportTask()
        task.set_editor_property("filename", str(source_path))
        task.set_editor_property("destination_path", SAKURA_PARALLAX_TEXTURE_ROOT)
        task.set_editor_property("destination_name", asset_name)
        task.set_editor_property("automated", True)
        task.set_editor_property("save", False)
        task.set_editor_property("replace_existing", True)
        task.set_editor_property("factory", unreal.TextureFactory())
        tasks.append(task)

    if tasks:
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)

    textures = {}
    for layer in SAKURA_PARALLAX_LAYERS:
        texture = load_asset(SAKURA_PARALLAX_TEXTURE_ROOT + "/T_SakuraParallax_" + layer["name"])
        try:
            texture.set_editor_property("compression_settings", unreal.TextureCompressionSettings.TC_EDITOR_ICON)
            texture.set_editor_property("filter", unreal.TextureFilter.TF_NEAREST)
        except Exception:
            pass
        unreal.EditorAssetLibrary.save_loaded_asset(texture)
        textures[layer["name"]] = texture
    return textures


def build_sakura_parallax_library():
    textures = import_sakura_parallax_textures()
    parallax_layers = {}
    for layer in SAKURA_PARALLAX_LAYERS:
        layer_name = "SakuraParallax_" + layer["name"]
        parallax_layers[layer["name"]] = {
            "material": get_or_create_sakura_material(layer_name, textures[layer["name"]]),
            "width": float(layer["source_dimension"][0]),
            "height": float(layer["source_dimension"][1]),
            "location": side_location(*layer["location"]),
            "scale_x": float(layer.get("scale_x", layer.get("scale", 1.0))),
            "scale_z": float(layer.get("scale_z", layer.get("scale", 1.0))),
            "sort_priority": int(layer["sort_priority"]),
        }
    return parallax_layers


def load_class(path):
    cls = unreal.load_class(None, path)
    if not cls:
        raise RuntimeError("Could not load class: " + path)
    return cls


def set_label(actor, label):
    try:
        actor.set_actor_label(label)
    except Exception:
        pass


def try_set_editor_property(actor, names, value):
    for property_name in names:
        try:
            actor.set_editor_property(property_name, value)
            return True
        except Exception:
            pass
    return False


def set_autopossess_player0(actor):
    try:
        actor.set_editor_property("auto_possess_player", unreal.AutoReceiveInput.PLAYER0)
    except Exception as exc:
        log("Could not set AutoPossessPlayer on playable player: " + str(exc))


def open_or_create_level():
    unreal.EditorAssetLibrary.make_directory("/Game/NocturneSignal/Slice01/Maps")
    level_subsystem = get_level_editor_subsystem()
    if unreal.EditorAssetLibrary.does_asset_exist(LEVEL_PATH):
        if level_subsystem:
            if not level_subsystem.load_level(LEVEL_PATH):
                raise RuntimeError("Failed to load gameplay test level: " + LEVEL_PATH)
        elif not unreal.EditorLevelLibrary.load_level(LEVEL_PATH):
            raise RuntimeError("Failed to load gameplay test level: " + LEVEL_PATH)
        return

    if level_subsystem:
        if not level_subsystem.new_level(LEVEL_PATH):
            raise RuntimeError("Failed to create gameplay test level: " + LEVEL_PATH)
    elif not unreal.EditorLevelLibrary.new_level(LEVEL_PATH):
        raise RuntimeError("Failed to create gameplay test level: " + LEVEL_PATH)


def clear_test_actors():
    actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    for actor in actor_subsystem.get_all_level_actors():
        try:
            label = actor.get_actor_label()
        except Exception:
            label = actor.get_name()
        if label.startswith("Slice01_") or label.startswith("TXT_Slice01_"):
            actor_subsystem.destroy_actor(actor)


def spawn_text(label, location, size=28.0):
    if not SHOW_DEBUG_LABELS:
        return None

    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.TextRenderActor,
        location,
        unreal.Rotator(0.0, 180.0, 0.0),
    )
    set_label(actor, "TXT_Slice01_" + label.replace(" ", "_"))
    component = actor.get_component_by_class(unreal.TextRenderComponent)
    if component:
        set_component_movable(component)
        component.set_editor_property("text", label)
        component.set_editor_property("horizontal_alignment", unreal.HorizTextAligment.EHTA_CENTER)
        component.set_editor_property("world_size", size)
    return actor


def spawn_static_mesh(label, mesh, location, scale, material_color=None):
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.StaticMeshActor,
        location,
        unreal.Rotator(0.0, 0.0, 0.0),
    )
    set_label(actor, "Slice01_" + label.replace(" ", "_"))
    actor.set_actor_scale3d(scale)

    component = actor.get_component_by_class(unreal.StaticMeshComponent)
    if component:
        component.set_static_mesh(mesh)
        set_component_movable(component)
        try:
            component.set_collision_profile_name("BlockAll")
        except Exception:
            pass
        if material_color:
            component.set_editor_property("hidden_in_game", False)
    return actor


def hide_actor_rendering(actor):
    for component in actor.get_components_by_class(unreal.PrimitiveComponent):
        try:
            component.set_visibility(False)
            component.set_hidden_in_game(True)
        except Exception:
            pass


def disable_actor_collision(actor):
    for component in actor.get_components_by_class(unreal.PrimitiveComponent):
        try:
            component.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
        except Exception:
            pass


def spawn_sprite(label, sprite_plane, location, scale=1.0, layer=0, actor_class=None):
    spawn_class = actor_class if actor_class else unreal.StaticMeshActor
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        spawn_class,
        location,
        unreal.Rotator(90.0, 0.0, 0.0),
    )
    set_label(actor, "Slice01_Sakura_" + label.replace(" ", "_"))
    plane_width = max(sprite_plane["width"], 1.0)
    plane_height = max(sprite_plane["height"], 1.0)
    if isinstance(scale, (tuple, list)):
        scale_x = float(scale[0])
        scale_z = float(scale[1])
    else:
        scale_x = float(scale)
        scale_z = float(scale)
    actor.set_actor_scale3d(unreal.Vector(plane_width * scale_x / 100.0, plane_height * scale_z / 100.0, 1.0))
    component = actor.get_component_by_class(unreal.StaticMeshComponent)
    if component:
        component.set_static_mesh(load_asset(PLANE_PATH))
        set_component_movable(component)
        component.set_editor_property("translucency_sort_priority", layer)
        component.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
        material = sprite_plane.get("material")
        if material:
            component.set_material(0, material)
    return actor


def configure_parallax_actor(actor):
    try_set_editor_property(actor, ("auto_follow_player", "b_auto_follow_player"), True)
    try_set_editor_property(actor, ("horizontal_follow_factor",), 1.0)
    try_set_editor_property(actor, ("lock_depth_and_height", "b_lock_depth_and_height"), True)


def spawn_parallax_layer(label, layer, parallax_actor_class):
    plane_width = max(layer["width"], 1.0) * float(layer["scale_x"])
    for tile_offset in PARALLAX_TILE_OFFSETS:
        tile_label = label
        if tile_offset < 0:
            tile_label += "_Left"
        elif tile_offset > 0:
            tile_label += "_Right"
        tile_location = unreal.Vector(
            layer["location"].x + (plane_width * float(tile_offset)),
            layer["location"].y,
            layer["location"].z,
        )
        actor = spawn_sprite(
            tile_label,
            layer,
            tile_location,
            (layer["scale_x"], layer["scale_z"]),
            layer["sort_priority"],
            parallax_actor_class,
        )
        configure_parallax_actor(actor)


def get_main_floor_surface_z():
    return MAIN_FLOOR_LOCATION_Z + BASIC_CUBE_HALF_EXTENT * COLLISION_SCALE_FLOOR_MAIN.z


def spawn_playable_bounds(mesh):
    floor_surface_z = get_main_floor_surface_z()
    bound_center_z = floor_surface_z + BASIC_CUBE_HALF_EXTENT * COLLISION_SCALE_PLAYABLE_BOUND.z
    left_bound = spawn_static_mesh(
        "Collision_Bounds_Left",
        mesh,
        side_location(PLAYABLE_BOUNDS_MIN_X, bound_center_z),
        COLLISION_SCALE_PLAYABLE_BOUND,
    )
    right_bound = spawn_static_mesh(
        "Collision_Bounds_Right",
        mesh,
        side_location(PLAYABLE_BOUNDS_MAX_X, bound_center_z),
        COLLISION_SCALE_PLAYABLE_BOUND,
    )
    return (left_bound, right_bound)


def spawn_visible_floor_tiles(sprite_planes):
    floor_surface_z = get_main_floor_surface_z()
    tile_names = [name for name in VISIBLE_FLOOR_TILE_PATTERN if name in sprite_planes]
    if not tile_names:
        raise RuntimeError("No Sakura floor tile planes are available for visible gameplay floor.")

    tile_width = max(sprite_planes[tile_names[0]]["width"] * VISIBLE_FLOOR_TILE_SCALE, 1.0)
    tile_count = int((VISIBLE_FLOOR_TILE_EXTENT_X * 2.0) / tile_width) + 3
    first_x = -tile_width * float(tile_count - 1) * 0.5

    for tile_index in range(tile_count):
        tile_name = tile_names[tile_index % len(tile_names)]
        tile = sprite_planes[tile_name]
        tile_height = max(tile["height"] * VISIBLE_FLOOR_TILE_SCALE, 1.0)
        tile_x = first_x + tile_width * float(tile_index)
        tile_z = floor_surface_z - tile_height * 0.5
        spawn_sprite(
            "GroundTile_{:03d}".format(tile_index),
            tile,
            side_location(tile_x, tile_z, ART_PLANE_Y),
            VISIBLE_FLOOR_TILE_SCALE,
            VISIBLE_FLOOR_TILE_LAYER,
        )


def spawn_anchor(label, anchor_class, marker_mesh, location, anchor_type=None):
    anchor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        anchor_class,
        location,
        unreal.Rotator(0.0, 0.0, 0.0),
    )
    set_label(anchor, "Slice01_Anchor_" + label.replace(" ", "_"))
    if anchor_type:
        try:
            anchor.set_editor_property("anchor_type", anchor_type)
        except Exception:
            pass

    marker = spawn_static_mesh(
        "AnchorMarker_" + label,
        marker_mesh,
        location,
        unreal.Vector(0.28, 0.28, 0.28),
    )
    disable_actor_collision(marker)
    if not SHOW_ANCHOR_MARKERS:
        hide_actor_rendering(marker)
    spawn_text(label, unreal.Vector(location.x, TEXT_PLANE_Y, location.z + 65.0), 18.0)
    return anchor, marker


def spawn_grabbable_prop(label, anchor_class, visual_plane, location, scale, anchor_type=None):
    anchor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        anchor_class,
        location,
        unreal.Rotator(90.0, 0.0, 0.0),
    )
    set_label(anchor, "Slice01_Grabbable_" + label.replace(" ", "_"))
    try_set_editor_property(
        anchor,
        ("pull_anchor_to_grappler", "b_pull_anchor_to_grappler", "bPullAnchorToGrappler"),
        True,
    )
    try_set_editor_property(anchor, ("arrival_radius", "ArrivalRadius"), 72.0)
    if anchor_type:
        try_set_editor_property(anchor, ("anchor_type", "AnchorType"), anchor_type)

    component = anchor.get_component_by_class(unreal.StaticMeshComponent)
    if component:
        component.set_static_mesh(load_asset(PLANE_PATH))
        set_component_movable(component)
        plane_width = max(visual_plane["width"], 1.0)
        plane_height = max(visual_plane["height"], 1.0)
        anchor.set_actor_scale3d(unreal.Vector(plane_width * scale.x / 100.0, plane_height * scale.z / 100.0, 1.0))
        material = visual_plane.get("material")
        if material:
            component.set_material(0, material)
        try:
            component.set_editor_property("translucency_sort_priority", 35)
        except Exception:
            pass
        try:
            component.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
        except Exception:
            pass
        try:
            component.set_collision_profile_name("NoCollision")
        except Exception:
            pass
        try:
            component.set_visibility(True)
            component.set_hidden_in_game(False)
        except Exception:
            pass
        # Keep the C++ AnchorDisplayMesh as the visible movable prop, but feed it
        # Sakura art instead of a black debug cube.
        try:
            component.set_editor_property("component_tags", [unreal.Name("AnchorDisplayMesh")])
        except Exception:
            pass

    spawn_text(label, unreal.Vector(location.x, TEXT_PLANE_Y, location.z + 78.0), 16.0)
    return anchor


def resolve_anchor_type(name):
    for enum_name in ("EGrappleAnchorType", "GrappleAnchorType"):
        enum_type = getattr(unreal, enum_name, None)
        if enum_type and hasattr(enum_type, name):
            return getattr(enum_type, name)
    return None


def spawn_lighting():
    light = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.DirectionalLight,
        unreal.Vector(-500.0, -350.0, 650.0),
        unreal.Rotator(-42.0, -35.0, 0.0),
    )
    set_label(light, "Slice01_KeyLight")
    component = light.get_component_by_class(unreal.DirectionalLightComponent)
    if component:
        set_component_movable(component)
        component.set_editor_property("intensity", 8.0)

    sky = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.SkyLight,
        unreal.Vector(0.0, 0.0, 500.0),
        unreal.Rotator(0.0, 0.0, 0.0),
    )
    set_label(sky, "Slice01_SkyLight")
    sky_component = sky.get_component_by_class(unreal.SkyLightComponent)
    if sky_component:
        set_component_movable(sky_component)
        sky_component.set_editor_property("intensity", 1.8)


def validate_playable_player(actor):
    mesh_component = actor.get_component_by_class(unreal.SkeletalMeshComponent)
    if not mesh_component:
        raise RuntimeError("Playable player has no SkeletalMeshComponent.")

    skeletal_mesh = None
    for accessor in ("get_skeletal_mesh_asset", "get_skeletal_mesh"):
        if hasattr(mesh_component, accessor):
            skeletal_mesh = getattr(mesh_component, accessor)()
            break
    if not skeletal_mesh:
        try:
            skeletal_mesh = mesh_component.get_editor_property("skeletal_mesh_asset")
        except Exception:
            skeletal_mesh = None
    if not skeletal_mesh:
        raise RuntimeError("Playable player has no Jacob skeletal mesh assigned.")

    anim_instance = mesh_component.get_anim_instance() if hasattr(mesh_component, "get_anim_instance") else None
    if not anim_instance:
        log("Playable player has no live AnimInstance in commandlet mode; PIE should create it from single-node fallback.")

    required_components = [
        "VestigeLimbComponent",
        "VestigeTentacleVisualAdapter",
        "CameraBoom",
        "SideViewCamera",
    ]
    missing = []
    for name in required_components:
        try:
            if not actor.get_editor_property(name):
                missing.append(name)
        except Exception:
            # Components are also discoverable by name on spawned C++ actors.
            if not any(component.get_name() == name for component in actor.get_components_by_class(unreal.ActorComponent)):
                missing.append(name)
    if missing:
        raise RuntimeError("Playable player missing components: " + ", ".join(missing))


def main():
    player_class = load_class(PLAYER_CLASS_PATH)
    anchor_class = load_class(ANCHOR_CLASS_PATH)
    parallax_actor_class = load_class(PARALLAX_LAYER_CLASS_PATH)
    cube = load_asset(CUBE_PATH)
    sphere = load_asset(SPHERE_PATH)
    load_asset(PLANE_PATH)
    build_sakura_sprite_library()
    sakura_sprites = build_sakura_plane_library()
    parallax_layers = build_sakura_parallax_library()

    open_or_create_level()
    clear_test_actors()
    disable_static_lighting_for_level()
    spawn_lighting()

    for layer_name in ("SkyClouds", "DistantTemples", "MidgroundGarden", "ForegroundRuins"):
        layer = parallax_layers[layer_name]
        spawn_parallax_layer("Parallax_" + layer_name, layer, parallax_actor_class)

    player = unreal.EditorLevelLibrary.spawn_actor_from_class(
        player_class,
        side_location(0.0, PLAYER_START_Z),
        unreal.Rotator(0.0, 0.0, 0.0),
    )
    set_label(player, "Slice01_PlayablePlayer")
    set_autopossess_player0(player)
    validate_playable_player(player)

    floor_main = spawn_static_mesh(
        "Collision_Floor_Main",
        cube,
        side_location(0.0, MAIN_FLOOR_LOCATION_Z),
        COLLISION_SCALE_FLOOR_MAIN,
    )
    jump_low = spawn_static_mesh("Collision_Jump_Platform_Low", cube, side_location(720.0, 120.0), COLLISION_SCALE_PLATFORM_LOW)
    jump_high = spawn_static_mesh("Collision_Jump_Platform_High", cube, side_location(1120.0, 330.0), COLLISION_SCALE_PLATFORM_HIGH)
    slide_ceiling = spawn_static_mesh("Collision_Slide_Ceiling", cube, side_location(-650.0, 165.0), COLLISION_SCALE_SLIDE_CEILING)
    slide_ground = spawn_static_mesh("Collision_Slide_GroundMarker", cube, side_location(-650.0, 4.0), COLLISION_SCALE_SLIDE_MARKER)
    playable_bounds = spawn_playable_bounds(cube)
    for collision_actor in (floor_main, jump_low, jump_high, slide_ceiling, slide_ground) + playable_bounds:
        hide_actor_rendering(collision_actor)

    spawn_visible_floor_tiles(sakura_sprites)

    spawn_anchor("Grapple Right Near", anchor_class, sphere, side_location(470.0, 330.0))
    spawn_anchor("Grapple Left Near", anchor_class, sphere, side_location(-470.0, 330.0))
    spawn_anchor("Grapple High", anchor_class, sphere, side_location(820.0, 560.0))
    spawn_anchor("Grapple Blocked", anchor_class, sphere, side_location(720.0, 330.0))
    blocker = spawn_static_mesh("Grapple_LOS_Blocker", cube, side_location(610.0, 220.0), unreal.Vector(0.12, 0.6, 1.8))
    hide_actor_rendering(blocker)
    floor_surface_z = get_main_floor_surface_z()
    lantern_plane = sakura_sprites["SP_SakuraLantern"]
    lantern_left_scale = unreal.Vector(0.82, 0.82, 0.82)
    lantern_right_scale = unreal.Vector(0.92, 0.92, 0.92)
    spawn_grabbable_prop(
        "Lantern Crate Left",
        anchor_class,
        lantern_plane,
        side_location(-320.0, floor_surface_z + lantern_plane["height"] * lantern_left_scale.z * 0.5),
        lantern_left_scale,
        resolve_anchor_type("Signal"),
    )
    spawn_grabbable_prop(
        "Lantern Crate Right",
        anchor_class,
        lantern_plane,
        side_location(360.0, floor_surface_z + lantern_plane["height"] * lantern_right_scale.z * 0.5),
        lantern_right_scale,
        resolve_anchor_type("Signal"),
    )
    spawn_anchor("Consume Dummy", anchor_class, sphere, side_location(-1120.0, 120.0), resolve_anchor_type("Enemy"))
    dummy_collision = spawn_static_mesh("AttackConsumeDummy", cube, side_location(-1120.0, 70.0), unreal.Vector(0.55, 0.55, 1.4))
    hide_actor_rendering(dummy_collision)
    spawn_sprite(
        "AttackConsumeDummyVisual",
        sakura_sprites["SP_SakuraGateRed"],
        side_location(-1120.0, floor_surface_z + 95.0, ART_PLANE_Y),
        0.95,
        30,
    )

    spawn_text(
        "Controls: A/D or stick/D-pad move, Space/A jump, Shift/LB slide, E/RB grapple, LMB/RT attack, F/Y consume",
        side_location(0.0, 315.0, TEXT_PLANE_Y),
        20.0,
    )
    spawn_text("Slide lane", side_location(-650.0, 255.0, TEXT_PLANE_Y), 18.0)
    spawn_text("Jump lane", side_location(920.0, 455.0, TEXT_PLANE_Y), 18.0)
    spawn_text("Attack / consume dummy", side_location(-1120.0, 240.0, TEXT_PLANE_Y), 18.0)

    level_subsystem = get_level_editor_subsystem()
    if level_subsystem:
        level_subsystem.save_current_level()
    else:
        unreal.EditorLevelLibrary.save_current_level()
    log("Built gameplay test level: " + LEVEL_PATH)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        unreal.log_error(str(exc))
        raise

