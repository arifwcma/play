import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

NUM_NEEDLES = 300
NEEDLE_LENGTH = 0.8
LINE_SPACING = 1.0
DROP_PER_FRAME = 3
FLOOR_WIDTH = 10
NUM_LINES = int(FLOOR_WIDTH / LINE_SPACING) + 1

fig, (ax_floor, ax_pi) = plt.subplots(1, 2, figsize=(12, 6))
fig.suptitle("Buffon's Needle Simulation", fontsize=14, fontweight="bold")

for i in range(NUM_LINES):
    ax_floor.axhline(y=i * LINE_SPACING, color="steelblue", linewidth=1.5, alpha=0.6)
ax_floor.set_xlim(-0.5, FLOOR_WIDTH + 0.5)
ax_floor.set_ylim(-0.5, (NUM_LINES - 1) * LINE_SPACING + 0.5)
ax_floor.set_aspect("equal")
ax_floor.set_title("Needle Drops")

pi_estimates = []
frames_x = []
ax_pi.axhline(y=np.pi, color="red", linestyle="--", linewidth=1.5, label="actual π")
(line_pi,) = ax_pi.plot([], [], color="green", linewidth=1.5, label="estimate")
ax_pi.set_xlim(0, NUM_NEEDLES)
ax_pi.set_ylim(2, 4.5)
ax_pi.set_xlabel("needles dropped")
ax_pi.set_ylabel("π estimate")
ax_pi.set_title("Estimating π")
ax_pi.legend(loc="upper right")

total_dropped = [0]
total_crossing = [0]


def crosses_line(y_center, angle):
    half_proj = (NEEDLE_LENGTH / 2) * np.sin(angle)
    y_top = y_center + half_proj
    y_bot = y_center - half_proj
    top_line = np.ceil(min(y_top, y_bot) / LINE_SPACING) * LINE_SPACING
    return top_line <= max(y_top, y_bot)


def animate(frame):
    for _ in range(DROP_PER_FRAME):
        if total_dropped[0] >= NUM_NEEDLES:
            return line_pi,

        x_center = np.random.uniform(0, FLOOR_WIDTH)
        y_center = np.random.uniform(0, (NUM_LINES - 1) * LINE_SPACING)
        angle = np.random.uniform(0, np.pi)

        dx = (NEEDLE_LENGTH / 2) * np.cos(angle)
        dy = (NEEDLE_LENGTH / 2) * np.sin(angle)

        hit = crosses_line(y_center, angle)
        color = "red" if hit else "gray"
        alpha = 0.9 if hit else 0.4
        ax_floor.plot([x_center - dx, x_center + dx],
                      [y_center - dy, y_center + dy],
                      color=color, linewidth=1.2, alpha=alpha)

        total_dropped[0] += 1
        if hit:
            total_crossing[0] += 1

        if total_crossing[0] > 0:
            pi_est = (2 * NEEDLE_LENGTH * total_dropped[0]) / (LINE_SPACING * total_crossing[0])
            pi_estimates.append(pi_est)
            frames_x.append(total_dropped[0])
            line_pi.set_data(frames_x, pi_estimates)

    ax_pi.set_title(f"π ≈ {pi_estimates[-1]:.4f}  (n={total_dropped[0]})" if pi_estimates else "Estimating π")
    return line_pi,


ani = animation.FuncAnimation(fig, animate, frames=NUM_NEEDLES // DROP_PER_FRAME + 10,
                              interval=50, blit=False, repeat=False)
plt.tight_layout()
plt.show()
