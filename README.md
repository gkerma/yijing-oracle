# 易經 Yi Jing Oracle v2.1 - Streamlit App

Application web de consultation du Yi Jing avec méditation **Kasina KBS** (Mindplace).

## 🧘 Méditation Kasina / AVS

Génère des sessions au format **KBS (Kasina Basic Session)** officiel Mindplace :

- **Fichier .kbs** : Format natif pour Kasina/Limina
- **Audio WAV binaural** : Battements binauraux stéréo (casque requis)

### Structure de la méditation (5 min)

| Phase | Durée | État | Fréquence |
|-------|-------|------|-----------|
| Ancrage | 1 min | Alpha 10 Hz | 432 Hz |
| Trigramme Bas | 1.5 min | Theta 7 Hz | Variable |
| Trigramme Haut | 1.5 min | Theta 5 Hz | Variable |
| Intégration | 1 min | Alpha 8 Hz | 528 Hz |

### Paramètres KBS

- `ColorControlMode=3` : RGB personnalisé par segment
- `SAMDpth=0` : Binaural pur (pas d'isochronique)
- `LgtModWF=Sine` : Onde sinusoïdale pour relaxation
- Couleurs basées sur les trigrammes et principes AVS

## 🚀 Déploiement

### Streamlit Cloud

1. Push vers GitHub
2. Connecter sur [share.streamlit.io](https://share.streamlit.io)
3. Déployer avec `app.py` comme fichier principal

### Local

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📁 Structure

```
├── app.py                    # Application Streamlit
├── yijing_complet.json       # 64 hexagrammes
├── requirements.txt
├── .streamlit/config.toml
└── images/                   # 24 grilles PNG
```

## ✨ Fonctionnalités

- 🎲 Tirage aléatoire ou manuel
- 📜 Textes traditionnels complets
- 🎮 Grilles La Livrée d'Hermès (couleurs préservées)
- 📄 PDF avec caractères chinois
- 🎵 Audio 432 Hz
- 🧘 **Session Kasina KBS** avec battements binauraux

## 📚 Références

- Documentation KBS v2 Mindplace
- AVS Technology (Ayrmetes Advanced Cognitive Technologies)
- Frequency Following Response (FFR)

## 📝 Crédits

- **Grilles** : Anibal Edelbert Amiot
- **Développement** : CyberMind.FR
- **Format KBS** : Mindplace
