import pygame

from schoolmind.simulation.config import SimulationConfig
from schoolmind.simulation.world import World


class Renderer:
    def __init__(self, config: SimulationConfig) -> None:
        self.config = config

        self.screen = pygame.display.set_mode(
            (config.width, config.height)
        )

        pygame.display.set_caption("SchoolMind")

        self.font = pygame.font.Font(None, 24)

    def render(self, world: World) -> None:
        self.screen.fill((20, 25, 30))

        for fish in world.fish:
            self._draw_fish(fish)

        for predator in world.predators:
            self._draw_predator(predator)

        self._draw_metrics(world)

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

    def _draw_metrics(self, world: World) -> None:
        metrics = world.get_metrics()

        text = (
            f"Fish: {metrics['fish_alive']}   "
            f"Captured: {metrics['fish_captured']}   "
            f"Predators: {metrics['active_predators']}"
        )

        surface = self.font.render(
            text,
            True,
            (255, 255, 255),
        )

        self.screen.blit(surface, (10, 10))

    def _draw_predator(self, predator) -> None:
        center = pygame.Vector2(predator.position)

        # ------------------------------------------------------------------
        # Orientation
        # ------------------------------------------------------------------
        if predator.velocity.length_squared() > 0:
            direction = predator.velocity.normalize()
        else:
            direction = pygame.Vector2(1, 0)

        # Perpendicular direction.
        side = pygame.Vector2(-direction.y, direction.x)

        def point(forward: float, lateral: float) -> tuple[int, int]:
            """Convert local fish coordinates into screen coordinates."""
            p = center + direction * forward + side * lateral
            return int(p.x), int(p.y)

        # ------------------------------------------------------------------
        # Detection radius
        # ------------------------------------------------------------------
        pygame.draw.circle(
            self.screen,
            (80, 120, 150),
            (int(center.x), int(center.y)),
            int(predator.detection_range),
            1,
        )

        # ------------------------------------------------------------------
        # Main body
        # ------------------------------------------------------------------
        body = [
            point(30, 0),       # Nose
            point(20, -5),
            point(8, -9),
            point(-8, -10),
            point(-22, -6),
            point(-30, 0),      # Tail connection
            point(-22, 6),
            point(-8, 10),
            point(8, 9),
            point(20, 5),
        ]

        pygame.draw.polygon(
            self.screen,
            (30, 100, 160),     # Ocean blue
            body,
        )

        # ------------------------------------------------------------------
        # Blue-grey underside
        # ------------------------------------------------------------------
        underside = [
            point(20, 3),
            point(8, 8),
            point(-8, 8),
            point(-22, 5),
            point(-28, 0),
            point(-20, 2),
            point(-5, 4),
            point(10, 4),
        ]

        pygame.draw.polygon(
            self.screen,
            (100, 130, 145),    # Blue-grey
            underside,
        )

        # ------------------------------------------------------------------
        # Bill / sword
        # ------------------------------------------------------------------
        bill = [
            point(30, 1.5),
            point(62, 0),
            point(30, -1.5),
        ]

        pygame.draw.polygon(
            self.screen,
            (200, 205, 200),    # Light grey
            bill,
        )

        # ------------------------------------------------------------------
        # Large dorsal sail
        # ------------------------------------------------------------------
        dorsal_fin = [
            point(5, -7),
            point(-2, -24),
            point(-8, -31),
            point(-14, -26),
            point(-20, -15),
            point(-22, -6),
        ]

        pygame.draw.polygon(
            self.screen,
            (190, 155, 55),     # Muted golden yellow
            dorsal_fin,
        )

        # Darker lines across the sail.
        for offset in (-15, -10, -5):
            pygame.draw.line(
                self.screen,
                (145, 110, 35), # Dark gold
                point(offset, -7),
                point(offset - 1, -24),
                1,
            )

        # ------------------------------------------------------------------
        # Pectoral fins
        # ------------------------------------------------------------------
        top_fin = [
            point(4, -7),
            point(-5, -20),
            point(-15, -24),
            point(-10, -8),
        ]

        bottom_fin = [
            point(4, 7),
            point(-5, 20),
            point(-15, 24),
            point(-10, 8),
        ]

        pygame.draw.polygon(
            self.screen,
            (190, 155, 55),     # Muted golden yellow
            top_fin,
        )

        pygame.draw.polygon(
            self.screen,
            (190, 155, 55),     # Muted golden yellow
            bottom_fin,
        )

        # ------------------------------------------------------------------
        # Tail
        # ------------------------------------------------------------------
        tail = [
            point(-27, 0),
            point(-43, -12),
            point(-39, 0),
            point(-43, 12),
        ]

        pygame.draw.polygon(
            self.screen,
            (25, 85, 140),      # Darker blue
            tail,
        )

        # ------------------------------------------------------------------
        # Eye
        # ------------------------------------------------------------------
        eye_position = point(18, -5)

        pygame.draw.circle(
            self.screen,
            (15, 15, 15),
            eye_position,
            2,
        )

        # Small white eye highlight.
        pygame.draw.circle(
            self.screen,
            (255, 255, 255),
            point(18.5, -5.5),
            1,
        )

        # ------------------------------------------------------------------
        # Heading indicator
        # ------------------------------------------------------------------
        heading_end = center + direction * 48

        pygame.draw.line(
            self.screen,
            (220, 200, 100),   # Muted yellow
            (int(center.x), int(center.y)),
            (int(heading_end.x), int(heading_end.y)),
            2,
        )

        # ------------------------------------------------------------------
        # Target line
        # ------------------------------------------------------------------
        if predator.target is not None:
            target_position = predator.target.position

            pygame.draw.line(
                self.screen,
                (220, 130, 70),
                (int(center.x), int(center.y)),
                (
                    int(target_position.x),
                    int(target_position.y),
                ),
                1,
            )

        # ------------------------------------------------------------------
        # Predator ID
        # ------------------------------------------------------------------
        label = self.font.render(
            f"P{predator.id}",
            True,
            (255, 255, 255),
        )

        self.screen.blit(
            label,
            (
                int(center.x) + 16,
                int(center.y) - 18,
            ),
        )
