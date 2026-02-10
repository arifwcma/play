import numpy as np
import pygame


def step(g: np.ndarray) -> np.ndarray:
    n = (
        np.roll(np.roll(g, 1, 0), 1, 1)
        + np.roll(g, 1, 0)
        + np.roll(np.roll(g, 1, 0), -1, 1)
        + np.roll(g, 1, 1)
        + np.roll(g, -1, 1)
        + np.roll(np.roll(g, -1, 0), 1, 1)
        + np.roll(g, -1, 0)
        + np.roll(np.roll(g, -1, 0), -1, 1)
    )
    return ((n == 3) | ((g == 1) & (n == 2))).astype(np.uint8)


def main() -> None:
    cell = 8
    w, h = 120, 80
    fps = 60

    pygame.init()
    screen = pygame.display.set_mode((w * cell, h * cell))
    pygame.display.set_caption("Game of Life (numpy + pygame)")
    clock = pygame.time.Clock()

    g = (np.random.rand(h, w) < 0.15).astype(np.uint8)
    paused = False

    running = True
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_SPACE:
                    paused = not paused
                elif ev.key == pygame.K_c:
                    g[:] = 0
                elif ev.key == pygame.K_r:
                    g[:] = (np.random.rand(h, w) < 0.15).astype(np.uint8)
                elif ev.key == pygame.K_n and paused:
                    g = step(g)
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                mx, my = ev.pos
                x, y = mx // cell, my // cell
                if 0 <= x < w and 0 <= y < h:
                    g[y, x] ^= 1

        if not paused:
            g = step(g)

        rgb = (g * 255).astype(np.uint8)
        img = np.dstack([rgb, rgb, rgb])
        surf = pygame.surfarray.make_surface(img.swapaxes(0, 1))
        surf = pygame.transform.scale(surf, (w * cell, h * cell))
        screen.blit(surf, (0, 0))
        pygame.display.flip()

        clock.tick(fps)

    pygame.quit()


if __name__ == "__main__":
    main()

