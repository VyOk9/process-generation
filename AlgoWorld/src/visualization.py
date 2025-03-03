import noise
import numpy as np
import matplotlib.pyplot as plt


def fbm_altitude(
    start, stop, step, frequency, amplitude, octaves, lacunarity, h, offset
):
    """Génère une heightmap en utilisant le bruit de Perlin et Fractional Brownian Motion (fBM)"""
    xx, yy = np.meshgrid(np.arange(start, stop, step), np.arange(start, stop, step))
    f = frequency
    total_value = np.zeros_like(xx, dtype=np.float32)

    for o in range(octaves):
        gain = amplitude * (lacunarity ** (-h * o))
        total_value += gain * np.vectorize(noise.pnoise2)(
            f * xx, f * yy
        )
        f *= lacunarity

    return total_value + offset


def normalize(x):
    """Normalise la heightmap entre 0 et 1"""
    x = x.astype(np.float32)
    x -= x.min()
    x /= x.max()
    return x


def generate_minecraft_heightmap(
    start,
    stop,
    step,
    frequency,
    amplitude,
    octaves,
    lacunarity,
    h,
    offset,
    block_scale=10,
):
    """Génère une heightmap de type Minecraft avec des valeurs discrètes"""
    heightmap = fbm_altitude(
        start, stop, step, frequency, amplitude, octaves, lacunarity, h, offset
    )
    heightmap = normalize(heightmap)

    heightmap = np.round(heightmap * block_scale)

    heightmap = np.clip(heightmap, 0, 256)

    return heightmap.astype(np.uint8)


def plot_minecraft_terrain(heightmap):
    """Affiche la heightmap en 3D avec un effet cubique"""
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")

    x, y = np.meshgrid(np.arange(heightmap.shape[0]), np.arange(heightmap.shape[1]))

    x, y, z = x.ravel(), y.ravel(), heightmap.ravel()

    ax.bar3d(x, y, np.zeros_like(z), 1, 1, z, shade=True, cmap="terrain")

    ax.set_title("Terrain style Minecraft")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Altitude")
    plt.show()


############## Génération de la heightmap ##############
start = 200
stop = 800
step = 1
frequency = 0.05  # Fréquence plus faible pour des transitions douces
amplitude = 0.99  # Réduit l'amplitude pour un terrain plus doux
octaves = 10  # Augmenter les octaves pour plus de détails
lacunarity = 0.5  # Plus élevé pour des détails fins mais réguliers
h = 0.99  # Moins rugueux, terrain plus lisse
offset = 0.1  # Ajuste l'offset pour un terrain réaliste
block_scale = 10  # Ajuste la granularité des blocs

heightmap = generate_minecraft_heightmap(
    start, stop, step, frequency, amplitude, octaves, lacunarity, h, offset, block_scale
)


plot_minecraft_terrain(heightmap)

plt.savefig(
    f"3D_minecraft_heightMap_f{frequency}_A{amplitude}_O{octaves}_L{lacunarity}_H{h}_offset{offset}.png",
    bbox_inches="tight",
    pad_inches=0,
)