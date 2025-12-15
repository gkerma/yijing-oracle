# 易經 Yi Jing Oracle v2.2 - Streamlit App

Application web complète de consultation du Yi Jing avec animations, textes complets et méditation Kasina.

## ✨ Nouveautés v2.2

### 🎮 Animation entre les grilles
- Transition fluide hexagramme principal ↔ mutation
- Boutons de navigation interactifs
- Mode animation automatique (2 secondes)

### 📜 Textes complets
- **Description** de l'hexagramme
- **Le Jugement** (texte traditionnel)
- **L'Image** (conseil pratique)
- **Les 6 traits** avec textes individuels
- **Traits mutants** mis en évidence

### 📄 PDF détaillé (3-5 pages)
- Page 1 : Hexagramme principal, trigrammes, grille
- Page 2 : Jugement, Image, interprétation générale
- Page 3 : Les 6 traits avec textes complets
- Page 4 : Traits mutants (si présents)
- Page 5 : Hexagramme de mutation (si applicable)

### 🧘 Méditation Kasina KBS
- Format officiel Mindplace
- Audio binaural stéréo

## 🚀 Installation

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📁 Structure

```
├── app.py                    # Application Streamlit (1500+ lignes)
├── yijing_complet.json       # 64 hexagrammes complets
├── requirements.txt
├── .streamlit/config.toml
└── images/                   # 24 grilles PNG
```

## 📦 Exports disponibles

| Export | Format | Contenu |
|--------|--------|---------|
| Audio tirage | WAV | Fréquences sacrées 432 Hz |
| Rapport PDF | PDF | 3-5 pages détaillées |
| Session Kasina | KBS | Format Mindplace |
| Audio binaural | WAV | Battements binauraux |
| Grilles | PNG | Images haute qualité |

## 📝 Crédits

- **Grilles** : Anibal Edelbert Amiot
- **Développement** : CyberMind.FR
- **Format KBS** : Mindplace
