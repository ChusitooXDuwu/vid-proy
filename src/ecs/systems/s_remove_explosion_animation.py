import esper

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.tags.c_tag_explosion import CTagExplosion

# Sistema system_remove_explosion_animation encargado de remover la entidad de la explosion
def system_remove_explosion_animation(world: esper.World):
    components = world.get_components(CAnimation, CTagExplosion)

    c_a: CAnimation
    for entity, (c_a, c_te) in components:
        if c_a.current_frame >= c_a.animations_list[c_a.current_animation].end:
            world.delete_entity(entity)