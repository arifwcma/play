from PIL import Image
import numpy as np

img = Image.open("1560.png")
arr = np.array(img)
print(arr)
np.savetxt("tile.csv", arr.reshape(-1, arr.shape[-1]), delimiter=",", fmt="%d")
