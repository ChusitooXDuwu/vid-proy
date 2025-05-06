import esper

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_player_state import CPlayerState, PlayerState
from src.ecs.components.c_rotation import CRotation


def system_player_state(world: esper.World) -> None:
    components = world.get_components(CAnimation, CPlayerState, CRotation)
    for _, (c_a, c_pst, c_r) in components:
        match c_pst.state:
            case (
                PlayerState.MOVE0
                | PlayerState.MOVE1
                | PlayerState.MOVE2
                | PlayerState.MOVE3
                | PlayerState.MOVE4
                | PlayerState.MOVE5
                | PlayerState.MOVE6
                | PlayerState.MOVE7
                | PlayerState.MOVE8
                | PlayerState.MOVE9
                | PlayerState.MOVE10
                | PlayerState.MOVE11
                | PlayerState.MOVE12
                | PlayerState.MOVE13
                | PlayerState.MOVE14
                | PlayerState.MOVE15
                | PlayerState.MOVE16
                | PlayerState.MOVE17
                | PlayerState.MOVE18
                | PlayerState.MOVE19
                | PlayerState.MOVE20
                | PlayerState.MOVE21
                | PlayerState.MOVE22
                | PlayerState.MOVE23
                | PlayerState.MOVE24
                | PlayerState.MOVE25
                | PlayerState.MOVE26
                | PlayerState.MOVE27
                | PlayerState.MOVE28
                | PlayerState.MOVE29
                | PlayerState.MOVE30
                | PlayerState.MOVE31
            ):
                _do_move_state(c_a, c_r, c_pst)


def _do_move_state(
    c_a: CAnimation,
    c_r: CRotation,
    c_pst: CPlayerState,
) -> None:
    _set_animation(c_a, PlayerState(c_r.index).value)
    c_pst.state = PlayerState(c_r.index)


def _set_animation(c_a: CAnimation, num_animation: int) -> None:
    if c_a.current_animation == num_animation:
        return
    c_a.current_animation = num_animation
    c_a.current_animation_time = 0
    c_a.current_frame = c_a.animations_list[c_a.current_animation].start
