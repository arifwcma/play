import numpy as np
import pygame


def step(a: np.ndarray) -> np.ndarray:
    l = np.roll(a, 1)
    c = a
    r = np.roll(a, -1)
    idx = (l << 2) | (c << 1) | r
    lut = np.array([0, 1, 1, 1, 0, 1, 1, 0], dtype=np.uint8)
    return lut[idx]


def main() -> None:
    cell = 2
    w = 480
    h = 320
    fps = 60

    pygame.init()
    screen = pygame.display.set_mode((w * cell, h * cell))
    pygame.display.set_caption("Rule 110")
    clock = pygame.time.Clock()

    row = np.zeros(w, dtype=np.uint8)
    row[w // 2] = 1
    hist = np.zeros((h, w), dtype=np.uint8)

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
                    row[:] = 0
                    row[w // 2] = 1
                    hist[:] = 0
                elif ev.key == pygame.K_c:
                    row[:] = 0
                    hist[:] = 0
                elif ev.key == pygame.K_n and paused:
                    hist[:-1] = hist[1:]
                    hist[-1] = row
                    row = step(row)

        if not paused:
            hist[:-1] = hist[1:]
            hist[-1] = row
            row = step(row)

        img = (hist * 255).astype(np.uint8)
        rgb = np.dstack([img, img, img])
        surf = pygame.surfarray.make_surface(rgb.swapaxes(0, 1))
        if cell != 1:
            surf = pygame.transform.scale(surf, (w * cell, h * cell))
        screen.blit(surf, (0, 0))
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()


if __name__ == "__main__":
    main()

