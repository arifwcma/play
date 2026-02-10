import numpy as np
import pygame


def step(s: np.ndarray) -> np.ndarray:
    alive = (s == 1).astype(np.uint8)
    n = (
        np.roll(np.roll(alive, 1, 0), 1, 1)
        + np.roll(alive, 1, 0)
        + np.roll(np.roll(alive, 1, 0), -1, 1)
        + np.roll(alive, 1, 1)
        + np.roll(alive, -1, 1)
        + np.roll(np.roll(alive, -1, 0), 1, 1)
        + np.roll(alive, -1, 0)
        + np.roll(np.roll(alive, -1, 0), -1, 1)
    )
    nxt = np.zeros_like(s)
    nxt[s == 1] = 2
    nxt[s == 2] = 0
    nxt[(s == 0) & (n == 2)] = 1
    return nxt


def main() -> None:
    cell = 6
    w, h = 140, 90
    fps = 60

    pygame.init()
    screen = pygame.display.set_mode((w * cell, h * cell))
    pygame.display.set_caption("Brian's Brain")
    clock = pygame.time.Clock()

    s = np.zeros((h, w), dtype=np.uint8)
    s[np.random.rand(h, w) < 0.12] = 1
    paused = False

    running = True
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_SPACE:
                    paused = not paused
                elif ev.key == pygame.K_r:
                    s[:] = 0
                    s[np.random.rand(h, w) < 0.12] = 1
                elif ev.key == pygame.K_c:
                    s[:] = 0
                elif ev.key == pygame.K_n and paused:
                    s = step(s)
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                mx, my = ev.pos
                x, y = mx // cell, my // cell
                if 0 <= x < w and 0 <= y < h:
                    s[y, x] = 1

        if not paused:
            s = step(s)

        alive = (s == 1).astype(np.uint8) * 255
        dying = (s == 2).astype(np.uint8) * 120
        r = alive
        g = alive
        b = np.clip(alive + dying, 0, 255).astype(np.uint8)
        rgb = np.dstack([r, g, b]).astype(np.uint8)
        surf = pygame.surfarray.make_surface(rgb.swapaxes(0, 1))
        if cell != 1:
            surf = pygame.transform.scale(surf, (w * cell, h * cell))
        screen.blit(surf, (0, 0))
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()


if __name__ == "__main__":
    main()

