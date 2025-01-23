import noise
import numpy as np
import matplotlib.pyplot as plt

def fbm_altitude(start, stop, step,  # general params
                 frequency, amplitude,  # perlin params
                 octaves, lacunarity, h,  # fBM params
                 offset):  # statistics by altitude params
    xx = np.arange(start, stop, step)
    shape = (xx.size, xx.size)

    yy = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            f = frequency
            total_value = 0  # pour accumuler la somme des octaves
            for o in range(octaves):
                # Calcul du gain pour chaque octave
                gain = amplitude * (lacunarity**(-h * o))  # ajustement du gain
                # Ajout du bruit Perlin avec offset et gain
                total_value += gain * noise.pnoise2(f*xx[i], f*xx[j])  
                f *= lacunarity  # incrémentation de la fréquence pour chaque octave
            yy[i][j] = total_value + offset  # application de l'offset après toutes les octaves
    return yy

def normalize(x):
    # Normalisation de la heightmap entre 0 et 1
    x -= x.min()  # on retire la valeur minimale
    x /= x.max()  # on divise par la valeur maximale
    return x

def generate_minecraft_heightmap(start, stop, step, frequency, amplitude, octaves, lacunarity, h, offset):
    # Génère la heightmap avec des valeurs discrètes de type "cubique"
    heightmap = fbm_altitude(start, stop, step, frequency, amplitude, octaves, lacunarity, h, offset)
    heightmap = normalize(heightmap)
    
    # Arrondi les valeurs pour donner l'effet de blocs Minecraft
    heightmap = np.floor(heightmap * 10)  # Multiplie et arrondi pour augmenter la taille des "blocs"
    
    # Limite les hauteurs entre 0 et 256 (typique pour Minecraft)
    heightmap = np.clip(heightmap, 0, 256)
    
    return heightmap

############## generate minecraft-style heightmap ##############
start = 200
stop = 800
step = 1
frequency = 0.05  # Fréquence plus faible pour des transitions douces
amplitude = 0.5  # Réduit l'amplitude pour un terrain plus doux
octaves = 4  # Augmenter les octaves pour plus de détails
lacunarity = 0.5  # Un peu plus élevé pour des détails plus fins mais réguliers
h = 0.99  # Moins rugueux, pour un terrain plus lisse
offset = 0.1  # Ajuste l'offset pour un terrain réaliste

heightmap = generate_minecraft_heightmap(
    start=start,
    stop=stop,
    step=step,
    frequency=frequency,
    amplitude=amplitude,
    octaves=octaves,
    lacunarity=lacunarity,
    h=h,
    offset=offset
)

# Création de la grille X, Y
x = np.arange(0, heightmap.shape[0], 1)
y = np.arange(0, heightmap.shape[1], 1)
x, y = np.meshgrid(x, y)

# Initialisation de la figure
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Surface 3D avec heightmap cubique
ax.plot_surface(x, y, heightmap, cmap='terrain', edgecolor='none')

# Titres et labels
ax.set_title("Visualisation 3D du terrain style Minecraft")
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Altitude')

# Affichage de la visualisation
plt.show()

# Sauvegarde de l'image en 3D
fig.savefig(f'3D_minecraft_heightMap_f{frequency}_A{amplitude}_O{octaves}_L{lacunarity}_H{h}_offset{offset}.png', bbox_inches='tight', pad_inches=0)
