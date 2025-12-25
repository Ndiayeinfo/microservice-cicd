# ⚡ Guide Rapide - Déploiement CloudTaskHub sur GCP

**Pour les utilisateurs expérimentés qui veulent un rappel rapide**

## 🚀 Checklist Rapide

### 1. GCP Setup (15 min)
- [ ] Créer un projet GCP
- [ ] Activer Compute Engine API
- [ ] Créer une VM `e2-standard-2` (2 vCPU, 8 Go RAM) avec Ubuntu 22.04
- [ ] Ouvrir les ports : 22, 80, 443, 8080, 9090, 3000, 16686
- [ ] Noter l'IP externe de la VM

### 2. VM Configuration (10 min)
```bash
# Mise à jour
sudo apt update && sudo apt upgrade -y

# Installer Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker

# Initialiser Swarm
docker swarm init

# Créer les réseaux
docker network create --driver=overlay traefik-public
docker network create --driver=overlay internal

# Préparer les répertoires
sudo mkdir -p /opt/cloudtaskhub /var/data/traefik
sudo chown -R $USER:$USER /opt/cloudtaskhub /var/data/traefik
```

### 3. GitHub Secrets (5 min)
Créer dans GitHub > Settings > Secrets :
- `DOCKERHUB_USERNAME` : Votre username Docker Hub
- `DOCKERHUB_TOKEN` : Token Docker Hub (Read & Write)
- `SERVER_HOST` : IP externe de la VM GCP
- `SERVER_USER` : Utilisateur SSH (ex: `ubuntu`)
- `SERVER_SSH_KEY` : Clé privée SSH (générée avec `ssh-keygen -t ed25519 -f ~/.ssh/cloudtaskhub_deploy`)

### 4. SSH Key Setup (5 min)
```bash
# Générer la clé
ssh-keygen -t ed25519 -f ~/.ssh/cloudtaskhub_deploy

# Copier sur la VM
ssh-copy-id -i ~/.ssh/cloudtaskhub_deploy.pub USER@VM_IP

# Tester
ssh -i ~/.ssh/cloudtaskhub_deploy USER@VM_IP

# Ajouter la clé privée dans GitHub secret SERVER_SSH_KEY
cat ~/.ssh/cloudtaskhub_deploy
```

### 5. Premier Déploiement (5 min)
```bash
# Push sur main déclenche automatiquement :
# 1. CI - Main Build & Push (build les images)
# 2. CD - Deploy Production (déploie sur la VM)

git add .
git commit -m "Initial deployment"
git push origin main
```

### 6. Vérification (2 min)
```bash
# Sur la VM
docker service ls
docker service logs cloudtaskhub_gateway-service -f

# Tester
curl http://VM_IP/
curl http://VM_IP/health
```

## 🔗 URLs d'Accès

- **Gateway** : `http://VM_IP/`
- **Traefik Dashboard** : `http://VM_IP:8080/dashboard/`
- **Prometheus** : `http://VM_IP:9090`
- **Grafana** : `http://VM_IP:3000` (admin/admin)
- **Jaeger** : `http://VM_IP:16686`

## 🛠️ Commandes Utiles

```bash
# Voir les services
docker service ls
docker stack ps cloudtaskhub

# Logs
docker service logs -f cloudtaskhub_gateway-service

# Redémarrer un service
docker service update --force cloudtaskhub_gateway-service

# Supprimer la stack
docker stack rm cloudtaskhub

# Nettoyer
docker system prune -af
```

## ⚠️ Problèmes Courants

**Services ne démarrent pas** :
```bash
docker service ps cloudtaskhub_gateway-service --no-trunc
docker service logs cloudtaskhub_gateway-service
```

**Erreur SSH GitHub Actions** :
- Vérifier que la clé privée est complète dans le secret
- Tester la connexion manuellement

**Images introuvables** :
- Vérifier que `DOCKERHUB_USERNAME` est correct
- Vérifier que les images existent sur Docker Hub

## 📖 Tutoriel Complet

Pour les débutants, voir : [tutoriel-complet-gcp.md](./tutoriel-complet-gcp.md)

