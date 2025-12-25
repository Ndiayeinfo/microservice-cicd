# 🎓 Tutoriel Complet : Déploiement CloudTaskHub sur Google Cloud Platform (GCE)

**Durée estimée : 24 heures**  
**Niveau : Débutant**  
**Objectif : Déployer une architecture microservices complète avec CI/CD**

---

## 📋 Table des Matières

1. [Introduction et Prérequis](#1-introduction-et-prérequis)
2. [Création de la Machine Virtuelle sur GCP](#2-création-de-la-machine-virtuelle-sur-gcp)
3. [Configuration Initiale de la VM](#3-configuration-initiale-de-la-vm)
4. [Installation de Docker et Docker Swarm](#4-installation-de-docker-et-docker-swarm)
5. [Configuration du Projet Local](#5-configuration-du-projet-local)
6. [Configuration de GitHub Actions](#6-configuration-de-github-actions)
7. [Premier Déploiement](#7-premier-déploiement)
8. [Tests et Vérifications](#8-tests-et-vérifications)
9. [Monitoring et Observabilité](#9-monitoring-et-observabilité)
10. [Dépannage et Solutions](#10-dépannage-et-solutions)

---

## 1. Introduction et Prérequis

### 🎯 Ce que vous allez apprendre

Ce tutoriel vous guidera pas à pas pour :
- Créer une machine virtuelle sur Google Cloud Platform (GCE)
- Installer et configurer Docker Swarm
- Configurer un pipeline CI/CD complet avec GitHub Actions
- Déployer 6 microservices avec observabilité (tracing, métriques, logs)
- Utiliser Traefik comme reverse proxy
- Monitorer votre infrastructure avec Prometheus et Grafana

### 📦 Prérequis

Avant de commencer, vous devez avoir :

1. **Un compte Google Cloud Platform (GCP)**
   - Si vous n'en avez pas : https://cloud.google.com/
   - Google offre $300 de crédit gratuit pour les nouveaux comptes

2. **Un compte GitHub**
   - Si vous n'en avez pas : https://github.com/

3. **Un compte Docker Hub**
   - Si vous n'en avez pas : https://hub.docker.com/

4. **Git installé sur votre machine locale**
   - Windows : https://git-scm.com/download/win
   - Mac : `brew install git`
   - Linux : `sudo apt install git` (Ubuntu/Debian)

5. **Un éditeur de texte** (VS Code recommandé)

6. **Un client SSH** (déjà inclus sur Mac/Linux, utiliser PuTTY ou Git Bash sur Windows)

### 💰 Estimation des Coûts

Pour ce projet, vous utiliserez :
- **Machine GCE** : ~$15-30/mois (selon utilisation)
- **Bande passante** : Gratuite jusqu'à 1 To/mois
- **Stockage** : ~$2-5/mois pour 20 Go

**Total estimé : ~$20-35/mois** (mais vous pouvez arrêter la VM quand vous n'en avez pas besoin)

---

## 2. Création de la Machine Virtuelle sur GCP

### 2.1. Créer un Projet GCP

1. **Connectez-vous à Google Cloud Console**
   - Allez sur : https://console.cloud.google.com/
   - Connectez-vous avec votre compte Google

2. **Créer un nouveau projet**
   - Cliquez sur le sélecteur de projet en haut (à côté de "Google Cloud")
   - Cliquez sur "Nouveau projet"
   - Nom : `cloudtaskhub` (ou un nom de votre choix)
   - ID du projet : sera généré automatiquement
   - Cliquez sur "Créer"

3. **Activer la facturation**
   - GCP vous demandera d'activer la facturation
   - Suivez les instructions (nécessite une carte bancaire, mais vous avez $300 de crédit gratuit)

### 2.2. Activer l'API Compute Engine

1. Dans la console GCP, allez dans **"APIs & Services" > "Library"**
2. Recherchez "Compute Engine API"
3. Cliquez sur "Enable" (Activer)

### 2.3. Créer la Machine Virtuelle

#### Caractéristiques Recommandées

Pour ce projet, nous recommandons :

- **Type de machine** : `e2-standard-2`
  - **CPU** : 2 vCPU
  - **RAM** : 8 Go
  - **Coût** : ~$0.067/heure (~$48/mois si 24/7)
  
  **Alternative économique** (pour tests) : `e2-standard-1`
  - **CPU** : 1 vCPU
  - **RAM** : 4 Go
  - **Coût** : ~$0.033/heure (~$24/mois si 24/7)

- **Système d'exploitation** : Ubuntu 22.04 LTS
- **Disque** : 30 Go SSD (Standard Persistent Disk)
- **Région** : Choisissez la région la plus proche de vous (ex: `europe-west1` pour l'Europe)

> 📖 **Pour plus de détails** : Voir [Spécifications VM GCP](./specifications-vm-gcp.md) pour une analyse complète des ressources et des coûts.

#### Étapes de Création

1. **Accéder à Compute Engine**
   - Dans le menu latéral, allez dans **"Compute Engine" > "VM instances"**
   - Cliquez sur "CREATE INSTANCE" (Créer une instance)

2. **Configuration de Base**
   - **Name** : `cloudtaskhub-vm` (ou un nom de votre choix)
   - **Region** : Choisissez une région proche (ex: `europe-west1-b`)
   - **Zone** : Laissez la zone par défaut

3. **Machine Configuration**
   - **Machine family** : General-purpose
   - **Series** : E2
   - **Machine type** : `e2-standard-2` (2 vCPU, 8 Go RAM)
   
   > 💡 **Explication** : E2 est une série économique. Pour un projet de production réel, vous pourriez utiliser N1 ou N2, mais E2 est parfait pour apprendre.

4. **Boot Disk**
   - Cliquez sur "Change" (Modifier)
   - **Operating System** : Ubuntu
   - **Version** : Ubuntu 22.04 LTS
   - **Boot disk type** : Standard persistent disk
   - **Size** : 30 GB (augmentez si nécessaire)
   - Cliquez sur "Select"

5. **Firewall**
   - Cochez **"Allow HTTP traffic"**
   - Cochez **"Allow HTTPS traffic"**
   
   > ⚠️ **Important** : Ces options ouvrent les ports 80 et 443. Nous ouvrirons d'autres ports manuellement plus tard.

6. **Cliquez sur "CREATE"** (Créer)

   La VM va prendre 1-2 minutes à démarrer.

### 2.4. Configurer le Pare-feu GCP

Nous devons ouvrir les ports nécessaires pour les services :

1. **Aller dans "VPC network" > "Firewall"**
2. **Cliquer sur "CREATE FIREWALL RULE"**

Créer les règles suivantes :

#### Règle 1 : SSH (déjà existante normalement)
- **Name** : `allow-ssh`
- **Direction** : Ingress
- **Targets** : All instances in the network
- **Source IP ranges** : `0.0.0.0/0` (ou votre IP pour plus de sécurité)
- **Protocols and ports** : TCP:22
- **Create**

#### Règle 2 : Traefik HTTP
- **Name** : `allow-traefik-http`
- **Direction** : Ingress
- **Targets** : All instances in the network
- **Source IP ranges** : `0.0.0.0/0`
- **Protocols and ports** : TCP:80
- **Create**

#### Règle 3 : Traefik Dashboard
- **Name** : `allow-traefik-dashboard`
- **Direction** : Ingress
- **Targets** : All instances in the network
- **Source IP ranges** : `0.0.0.0/0`
- **Protocols and ports** : TCP:8080
- **Create**

#### Règle 4 : Prometheus
- **Name** : `allow-prometheus`
- **Direction** : Ingress
- **Targets** : All instances in the network
- **Source IP ranges** : `0.0.0.0/0`
- **Protocols and ports** : TCP:9090
- **Create**

#### Règle 5 : Grafana
- **Name** : `allow-grafana`
- **Direction** : Ingress
- **Targets** : All instances in the network
- **Source IP ranges** : `0.0.0.0/0`
- **Protocols and ports** : TCP:3000
- **Create**

#### Règle 6 : Jaeger
- **Name** : `allow-jaeger`
- **Direction** : Ingress
- **Targets** : All instances in the network
- **Source IP ranges** : `0.0.0.0/0`
- **Protocols and ports** : TCP:16686
- **Create**

> 🔒 **Sécurité** : Pour un environnement de production, vous devriez restreindre les IP sources au lieu de `0.0.0.0/0`. Mais pour apprendre, c'est acceptable.

### 2.5. Obtenir l'Adresse IP de la VM

1. Retournez dans **"Compute Engine" > "VM instances"**
2. Notez l'**External IP** de votre VM (ex: `34.123.45.67`)
3. Cette IP sera utilisée pour :
   - Se connecter en SSH
   - Accéder aux services déployés
   - Configurer GitHub Actions

> 💡 **IP Statique** : Par défaut, l'IP externe change si vous arrêtez/redémarrez la VM. Pour une IP fixe :
> - Cliquez sur votre VM
> - Allez dans "Networking"
> - Cliquez sur "External IP" > "Reserve static address"
> - Donnez un nom et réservez

---

## 3. Configuration Initiale de la VM

### 3.1. Se Connecter en SSH

#### Option A : Via la Console GCP (Recommandé pour débutants)

1. Dans **"Compute Engine" > "VM instances"**
2. Cliquez sur **"SSH"** à côté de votre VM
3. Une fenêtre de terminal s'ouvre dans votre navigateur

#### Option B : Via SSH depuis votre Machine Locale

**Sur Windows (PowerShell ou Git Bash) :**
```bash
ssh -i ~/.ssh/gcp_key USERNAME@EXTERNAL_IP
```

**Sur Mac/Linux :**
```bash
ssh USERNAME@EXTERNAL_IP
```

> 💡 **Note** : L'utilisateur par défaut sur Ubuntu GCE est généralement votre email Google ou `ubuntu`.

### 3.2. Mise à Jour du Système

Une fois connecté, exécutez :

```bash
# Mettre à jour la liste des paquets
sudo apt update

# Mettre à jour tous les paquets installés
sudo apt upgrade -y

# Installer les outils de base
sudo apt install -y ca-certificates curl gnupg lsb-release wget git
```

> 📚 **Explication** :
> - `apt update` : Met à jour la liste des paquets disponibles
> - `apt upgrade` : Met à jour les paquets déjà installés
> - `-y` : Répond automatiquement "oui" aux questions

### 3.3. Créer un Utilisateur pour le Déploiement (Optionnel mais Recommandé)

Pour des raisons de sécurité, créons un utilisateur dédié :

```bash
# Créer un nouvel utilisateur
sudo adduser cloudtaskhub

# Ajouter l'utilisateur au groupe sudo (pour les commandes admin)
sudo usermod -aG sudo cloudtaskhub

# Ajouter l'utilisateur au groupe docker (nous l'ajouterons après l'installation de Docker)
# sudo usermod -aG docker cloudtaskhub

# Passer à cet utilisateur
sudo su - cloudtaskhub
```

> 💡 **Note** : Vous pouvez aussi utiliser votre utilisateur actuel. L'important est d'avoir les droits sudo.

### 3.4. Installer Git (si pas déjà installé)

```bash
sudo apt install -y git
git --version
```

---

## 4. Installation de Docker et Docker Swarm

### 4.1. Comprendre Docker et Docker Swarm

**Docker** : Permet de créer des "conteneurs" qui isolent les applications et leurs dépendances.

**Docker Swarm** : Mode natif de Docker pour orchestrer plusieurs conteneurs sur une ou plusieurs machines (clustering).

> 📚 **Analogie** : Imaginez Docker comme des boîtes qui contiennent vos applications, et Docker Swarm comme un chef d'orchestre qui gère toutes ces boîtes.

### 4.2. Installation de Docker

#### Étape 1 : Ajouter la Clé GPG Docker

```bash
# Créer le répertoire pour les clés
sudo install -m 0755 -d /etc/apt/keyrings

# Télécharger et ajouter la clé GPG Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Donner les permissions de lecture
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

> 📚 **Explication** : GPG (GNU Privacy Guard) est utilisé pour vérifier l'authenticité des paquets. La clé GPG garantit que les paquets Docker proviennent bien de Docker Inc.

#### Étape 2 : Ajouter le Dépôt Docker

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

> 📚 **Explication** : Cette commande ajoute le dépôt officiel Docker à la liste des sources de paquets Ubuntu.

#### Étape 3 : Mettre à Jour et Installer Docker

```bash
# Mettre à jour la liste des paquets (incluant le nouveau dépôt Docker)
sudo apt update

# Installer Docker Engine, CLI, Containerd, et Docker Compose Plugin
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

> 📚 **Explication** :
> - `docker-ce` : Docker Community Edition (version gratuite)
> - `docker-ce-cli` : Interface en ligne de commande
> - `containerd` : Runtime de conteneurs
> - `docker-compose-plugin` : Plugin pour Docker Compose

#### Étape 4 : Vérifier l'Installation

```bash
# Vérifier la version de Docker
docker --version

# Vérifier la version de Docker Compose
docker compose version

# Tester Docker avec un conteneur Hello World
sudo docker run hello-world
```

Si vous voyez "Hello from Docker!", Docker est correctement installé ! 🎉

### 4.3. Configurer Docker pour l'Utilisateur

Par défaut, Docker nécessite `sudo`. Pour éviter de taper `sudo` à chaque fois :

```bash
# Ajouter votre utilisateur au groupe docker
sudo usermod -aG docker $USER

# Appliquer les changements (déconnexion/reconnexion nécessaire)
newgrp docker

# Tester sans sudo
docker run hello-world
```

> ⚠️ **Important** : Si `newgrp docker` ne fonctionne pas, déconnectez-vous et reconnectez-vous en SSH.

### 4.4. Activer Docker au Démarrage

```bash
# Activer Docker pour qu'il démarre automatiquement au boot
sudo systemctl enable docker

# Démarrer Docker maintenant
sudo systemctl start docker

# Vérifier le statut
sudo systemctl status docker
```

### 4.5. Initialiser Docker Swarm

Docker Swarm permet de gérer plusieurs conteneurs comme un seul système.

```bash
# Initialiser Docker Swarm
docker swarm init
```

Vous devriez voir quelque chose comme :
```
Swarm initialized: current node (xxxxx) is now a manager.

To add a worker node to this swarm, run the following command:
    docker swarm join --token SWMTKN-1-xxxxx...
```

> 📚 **Explication** : 
> - `docker swarm init` transforme votre machine en "manager" (chef d'orchestre)
> - Un token est généré pour ajouter d'autres machines (workers) au cluster
> - Pour ce tutoriel, une seule machine suffit

**Notez le token** (vous en aurez besoin si vous ajoutez d'autres machines plus tard).

### 4.6. Créer les Réseaux Docker Overlay

Les réseaux overlay permettent aux conteneurs de communiquer entre eux, même s'ils sont sur différentes machines.

```bash
# Créer le réseau pour Traefik (reverse proxy)
docker network create --driver=overlay traefik-public

# Créer le réseau interne pour les microservices
docker network create --driver=overlay internal
```

> 📚 **Explication** :
> - `traefik-public` : Réseau pour Traefik et les services exposés publiquement
> - `internal` : Réseau privé pour la communication entre microservices

Vérifier que les réseaux sont créés :
```bash
docker network ls
```

Vous devriez voir `traefik-public` et `internal` avec le type `overlay`.

### 4.7. Préparer les Répertoires

```bash
# Créer le répertoire pour le projet
sudo mkdir -p /opt/cloudtaskhub
sudo mkdir -p /var/data/traefik

# Donner les permissions à votre utilisateur
sudo chown -R $USER:$USER /opt/cloudtaskhub
sudo chown -R $USER:$USER /var/data/traefik

# Créer le fichier acme.json pour les certificats HTTPS (optionnel pour l'instant)
touch /var/data/traefik/acme.json
chmod 600 /var/data/traefik/acme.json
```

> 📚 **Explication** :
> - `/opt/cloudtaskhub` : Contiendra le code du projet
> - `/var/data/traefik` : Contiendra les certificats SSL/TLS
> - `chmod 600` : Donne uniquement les droits de lecture/écriture au propriétaire (sécurité)

---

## 5. Configuration du Projet Local

### 5.1. Cloner le Projet

Sur votre **machine locale** (pas sur la VM) :

```bash
# Aller dans un répertoire de travail
cd ~/Desktop  # ou cd ~/Documents selon votre préférence

# Cloner le projet (remplacez par l'URL de votre repo GitHub)
git clone https://github.com/VOTRE_USERNAME/microservice-cicd.git

# Entrer dans le projet
cd microservice-cicd
```

> 💡 **Note** : Si vous n'avez pas encore poussé le projet sur GitHub, créez d'abord un nouveau repository sur GitHub, puis :
> ```bash
# Initialiser git (si pas déjà fait)
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/VOTRE_USERNAME/microservice-cicd.git
git push -u origin main
```

### 5.2. Créer un Compte Docker Hub

1. Allez sur https://hub.docker.com/
2. Créez un compte (gratuit)
3. Notez votre **username** (ex: `monusername`)

### 5.3. Créer un Token d'Accès Docker Hub

1. Sur Docker Hub, allez dans **Account Settings > Security**
2. Cliquez sur **"New Access Token"**
3. Donnez un nom : `cloudtaskhub-ci`
4. Permissions : **Read & Write**
5. Cliquez sur **Generate**
6. **⚠️ COPIEZ LE TOKEN IMMÉDIATEMENT** (il ne sera plus visible après)

### 5.4. Tester le Build Local (Optionnel mais Recommandé)

Avant de déployer, testons que tout fonctionne localement :

```bash
# Dans le répertoire du projet
cd microservice-cicd

# Installer Python et pip (si pas déjà fait)
# Windows : Téléchargez depuis python.org
# Mac : brew install python3
# Linux : sudo apt install python3 python3-pip

# Installer les dépendances Python
pip install -r requirements.txt

# Tester un build Docker d'un service
cd services/gateway
docker build -t test-gateway:latest .
```

Si le build réussit, vous êtes prêt ! 🎉

---

## 6. Configuration de GitHub Actions

### 6.1. Créer les Secrets GitHub

Les secrets permettent à GitHub Actions d'accéder à vos services (Docker Hub, VM GCP) de manière sécurisée.

1. **Aller sur votre repository GitHub**
2. **Settings > Secrets and variables > Actions**
3. **Cliquer sur "New repository secret"**

Créer les secrets suivants :

#### Secret 1 : `DOCKERHUB_USERNAME`
- **Name** : `DOCKERHUB_USERNAME`
- **Value** : Votre username Docker Hub (ex: `monusername`)
- **Add secret**

#### Secret 2 : `DOCKERHUB_TOKEN`
- **Name** : `DOCKERHUB_TOKEN`
- **Value** : Le token Docker Hub que vous avez créé à l'étape 5.3
- **Add secret**

#### Secret 3 : `SERVER_HOST`
- **Name** : `SERVER_HOST`
- **Value** : L'adresse IP externe de votre VM GCP (ex: `34.123.45.67`)
- **Add secret**

#### Secret 4 : `SERVER_USER`
- **Name** : `SERVER_USER`
- **Value** : Votre utilisateur SSH sur la VM (ex: `ubuntu` ou votre email Google)
- **Add secret**

> 💡 **Comment trouver SERVER_USER** : Connectez-vous en SSH et regardez le prompt. Si vous voyez `ubuntu@vm-name`, alors `SERVER_USER=ubuntu`.

#### Secret 5 : `SERVER_SSH_KEY`

C'est la partie la plus importante. Nous devons créer une paire de clés SSH.

**Sur votre machine locale** :

> ⚠️ **IMPORTANT - Windows** : Si vous êtes sur Windows, vous devez d'abord créer le répertoire `.ssh` car il n'existe pas par défaut.

**Étape 1 : Créer le répertoire .ssh (Windows uniquement)**

Si vous êtes sur **Windows PowerShell** :

```powershell
# Créer le répertoire .ssh dans votre dossier utilisateur
New-Item -ItemType Directory -Force -Path $env:USERPROFILE\.ssh

# Vérifier que le répertoire existe
Test-Path $env:USERPROFILE\.ssh
```

Si vous êtes sur **Windows avec Git Bash** :

```bash
# Créer le répertoire .ssh
mkdir -p ~/.ssh

# Vérifier
ls -la ~/.ssh
```

**Étape 2 : Générer la paire de clés SSH**

**Sur Windows PowerShell** :

```powershell
# Générer la paire de clés SSH
ssh-keygen -t ed25519 -C "github-actions-cloudtaskhub" -f $env:USERPROFILE\.ssh\cloudtaskhub_deploy

# Vous serez demandé de créer un mot de passe (appuyez sur Entrée pour laisser vide, ou créez-en un)
# Appuyez sur Entrée deux fois si vous voulez laisser vide
```

**Sur Windows avec Git Bash, Mac ou Linux** :

```bash
# Générer une paire de clés SSH
ssh-keygen -t ed25519 -C "github-actions-cloudtaskhub" -f ~/.ssh/cloudtaskhub_deploy

# Vous serez demandé de créer un mot de passe (appuyez sur Entrée pour laisser vide, ou créez-en un)
# Appuyez sur Entrée deux fois si vous voulez laisser vide
```

Cela crée deux fichiers :
- **Windows** : `C:\Users\VOTRE_USERNAME\.ssh\cloudtaskhub_deploy` → **Clé privée** (à mettre dans GitHub)
- **Windows** : `C:\Users\VOTRE_USERNAME\.ssh\cloudtaskhub_deploy.pub` → **Clé publique** (à mettre sur la VM)
- **Mac/Linux** : `~/.ssh/cloudtaskhub_deploy` → **Clé privée**
- **Mac/Linux** : `~/.ssh/cloudtaskhub_deploy.pub` → **Clé publique**

**Copier la clé publique sur la VM GCP** :

**Sur Windows PowerShell** :

```powershell
# Méthode 1 : Afficher la clé publique pour la copier
Get-Content $env:USERPROFILE\.ssh\cloudtaskhub_deploy.pub

# Méthode 2 : Avec ssh-copy-id (si Git Bash est installé)
# Dans Git Bash :
# ssh-copy-id -i ~/.ssh/cloudtaskhub_deploy.pub USERNAME@EXTERNAL_IP
```

**Sur Windows avec Git Bash, Mac ou Linux** :

```bash
# Méthode 1 : Avec ssh-copy-id (si disponible)
ssh-copy-id -i ~/.ssh/cloudtaskhub_deploy.pub USERNAME@EXTERNAL_IP

# Méthode 2 : Manuellement
# 1. Afficher la clé publique
cat ~/.ssh/cloudtaskhub_deploy.pub
```

**Ensuite, manuellement (toutes plateformes)** :

1. **Copier tout le contenu** de la clé publique (commence par `ssh-ed25519...`)

2. **Se connecter à la VM GCP** :
   ```bash
   ssh USERNAME@EXTERNAL_IP
   ```

3. **Sur la VM, ajouter la clé** :
   ```bash
   mkdir -p ~/.ssh
   echo "COLLER_LA_CLE_PUBLIQUE_ICI" >> ~/.ssh/authorized_keys
   chmod 600 ~/.ssh/authorized_keys
   chmod 700 ~/.ssh
   exit  # Quitter la VM
   ```

**Tester la connexion** :

**Sur Windows PowerShell** :
```powershell
ssh -i $env:USERPROFILE\.ssh\cloudtaskhub_deploy USERNAME@EXTERNAL_IP
```

**Sur Windows avec Git Bash, Mac ou Linux** :
```bash
ssh -i ~/.ssh/cloudtaskhub_deploy USERNAME@EXTERNAL_IP
```

Si vous pouvez vous connecter sans mot de passe, c'est bon ! ✅

**Ajouter la clé privée dans GitHub** :

**Sur Windows PowerShell** :
```powershell
# Afficher la clé privée
Get-Content $env:USERPROFILE\.ssh\cloudtaskhub_deploy
```

**Sur Windows avec Git Bash, Mac ou Linux** :
```bash
# Afficher la clé privée
cat ~/.ssh/cloudtaskhub_deploy
```

Copiez **TOUT** le contenu (y compris `-----BEGIN OPENSSH PRIVATE KEY-----` et `-----END OPENSSH PRIVATE KEY-----`).

Dans GitHub :
- **Name** : `SERVER_SSH_KEY`
- **Value** : Collez tout le contenu de la clé privée
- **Add secret**

#### Secret 6 : `SLACK_WEBHOOK_URL` (Optionnel)

Si vous voulez des notifications Slack :

1. Allez sur https://api.slack.com/messaging/webhooks
2. Créez un nouveau webhook
3. Choisissez un channel
4. Copiez l'URL du webhook
5. Dans GitHub : **Name** : `SLACK_WEBHOOK_URL`, **Value** : l'URL

> 💡 **Note** : Si vous ne configurez pas Slack, les workflows fonctionneront quand même, mais vous n'aurez pas de notifications.

### 6.2. Vérifier les Workflows GitHub Actions

Les workflows sont déjà configurés dans le projet. Vérifions qu'ils existent :

```bash
# Dans votre projet local
ls -la .github/workflows/
```

Vous devriez voir :
- `ci-pr.yml` : Tests sur Pull Request
- `ci-main.yml` : Build et push Docker sur main
- `cd-deploy.yml` : Déploiement automatique
- `cd-rollback.yml` : Rollback manuel

### 6.3. Adapter le Workflow de Déploiement pour GCP

Le workflow `cd-deploy.yml` devrait fonctionner tel quel, mais vérifions qu'il utilise bien `docker-compose.prod.yml` :

Ouvrez `.github/workflows/cd-deploy.yml` et vérifiez la ligne 50 :
```yaml
docker stack deploy -c docker-compose.prod.yml cloudtaskhub --with-registry-auth --prune
```

Si c'est correct, pas besoin de modification.

---

## 7. Premier Déploiement

### 7.1. Préparer la VM pour le Déploiement

**Sur la VM GCP** (connectez-vous en SSH) :

```bash
# Aller dans le répertoire du projet
cd /opt/cloudtaskhub

# Cloner le projet (si pas déjà fait)
# Note : GitHub Actions le fera automatiquement, mais testons manuellement d'abord
git clone https://github.com/VOTRE_USERNAME/microservice-cicd.git .

# Ou si le repo est privé, utilisez votre token :
# git clone https://TOKEN@github.com/VOTRE_USERNAME/microservice-cicd.git .
```

### 7.2. Créer le Fichier .env.prod

```bash
# Dans /opt/cloudtaskhub
nano .env.prod
```

Ajoutez :
```
DOCKERHUB_USERNAME=votre_username_dockerhub
IMAGE_TAG=latest
```

Sauvegardez (Ctrl+O, Enter, Ctrl+X).

### 7.3. Test de Déploiement Manuel (Optionnel)

Avant de laisser GitHub Actions faire le travail, testons manuellement :

```bash
# S'assurer que les réseaux existent
docker network create --driver overlay --attachable --subnet=172.20.0.0/16 traefik-public || true
docker network create --driver overlay --attachable --subnet=172.21.0.0/16 internal || true

# Se connecter à Docker Hub
docker login

# Déployer la stack
docker stack deploy -c docker-compose.prod.yml cloudtaskhub --with-registry-auth
```

> ⚠️ **Note** : Si les images n'existent pas encore sur Docker Hub, cette étape échouera. C'est normal ! Nous allons d'abord les build avec GitHub Actions.

### 7.4. Premier Push et Déploiement Automatique

**Sur votre machine locale** :

```bash
# Dans le répertoire du projet
cd microservice-cicd

# Faire un petit changement (pour déclencher le workflow)
echo "# Test deployment" >> README.md

# Commit et push
git add .
git commit -m "Trigger first deployment"
git push origin main
```

### 7.5. Suivre le Déploiement sur GitHub

1. Allez sur votre repository GitHub
2. Cliquez sur l'onglet **"Actions"**
3. Vous devriez voir le workflow **"CI - Main Build & Push"** en cours
4. Cliquez dessus pour voir les détails

**Étapes du workflow** :
1. **Checkout code** : Récupère le code
2. **Login to Docker Hub** : Se connecte à Docker Hub
3. **Build & Push** : Build les 6 services en parallèle et les pousse sur Docker Hub
4. **Scan image** : Scanne les images pour les vulnérabilités

Une fois terminé, le workflow **"CD - Deploy Production"** devrait se déclencher automatiquement.

### 7.6. Vérifier le Déploiement sur la VM

**Sur la VM GCP** :

```bash
# Voir les services déployés
docker service ls

# Voir les détails d'un service
docker service ps cloudtaskhub_gateway-service

# Voir les logs
docker service logs cloudtaskhub_gateway-service -f
```

Vous devriez voir 6 services :
- `cloudtaskhub_traefik`
- `cloudtaskhub_gateway-service`
- `cloudtaskhub_auth-service`
- `cloudtaskhub_project-service`
- `cloudtaskhub_billing-service`
- `cloudtaskhub_notification-service`
- `cloudtaskhub_analytics-service`
- `cloudtaskhub_jaeger`
- `cloudtaskhub_prometheus`
- `cloudtaskhub_grafana`

---

## 8. Tests et Vérifications

### 8.1. Tester le Gateway

Le Gateway est le point d'entrée de votre application.

```bash
# Depuis votre machine locale ou la VM
curl http://EXTERNAL_IP/

# Vous devriez voir :
# {"status":"ok","service":"gateway","message":"Welcome to the Gateway Service by Donald Programmer"}
```

### 8.2. Tester le Health Check

```bash
curl http://EXTERNAL_IP/health

# Devrait retourner :
# {"status":"ok","service":"gateway"}
```

### 8.3. Tester le Workflow Complet

Le Gateway expose un endpoint qui orchestre tous les services :

```bash
curl -X POST http://EXTERNAL_IP/workflow/create-project \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123",
    "project_title": "Mon Premier Projet"
  }'
```

Cette requête devrait :
1. Créer un utilisateur (Auth Service)
2. Créer un projet (Project Service)
3. Enregistrer un événement de facturation (Billing Service)
4. Envoyer une notification (Notification Service)
5. Récupérer des analytics (Analytics Service)

### 8.4. Accéder aux Interfaces de Monitoring

#### Traefik Dashboard
```
http://EXTERNAL_IP:8080/dashboard/
```

> ⚠️ **Important** : Avec `--api.insecure=true`, le dashboard Traefik est **uniquement accessible sur le port 8080**, pas via le port 80. C'est le comportement normal de Traefik v3. Les services internes (`@internal`) ne peuvent pas être routés via un entrypoint personnalisé comme `web`.

#### Prometheus
```
http://EXTERNAL_IP:9090
```

#### Grafana
```
http://EXTERNAL_IP:3000
```
- **Username** : `admin`
- **Password** : `admin` (vous serez demandé de changer au premier login)

#### Jaeger
```
http://EXTERNAL_IP:16686
```

### 8.5. Vérifier les Logs

**Sur la VM** :

```bash
# Logs du Gateway
docker service logs cloudtaskhub_gateway-service -f

# Logs de tous les services
docker service logs cloudtaskhub_traefik -f
docker service logs cloudtaskhub_auth-service -f
# etc.
```

---

## 9. Monitoring et Observabilité

### 9.1. Comprendre l'Observabilité

L'observabilité se compose de 3 piliers :

1. **Logs** : Enregistrements textuels des événements
2. **Métriques** : Données numériques (CPU, mémoire, requêtes/seconde)
3. **Traces** : Suivi d'une requête à travers plusieurs services

### 9.2. Utiliser Jaeger pour le Tracing

1. Allez sur `http://EXTERNAL_IP:16686`
2. Dans le menu déroulant "Service", sélectionnez `gateway-service`
3. Cliquez sur "Find Traces"
4. Vous devriez voir les traces des requêtes

**Explication d'une trace** :
- Chaque trace montre le chemin d'une requête
- Vous pouvez voir combien de temps chaque service prend
- Les erreurs sont visibles en rouge

### 9.3. Utiliser Prometheus pour les Métriques

1. Allez sur `http://EXTERNAL_IP:9090`
2. Dans la barre de recherche, tapez : `http_requests_total`
3. Cliquez sur "Execute"
4. Vous verrez les métriques de requêtes HTTP

### 9.4. Configurer Grafana (Optionnel)

Grafana permet de créer des dashboards visuels.

1. Allez sur `http://EXTERNAL_IP:3000`
2. Connectez-vous (admin/admin)
3. Allez dans **Configuration > Data Sources**
4. Ajoutez Prometheus :
   - **URL** : `http://prometheus:9090`
   - Cliquez sur "Save & Test"

### 9.5. Surveiller les Ressources

**Sur la VM** :

```bash
# Voir l'utilisation CPU et mémoire
docker stats

# Voir l'espace disque
df -h

# Voir les processus
top
```

---

## 10. Dépannage et Solutions

### 10.1. Les Services ne Démarrant Pas

**Symptôme** : `docker service ls` montre des services avec 0/1 replicas

**Solutions** :

```bash
# Voir les détails d'un service
docker service ps cloudtaskhub_gateway-service --no-trunc

# Voir les logs d'erreur
docker service logs cloudtaskhub_gateway-service

# Vérifier que les images existent
docker images | grep cloudtaskhub

# Si les images n'existent pas, vérifier Docker Hub
docker pull DOCKERHUB_USERNAME/cloudtaskhub-gateway:latest
```

### 10.2. Erreur de Connexion SSH depuis GitHub Actions

**Symptôme** : Le workflow `cd-deploy.yml` échoue avec une erreur SSH

**Solutions** :

1. **Vérifier que la clé SSH est correcte** :
   ```bash
   # Sur votre machine locale
   ssh -i ~/.ssh/cloudtaskhub_deploy USERNAME@EXTERNAL_IP
   ```

2. **Vérifier que le secret GitHub est correct** :
   - Le secret `SERVER_SSH_KEY` doit contenir **toute** la clé privée
   - Inclure les lignes `-----BEGIN...` et `-----END...`

3. **Vérifier le firewall GCP** :
   - Le port 22 doit être ouvert
   - Vérifiez dans "VPC network > Firewall"

### 10.3. Les Images Docker ne se Build Pas

**Symptôme** : Le workflow `ci-main.yml` échoue au build

**Solutions** :

1. **Vérifier les secrets Docker Hub** :
   - `DOCKERHUB_USERNAME` doit être correct
   - `DOCKERHUB_TOKEN` doit être valide

2. **Vérifier les Dockerfiles** :
   ```bash
   # Tester localement
   cd services/gateway
   docker build -t test .
   ```

### 10.4. Traefik ne Route Pas les Requêtes

**Symptôme** : Les requêtes vers `http://EXTERNAL_IP/` ne fonctionnent pas

**Solutions** :

```bash
# Vérifier que Traefik est en cours d'exécution
docker service ps cloudtaskhub_traefik

# Vérifier les logs de Traefik
docker service logs cloudtaskhub_traefik

# Vérifier que le réseau traefik-public existe
docker network ls | grep traefik-public

# Vérifier que le Gateway est sur le bon réseau
docker service inspect cloudtaskhub_gateway-service | grep -A 10 Networks
```

### 10.5. Problèmes de Mémoire

**Symptôme** : Les services crashent ou sont lents

**Solutions** :

1. **Vérifier l'utilisation mémoire** :
   ```bash
   free -h
   docker stats
   ```

2. **Réduire le nombre de réplicas** :
   - Modifier `docker-compose.prod.yml`
   - Réduire `replicas: 2` à `replicas: 1`

3. **Upgrader la VM** :
   - Dans GCP Console, arrêtez la VM
   - Changez le type de machine (ex: e2-standard-2 → e2-standard-4)
   - Redémarrez

### 10.6. Réinitialiser Tout

Si tout est cassé et que vous voulez recommencer :

```bash
# Sur la VM
# Supprimer la stack
docker stack rm cloudtaskhub

# Attendre que tout soit supprimé
docker service ls  # Devrait être vide

# Supprimer les réseaux
docker network rm traefik-public internal

# Nettoyer Docker
docker system prune -af

# Recréer les réseaux
docker network create --driver=overlay traefik-public
docker network create --driver=overlay internal

# Redéployer
cd /opt/cloudtaskhub
docker stack deploy -c docker-compose.prod.yml cloudtaskhub --with-registry-auth
```

---

## 🎉 Félicitations !

Vous avez maintenant :
- ✅ Créé une VM sur Google Cloud Platform
- ✅ Installé Docker et Docker Swarm
- ✅ Configuré un pipeline CI/CD complet
- ✅ Déployé 6 microservices
- ✅ Configuré l'observabilité (tracing, métriques, logs)
- ✅ Mis en place un reverse proxy (Traefik)

### 🚀 Prochaines Étapes

1. **Personnaliser les services** : Modifiez le code des microservices selon vos besoins
2. **Ajouter HTTPS** : Configurez Let's Encrypt avec Traefik
3. **Ajouter Kafka** : Réactivez Kafka pour la communication asynchrone
4. **Créer des dashboards Grafana** : Visualisez vos métriques
5. **Ajouter plus de tests** : Écrivez des tests unitaires et d'intégration
6. **Mettre à l'échelle** : Ajoutez plus de réplicas ou plus de machines

### 📚 Ressources pour Aller Plus Loin

- **Docker Documentation** : https://docs.docker.com/
- **Docker Swarm** : https://docs.docker.com/engine/swarm/
- **Traefik Documentation** : https://doc.traefik.io/traefik/
- **OpenTelemetry** : https://opentelemetry.io/
- **Prometheus** : https://prometheus.io/docs/
- **Grafana** : https://grafana.com/docs/

### 💰 N'oubliez Pas

- **Arrêtez la VM** quand vous ne l'utilisez pas pour économiser de l'argent
- Dans GCP Console : Compute Engine > VM instances > Arrêter

---

**Bon courage et bon apprentissage ! 🎓**

