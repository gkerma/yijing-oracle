# 易經 Yi Jing Oracle

**Oracle du Yi Jing avec Grilles "La Livrée d'Hermès" et Fréquences Sacrées**

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/cybermind-fr/yijing-oracle)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

---

## 📖 Description

Ce programme permet de consulter l'oracle du **Yi Jing** (易經, I Ching, Livre des Mutations) avec une visualisation unique basée sur les grilles de **"La Livrée d'Hermès"** créées par **Anibal Edelbert Amiot**.

### Fonctionnalités

- 🎴 **Tirage automatique** : Simulation de la méthode traditionnelle des 3 pièces
- 🎮 **Grilles visuelles** : Superposition des 6 couches correspondant aux traits
- 📄 **Rapport PDF** : Document complet avec hexagramme, fréquences et grilles
- 🎵 **Sons sacrés** : Fichiers audio basés sur le Solfège ancien (432 Hz)
- 🔄 **Mutations** : Calcul et visualisation de l'hexagramme de mutation

---

## 🚀 Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation des dépendances

```bash
pip install pillow reportlab numpy scipy
```

### Structure du projet

```
yijing-oracle/
├── yijing_oracle.py      # Programme principal
├── images/               # Grilles La Livrée d'Hermès (24 PNG)
│   ├── lldh-YY-YANG-1.png
│   ├── lldh-YY-YANG-2.png
│   ├── ...
│   ├── lldh-YY-YING-MUT-6.png
├── output/               # Fichiers générés
├── README.md             # Cette documentation
└── LICENSE               # Licence MIT
```

---

## 📋 Utilisation

### Tirage simple

```bash
python yijing_oracle.py
```

### Tirage avec question

```bash
python yijing_oracle.py -q "Quelle direction prendre ?"
```

### Définir les traits manuellement

```bash
python yijing_oracle.py -t 7 6 7 6 6 7
```

Les valeurs possibles sont :
- `6` : Yin mutant (vieux Yin)
- `7` : Yang stable (jeune Yang)
- `8` : Yin stable (jeune Yin)
- `9` : Yang mutant (vieux Yang)

### Générer tous les fichiers

```bash
python yijing_oracle.py --all -q "Ma question"
```

Cette commande génère :
- Grille PNG de l'hexagramme principal
- Grille PNG de la mutation (si applicable)
- Rapport PDF complet
- Séquence audio du tirage
- Fichiers audio des fréquences des trigrammes

### Options disponibles

| Option | Description |
|--------|-------------|
| `-q, --question` | Question à poser à l'oracle |
| `-t, --traits` | Définir les 6 traits (ex: `-t 7 6 8 9 7 8`) |
| `-i, --images` | Chemin vers le dossier des images |
| `-o, --output` | Chemin vers le dossier de sortie |
| `--all` | Générer tous les fichiers |
| `--pdf` | Générer uniquement le PDF |
| `--audio` | Générer uniquement les fichiers audio |
| `--grille` | Générer uniquement les grilles PNG |
| `-v, --version` | Afficher la version |

---

## 🎮 Les Grilles "La Livrée d'Hermès"

### Principe

Les 24 grilles représentent les différentes configurations des traits du Yi Jing :

| Type | Nombre | Description |
|------|--------|-------------|
| YANG-1 à YANG-6 | 6 | Traits Yang stables (positions 1-6) |
| YING-1 à YING-6 | 6 | Traits Yin stables (positions 1-6) |
| YANG-MUT-1 à YANG-MUT-6 | 6 | Traits Yang mutants |
| YING-MUT-1 à YING-MUT-6 | 6 | Traits Yin mutants |

### Superposition

La grille finale est créée par **superposition** des 6 images correspondant au tirage, en utilisant le mode "darken" (assombrissement) qui conserve les motifs colorés tout en les combinant.

```
Trait 6 (haut)  ───┐
Trait 5         ───┼── Superposition → Grille unique
Trait 4         ───┤
Trait 3         ───┤
Trait 2         ───┤
Trait 1 (bas)   ───┘
```

---

## 🎵 Système de Fréquences Sacrées

### Fréquences des Trigrammes

Basées sur le **Solfège ancien** et l'accord **432 Hz** :

| Trigramme | Symbole | Élément | Fréquence | Bienfait |
|-----------|---------|---------|-----------|----------|
| ☰ Qián (Ciel) | ≡ | Métal | 852 Hz | Éveil spirituel |
| ☷ Kūn (Terre) | ⚏ | Terre | 396 Hz | Libération |
| ☳ Zhèn (Tonnerre) | ⚌ | Bois | 417 Hz | Transformation |
| ☵ Kǎn (Eau) | ⚍ | Eau | 528 Hz | Réparation ADN |
| ☶ Gèn (Montagne) | ⚎ | Terre | 639 Hz | Connexion |
| ☴ Xùn (Vent) | ⚋ | Bois | 741 Hz | Expression |
| ☲ Lí (Feu) | ⚊ | Feu | 963 Hz | Transcendance |
| ☱ Duì (Lac) | ⚏ | Métal | 432 Hz | Harmonie universelle |

### Fréquences des Traits

| Trait | Valeur | Fréquence | Note |
|-------|--------|-----------|------|
| Yin mutant | 6 | 216 Hz | LA-1 |
| Yang stable | 7 | 256 Hz | DO |
| Yin stable | 8 | 192 Hz | SOL-1 |
| Yang mutant | 9 | 288 Hz | RÉ |

### Fichiers Audio Générés

1. **Séquence du tirage** : Drone 432 Hz + 6 traits + accord final
2. **Fréquence trigramme supérieur** : 1 minute
3. **Fréquence trigramme inférieur** : 1 minute

---

## 📄 Rapport PDF

Le rapport généré contient :

### Page 1
- En-tête avec date et question
- Hexagramme principal (numéro, caractère, nom)
- Tableau des traits avec fréquences
- Trigrammes et leurs qualités
- **Grille La Livrée d'Hermès**

### Page 2
- Accord musical du tirage
- Protocole d'écoute recommandé
- Hexagramme de mutation (si applicable)
- Grille de mutation
- Tableau des fréquences du Solfège

---

## 🔧 Utilisation en tant que bibliothèque

```python
from yijing_oracle import YiJingOracle

# Créer l'oracle
oracle = YiJingOracle(
    images_dir="./images",
    output_dir="./output"
)

# Effectuer un tirage
oracle.effectuer_tirage("Ma question")

# Ou définir les traits manuellement
oracle.definir_traits([7, 6, 7, 6, 6, 7])
oracle.question = "Ma question"

# Afficher le résultat
oracle.afficher_resultat()

# Générer les fichiers
grille = oracle.sauvegarder_grille()
pdf = oracle.generer_rapport_pdf()
audio = oracle.generer_audio_sequence()

# Ou tout générer d'un coup
fichiers = oracle.generer_tout()
```

### Accéder aux données

```python
# Hexagramme principal
print(oracle.hexagramme['numero'])      # 38
print(oracle.hexagramme['caractere'])   # 睽
print(oracle.hexagramme['nom'])         # L'Opposition

# Traits
print(oracle.traits)  # [7, 6, 7, 6, 6, 7]

# Hexagramme de mutation (si traits mutants)
if oracle.hexagramme_mute:
    print(oracle.hexagramme_mute['nom'])

# Grilles (objets PIL.Image)
print(oracle.grille_principale.size)    # (595, 842)
```

---

## 📚 Référence Yi Jing

### Les 64 Hexagrammes

Consultez le fichier `HEXAGRAMMES.md` pour la liste complète des 64 hexagrammes avec leurs significations.

### Méthode des 3 Pièces

1. Lancer 3 pièces simultanément
2. Face = 3, Pile = 2
3. Total possible : 6, 7, 8, ou 9
4. Répéter 6 fois (du bas vers le haut)

| Total | Trait | Type |
|-------|-------|------|
| 6 (2+2+2) | ━ ✕ ━ | Yin mutant |
| 7 (2+2+3) | ━━━━━ | Yang stable |
| 8 (2+3+3) | ━   ━ | Yin stable |
| 9 (3+3+3) | ━━◯━━ | Yang mutant |

---

## 🙏 Crédits

- **Grilles "La Livrée d'Hermès"** : Anibal Edelbert Amiot
- **Développement** : CyberMind.FR
- **Textes Yi Jing** : Basés sur la traduction de Richard Wilhelm

---

## 📜 Licence

MIT License - Voir le fichier [LICENSE](LICENSE)

---

## 🔗 Liens

- [CyberMind.FR](https://cybermind.fr)
- [Yi Jing sur Wikipedia](https://fr.wikipedia.org/wiki/Yi_Jing)
- [Solfège ancien](https://fr.wikipedia.org/wiki/Solfège_sacré)

---

*易經 - Le changement est la seule constante de l'univers*
