# 易經 Yi Jing Oracle - Streamlit App

Application web de consultation du Yi Jing avec visualisation sur grilles "La Livrée d'Hermès" et fréquences sacrées.

## 🌐 Démo en ligne

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://yijing-oracle.streamlit.app)

## 🚀 Déploiement sur Streamlit Cloud

### Méthode 1 : Depuis GitHub

1. **Fork ou créez un repo GitHub** avec ces fichiers :
   ```
   yijing-oracle/
   ├── app.py
   ├── requirements.txt
   ├── .streamlit/
   │   └── config.toml
   ├── images/
   │   ├── lldh-YY-YANG-1.png
   │   ├── lldh-YY-YANG-2.png
   │   └── ... (24 fichiers PNG)
   └── README.md
   ```

2. **Allez sur** [share.streamlit.io](https://share.streamlit.io)

3. **Connectez votre compte GitHub**

4. **Déployez** :
   - Repository : `votre-username/yijing-oracle`
   - Branch : `main`
   - Main file path : `app.py`

5. **Cliquez "Deploy!"**

### Méthode 2 : Exécution locale

```bash
# Cloner le projet
git clone https://github.com/votre-username/yijing-oracle.git
cd yijing-oracle

# Créer environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou: venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run app.py
```

L'application s'ouvre sur `http://localhost:8501`

## 📁 Structure des fichiers

| Fichier | Description |
|---------|-------------|
| `app.py` | Application Streamlit principale |
| `requirements.txt` | Dépendances Python |
| `.streamlit/config.toml` | Configuration thème et serveur |
| `images/` | 24 grilles PNG La Livrée d'Hermès |

## ✨ Fonctionnalités

- 🎲 **Tirage aléatoire** : Simulation des 3 pièces
- ✏️ **Saisie manuelle** : Entrer ses propres traits
- 🎮 **Grilles visuelles** : Superposition colorée des 6 couches
- 🔄 **Mutations** : Calcul et affichage de l'hexagramme muté
- 🎵 **Audio** : Génération de séquences sonores (Solfège 432 Hz)
- 📄 **Export PDF** : Rapport complet téléchargeable
- 📱 **Responsive** : Fonctionne sur mobile et desktop

## 🎨 Les 24 Grilles

Les fichiers images doivent être nommés :
- `lldh-YY-YANG-1.png` à `lldh-YY-YANG-6.png` (Yang stable)
- `lldh-YY-YING-1.png` à `lldh-YY-YING-6.png` (Yin stable)
- `lldh-YY-YANG-MUT-1.png` à `lldh-YY-YANG-MUT-6.png` (Yang mutant)
- `lldh-YY-YING-MUT-1.png` à `lldh-YY-YING-MUT-6.png` (Yin mutant)

## 🎵 Fréquences Sacrées

| Trigramme | Fréquence | Bienfait |
|-----------|-----------|----------|
| ☰ Ciel | 852 Hz | Éveil spirituel |
| ☷ Terre | 396 Hz | Libération |
| ☳ Tonnerre | 417 Hz | Transformation |
| ☵ Eau | 528 Hz | Réparation ADN |
| ☶ Montagne | 639 Hz | Connexion |
| ☴ Vent | 741 Hz | Expression |
| ☲ Feu | 963 Hz | Transcendance |
| ☱ Lac | 432 Hz | Harmonie universelle |

## 📝 Configuration Streamlit Cloud

Pour personnaliser le thème, modifiez `.streamlit/config.toml` :

```toml
[theme]
primaryColor = "#8B4513"      # Marron (boutons)
backgroundColor = "#FFFAF0"   # Crème (fond)
secondaryBackgroundColor = "#FFF8DC"
textColor = "#5D4037"         # Marron foncé
```

## 🔒 Secrets (optionnel)

Si vous avez besoin de clés API, créez `.streamlit/secrets.toml` :

```toml
[api]
key = "votre-clé-secrète"
```

⚠️ Ne commitez jamais ce fichier ! Utilisez les secrets Streamlit Cloud.

## 📜 Licence

MIT License

## 🙏 Crédits

- **Grilles "La Livrée d'Hermès"** : Anibal Edelbert Amiot
- **Développement** : CyberMind.FR
- **Framework** : [Streamlit](https://streamlit.io)

---

*易經 - Le changement est la seule constante de l'univers*
