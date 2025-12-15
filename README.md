# 易經 Yi Jing Oracle v2.2 - Streamlit App

Application web de consultation du Yi Jing avec animations, textes complets et méditation Kasina.

## 🚀 Installation

```bash
# 1. Extraire le ZIP
unzip yijing-streamlit-v2.2.zip
cd yijing-streamlit-v2.2

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer l'application
streamlit run app.py
```

## 📁 Structure

```
yijing-streamlit-v2.2/
├── app.py                    # Application Streamlit
├── yijing_complet.json       # Base de données 64 hexagrammes
├── requirements.txt
├── .streamlit/config.toml
├── fonts/
│   └── ipag.ttf              # Police japonaise IPA Gothic (CJK)
└── images/                   # 24 grilles PNG
```

## ⚠️ Police CJK embarquée

La police **IPA Gothic** (`fonts/ipag.ttf`) est incluse dans le projet pour afficher les caractères chinois dans les PDF. Elle est automatiquement utilisée par l'application.

Si les caractères ne s'affichent pas, vérifiez que :
1. Le dossier `fonts/` existe avec `ipag.ttf` à l'intérieur
2. Le fichier fait environ 6 MB

## ✨ Fonctionnalités v2.2

- 🎮 **Animation des grilles** : Transition hexagramme ↔ mutation
- 📜 **Textes complets** : Jugement, Image, 6 traits
- 📄 **PDF détaillé** : 3-5 pages avec caractères chinois
- 🎵 **Audio** : Fréquences sacrées 432 Hz
- 🧘 **Kasina KBS** : Méditation AVS Mindplace

## 📝 Crédits

- **Grilles** : Anibal Edelbert Amiot "La Livrée d'Hermès"
- **Police CJK** : IPA Gothic (IPA フォント)
- **Développement** : CyberMind.FR
