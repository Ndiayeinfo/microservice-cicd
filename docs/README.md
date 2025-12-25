# 📚 Documentation CloudTaskHub

Bienvenue dans la documentation de CloudTaskHub ! Cette section contient tous les guides nécessaires pour déployer et comprendre le projet.

## 🎓 Guides de Déploiement

### Pour les Débutants

**[📘 Tutoriel Complet GCP](./tutoriel-complet-gcp.md)** ⭐ **RECOMMANDÉ**

Un guide exhaustif et détaillé pour déployer CloudTaskHub sur Google Cloud Platform (GCE) :
- ✅ Explications pas à pas de chaque concept
- ✅ Création de la VM GCP avec toutes les configurations
- ✅ Installation complète de Docker et Docker Swarm
- ✅ Configuration GitHub Actions de A à Z
- ✅ Dépannage et solutions aux problèmes courants
- ✅ Durée estimée : 24 heures

**Parfait pour** : Débutants qui veulent comprendre chaque étape en profondeur.

### Pour les Utilisateurs Expérimentés

**[⚡ Guide Rapide GCP](./guide-rapide-gcp.md)**

Une checklist rapide et des commandes essentielles pour un déploiement rapide :
- Checklist en 5 étapes
- Commandes essentielles
- URLs d'accès
- Dépannage rapide

**Parfait pour** : Utilisateurs qui connaissent déjà Docker et GCP.

### Spécifications Techniques

**[💻 Spécifications VM GCP](./specifications-vm-gcp.md)**

Détails complets sur les caractéristiques de la machine virtuelle :
- Configurations recommandées (standard, économique, production)
- Répartition des ressources par service
- Stratégies de scaling
- Optimisation des coûts
- Commandes de monitoring

## 🔧 Configuration

### GitHub Actions

**[🔐 Configuration GitHub Secrets](./github-secrets.md)**

Guide complet pour configurer tous les secrets nécessaires à la CI/CD :
- Liste des secrets requis
- Génération des tokens Docker Hub
- Configuration des clés SSH
- Setup des webhooks Slack
- Vérification de la configuration

### Setup Serveur

**[📄 Setup VPS Générique](./setup-vps.md)**

Guide pour configurer un serveur VPS (DigitalOcean, AWS EC2, etc.) :
- Installation de Docker
- Configuration de Docker Swarm
- Préparation des réseaux
- Configuration SSH
- Sécurité (firewall, fail2ban)

## 📖 Structure de la Documentation

```
docs/
├── README.md                    # Ce fichier (index)
├── tutoriel-complet-gcp.md      # Tutoriel détaillé GCP (débutants)
├── guide-rapide-gcp.md          # Guide rapide GCP (expérimentés)
├── specifications-vm-gcp.md     # Spécifications techniques VM
├── github-secrets.md            # Configuration GitHub Actions
└── setup-vps.md                 # Setup serveur générique
```

## 🚀 Par Où Commencer ?

### Si vous êtes débutant :

1. **Lisez** [Tutoriel Complet GCP](./tutoriel-complet-gcp.md) de A à Z
2. **Consultez** [Spécifications VM GCP](./specifications-vm-gcp.md) pour choisir votre configuration
3. **Suivez** [Configuration GitHub Secrets](./github-secrets.md) pour setup la CI/CD
4. **Référez-vous** à [Setup VPS](./setup-vps.md) pour les détails techniques

### Si vous êtes expérimenté :

1. **Consultez** [Guide Rapide GCP](./guide-rapide-gcp.md) pour la checklist
2. **Référez-vous** à [Configuration GitHub Secrets](./github-secrets.md) si besoin
3. **Vérifiez** [Spécifications VM GCP](./specifications-vm-gcp.md) pour les ressources

## ❓ Besoin d'Aide ?

### Problèmes Courants

Consultez la section **"Dépannage et Solutions"** dans le [Tutoriel Complet GCP](./tutoriel-complet-gcp.md).

### Questions Spécifiques

- **Docker** : Voir [Setup VPS](./setup-vps.md) section Docker
- **GitHub Actions** : Voir [Configuration GitHub Secrets](./github-secrets.md)
- **Ressources VM** : Voir [Spécifications VM GCP](./specifications-vm-gcp.md)

## 📝 Contribution

Si vous trouvez des erreurs ou souhaitez améliorer la documentation :

1. Ouvrez une issue sur GitHub
2. Ou créez une Pull Request avec vos améliorations

---

**Bon déploiement ! 🚀**

