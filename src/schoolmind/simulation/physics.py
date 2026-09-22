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