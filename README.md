# Génération procédurale de terrain avec bruit de Perlin et fBM

## Description

Ce projet implémente un algorithme de génération procédurale de terrain à l'aide du **bruit de Perlin** et du **Fractal Brownian Motion (fBM)**. Ces techniques sont utilisées pour créer des cartes de hauteur réalistes et variées, adaptées à des applications comme la simulation de mondes 3D et la génération de terrains pour les jeux vidéo.

## Algorithmes utilisés

### 1. Bruit de Perlin (Perlin Noise)

Le **bruit de Perlin** est un type de bruit cohérent qui génère des variations continues dans l'espace. Il est souvent utilisé pour créer des textures et des terrains procéduraux en raison de ses propriétés naturelles. Contrairement à un bruit aléatoire classique, le bruit de Perlin est lisse et a des caractéristiques de continuité, ce qui le rend adapté à la modélisation de phénomènes naturels.

#### Formule mathématique du bruit de Perlin

Le bruit de Perlin est basé sur une fonction qui utilise des gradients et des interpolations. Pour une dimension, la fonction du bruit est généralement donnée par :

\[ p(x) = \sum_{i=0}^{n} g_i \cdot (x - x_i) \cdot W(x) \]

Où :
- \( p(x) \) est la valeur du bruit à la position \( x \).
- \( g_i \) est un gradient aléatoire (généralement une direction vectorielle) à chaque point de la grille.
- \( (x - x_i) \) est la distance entre le point \( x \) et la position \( x_i \).
- \( W(x) \) est une fonction d'interpolation qui est utilisée pour lisser les transitions entre les points.

La version 2D du bruit de Perlin, qui est utilisée dans ce projet, fonctionne sur une grille bidimensionnelle, où chaque point de la grille possède une direction de gradient. Le bruit à un point \( (x, y) \) est calculé de manière similaire en fonction des gradients et des interpolations bidimensionnelles.

### 2. Fractal Brownian Motion (fBM)

Le **Fractal Brownian Motion (fBM)** est une méthode qui permet de créer des surfaces fractales en combinant plusieurs couches de bruit de Perlin (ou d'autres types de bruit). Chaque couche est un bruit de Perlin à une échelle différente, et la somme des différentes couches produit un terrain complexe et naturel.

#### Fonction fBM

La formule générale pour le **Fractal Brownian Motion** est la suivante :

\[
fBM(x, y) = \sum_{i=0}^{n} \frac{1}{2^i} \cdot \text{Noise}(x \cdot 2^i, y \cdot 2^i)
\]

Où :
- \( fBM(x, y) \) est la valeur finale du bruit fractal à la position \( (x, y) \).
- \( \text{Noise}(x \cdot 2^i, y \cdot 2^i) \) est une valeur de bruit de Perlin à une échelle donnée (échelle \( i \)).
- Le terme \( \frac{1}{2^i} \) est un facteur de réduction de l'amplitude du bruit à chaque couche, ce qui permet de créer des variations plus fines à chaque niveau d'échelle.

Les différents termes de bruit sont superposés pour générer un terrain complexe. Le paramètre \( n \) détermine le nombre de couches (octaves), et les paramètres \( h \) (persistante) et \( lacunarity \) influencent respectivement la réduction d'amplitude et l'augmentation de la fréquence à chaque octave.

#### Paramètres importants pour le fBM :
- **Octaves** : Le nombre de couches de bruit utilisées. Plus il y a d'octaves, plus le terrain devient complexe.
- **Persistante** : La manière dont l'amplitude du bruit diminue avec chaque octave. Cela affecte la "rugosité" du terrain.
- **Lacunarity** : Le facteur par lequel la fréquence du bruit augmente à chaque octave. Cela détermine la finesse des détails.

### 3. Normalisation du terrain

La **normalisation** du terrain est utilisée pour ajuster les valeurs générées par le bruit dans une plage souhaitée, généralement entre 0 et 1. Cela permet de rendre le terrain plus cohérent et contrôlable, en supprimant les valeurs extrêmes qui peuvent causer des artefacts visuels.

#### Formule de normalisation

La normalisation est effectuée en deux étapes :
1. On soustrait la valeur minimale à chaque élément de la matrice.
2. On divise ensuite le résultat par la valeur maximale pour obtenir une plage de valeurs entre 0 et 1.

La formule de normalisation est donc :

\[
x_{\text{norm}} = \frac{x - \min(x)}{\max(x) - \min(x)}
\]

Où \( x \) est la matrice de terrain générée, et \( x_{\text{norm}} \) est la version normalisée.

### 4. Application d'un colormap

Pour rendre le terrain plus visuellement intéressant, un **colormap** est appliqué pour transformer les valeurs d'altitude en couleurs réalistes. Ce colormap est défini manuellement, en attribuant des couleurs spécifiques à différentes plages d'altitude (par exemple, bleu pour les zones d'eau, vert pour les forêts, blanc pour la neige, etc.).

### Exemple de paramètres du colormap :
- **Coastline (plage de l'océan)** : altitudes faibles (par exemple, 0-50).
- **Pastures (pâturages)** : altitudes moyennes (par exemple, 50-100).
- **Mountains (montagnes)** : altitudes élevées (par exemple, 100-150).
- **Snow (neige)** : altitudes très élevées (par exemple, 150+).

## Conclusion

Ce projet implémente une méthode puissante pour la génération de terrains procéduraux, en utilisant des techniques comme le **bruit de Perlin** et le **Fractal Brownian Motion (fBM)**. Ces algorithmes permettent de créer des terrains variés, réalistes et complexes de manière automatique, avec un contrôle total sur les caractéristiques du terrain (rugosité, fréquence des détails, etc.). La génération procédurale est un outil fondamental dans la création de mondes virtuels pour les jeux vidéo et la simulation.

---