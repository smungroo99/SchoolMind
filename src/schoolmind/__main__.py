import pygame

from schoolmind.simulation.config import SimulationConfig
from schoolmind.simulation.world import World
from schoolmind.visualization.renderer import Renderer


def main() -> None:
    pygame.init()

    config = SimulationConfig()

    world = World(config)
    renderer = Renderer(config)

    clock = pygame.time.Clock()

    running = True

    while running:
        dt = clock.tick(config.fps) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    world.reset()

        world.update(dt)
        renderer.render(world)

    pygame.quit()


if __name__ == "__main__":
    main()