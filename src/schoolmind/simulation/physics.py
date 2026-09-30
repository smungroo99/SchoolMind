import pygame


def update_velocity(
    velocity: pygame.Vector2,
    desired_direction: pygame.Vector2,
    target_speed: float,
    max_speed: float,
    max_acceleration: float,
    dt: float,
) -> pygame.Vector2:
    """Return the new velocity after steering toward a desired direction."""
    if dt <= 0:
        return velocity.copy()

    if desired_direction.length_squared() == 0:
        return velocity.copy()

    desired_direction = desired_direction.normalize()

    # The velocity we would have if we were already
    # travelling in the desired direction.
    desired_velocity = desired_direction * target_speed

    # How much we need to change our current velocity.
    steering = desired_velocity - velocity

    # Convert the required velocity change into acceleration.
    acceleration = steering / dt

    # Limit how quickly the agent can accelerate.
    if acceleration.length_squared() > max_acceleration**2:
        acceleration.scale_to_length(max_acceleration)

    # Apply the acceleration.
    new_velocity = velocity + acceleration * dt

    # Never allow the agent to exceed maximum speed.
    if new_velocity.length_squared() > max_speed**2:
        new_velocity.scale_to_length(max_speed)

    return new_velocity

def adjust_direction_for_boundary(
    desired_direction: pygame.Vector2,
    current_velocity: pygame.Vector2,
    position: pygame.Vector2,
    world_width: int,
    world_height: int,
    boundary_margin: float,
) -> pygame.Vector2:
    """
    Adjust a desired direction so the entity does not steer into
    a nearby boundary.

    The boundary acts as a constraint rather than a competing force.

    If the desired direction points into a wall, the component pointing
    into that wall is removed. The remaining tangential direction is
    preserved.

    This prevents a wall from forcing an artificial 180-degree turn.
    """
    if desired_direction.length_squared() == 0:
        return current_velocity.copy()

    direction = desired_direction.normalize()

    if boundary_margin <= 0:
        return direction

    adjusted = direction.copy()

    near_left = position.x <= boundary_margin
    near_right = (
        position.x >= world_width - boundary_margin
    )
    near_top = position.y <= boundary_margin
    near_bottom = (
        position.y >= world_height - boundary_margin
    )

    # --------------------------------------------------------------
    # Left wall
    # --------------------------------------------------------------
    if near_left and adjusted.x < 0:
        adjusted.x = 0

    # --------------------------------------------------------------
    # Right wall
    # --------------------------------------------------------------
    if near_right and adjusted.x > 0:
        adjusted.x = 0

    # --------------------------------------------------------------
    # Top wall
    # --------------------------------------------------------------
    if near_top and adjusted.y < 0:
        adjusted.y = 0

    # --------------------------------------------------------------
    # Bottom wall
    # --------------------------------------------------------------
    if near_bottom and adjusted.y > 0:
        adjusted.y = 0

    # --------------------------------------------------------------
    # If the desired direction pointed directly into a wall,
    # the projection above can result in a zero vector.
    #
    # Use the current movement direction to determine which way
    # along the wall to travel.
    # --------------------------------------------------------------
    if adjusted.length_squared() == 0:
        if current_velocity.length_squared() > 0:
            current_direction = (
                current_velocity.normalize()
            )

            adjusted = current_direction.copy()

            if near_left and adjusted.x < 0:
                adjusted.x = 0

            if near_right and adjusted.x > 0:
                adjusted.x = 0

            if near_top and adjusted.y < 0:
                adjusted.y = 0

            if near_bottom and adjusted.y > 0:
                adjusted.y = 0

        # If the fish is completely stopped and is pointing
        # directly into a wall, choose a deterministic tangential
        # direction rather than allowing it to reverse.
        if adjusted.length_squared() == 0:
            if near_left or near_right:
                adjusted = pygame.Vector2(0, 1)
            else:
                adjusted = pygame.Vector2(1, 0)

    return adjusted.normalize()

def constrain_to_bounds(
    position: pygame.Vector2,
    velocity: pygame.Vector2,
    world_width: int,
    world_height: int,
    radius: float = 0.0,
) -> pygame.Vector2:
    """
    Keep an entity inside the rectangular world.

    If an entity reaches a boundary, the corresponding velocity
    component is reflected, producing a bounce.
    """
    min_x = radius
    max_x = world_width - radius
    min_y = radius
    max_y = world_height - radius

    if min_x > max_x or min_y > max_y:
        raise ValueError(
            "Entity radius is too large for the world dimensions."
        )

    if position.x < min_x:
        position.x = min_x

        if velocity.x < 0:
            velocity.x = -velocity.x

    elif position.x > max_x:
        position.x = max_x

        if velocity.x > 0:
            velocity.x = -velocity.x

    if position.y < min_y:
        position.y = min_y

        if velocity.y < 0:
            velocity.y = -velocity.y

    elif position.y > max_y:
        position.y = max_y

        if velocity.y > 0:
            velocity.y = -velocity.y

    return velocity