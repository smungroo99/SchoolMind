import pygame

from schoolmind.simulation.config import SimulationConfig
from schoolmind.simulation.world import World


class Renderer:
    def __init__(self, config: SimulationConfig) -> None:
        self.config = config

        self.screen = pygame.display.set_mode((config.width, config.height))

        pygame.display.set_caption("SchoolMind")

    def render(self, world: World) -> None:
        self.screen.fill((20, 25, 30))

        for fish in world.fish:
            self._draw_fish(fish)

        pygame.display.flip()

    def _draw_fish(self, fish) -> None:
        direction = fish.velocity.normalize()
        perpendicular = pygame.Vector2(-direction.y, direction.x)

        body_length = 18
        body_width = 8
        tail_length = 7

        # Body centre is slightly ahead of the simulation position.
        body_center = fish.position + direction * 2

        # Rotate a simple oval so it follows the fish's velocity.
        body_surface = pygame.Surface((body_length, body_width), pygame.SRCALPHA)

        pygame.draw.ellipse(
            body_surface,
            (220, 220, 220),
            (0, 0, body_length, body_width),
        )

        angle = direction.angle_to(pygame.Vector2(1, 0))
        rotated_body = pygame.transform.rotate(body_surface, angle)

        body_rect = rotated_body.get_rect(
            center=(int(body_center.x), int(body_center.y))
        )

        self.screen.blit(rotated_body, body_rect)

        # Triangle tail.
        tail_base = fish.position - direction * (body_length / 2 - 1)

        tail_tip = tail_base

        tail_top = tail_base - direction * tail_length + perpendicular * (body_width / 2)
        tail_bottom = tail_base - direction * tail_length - perpendicular * (body_width / 2)

        pygame.draw.polygon(
            self.screen,
            (180, 180, 180),
            [
                (int(tail_tip.x), int(tail_tip.y)),
                (int(tail_top.x), int(tail_top.y)),
                (int(tail_bottom.x), int(tail_bottom.y)),
            ],
)