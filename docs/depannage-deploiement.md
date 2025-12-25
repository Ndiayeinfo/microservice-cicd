# 🔧 Dépannage : Erreur de Déploiement GitHub Actions

## ❌ Erreur : "fatal: not a git repository"

### Symptôme

Le workflow de déploiement (`cd-deploy.yml`) échoue avec l'erreur :
```
fatal: not a git repository (or any of the parent directories): .git
```

### Cause

Le workflow essaie d'exécuter des commandes Git (`git fetch`, `git reset`) dans `/opt/cloudtaskhub` sur la VM, mais ce répertoire n'est pas encore un repository Git (il n'a pas été cloné).

### ✅ Solution Automatique

Le workflow a été mis à jour pour gérer ce cas automatiquement. Il va :
1. Vérifier si `/opt/cloudtaskhub` est un repository Git
2. Si oui : mettre à jour le code
3. Si non : cloner le repository automatiquement

**Vous n'avez rien à faire** - le prochain déploiement devrait fonctionner.

### 🔧 Solution Manuelle (Alternative)

Si vous préférez préparer la VM manuellement avant le premier déploiement :

**Sur la VM GCP** (connectez-vous en SSH) :

```bash
# 1. Créer le répertoire
sudo mkdir -p /opt/cloudtaskhub
sudo chown -R $USER:$USER /opt/cloudtaskhub

# 2. Cloner le repository
cd /opt/cloudtaskhub
git clone https://github.com/VOTRE_USERNAME/microservice-cicd.git .

# Si le repo est privé, utilisez un token :
# git clone https://TOKEN@github.com/VOTRE_USERNAME/microservice-cicd.git .

# 3. Vérifier
git status
ls -la
```

### 🔐 Repository Privé

Si votre repository est **privé**, vous devez configurer un token GitHub :

1. **Créer un Personal Access Token GitHub** :
   - Allez sur GitHub > Settings > Developer settings > Personal access tokens > Tokens (classic)
   - Cliquez sur "Generate new token (classic)"
   - Donnez un nom : `cloudtaskhub-deploy`
   - Permissions : cochez `repo` (accès complet aux repositories)
   - Cliquez sur "Generate token"
   - **⚠️ COPIEZ LE TOKEN** (il ne sera plus visible)

2. **Ajouter le token dans GitHub Secrets** :
   - Allez dans votre repository > Settings > Secrets and variables > Actions
   - Créez un nouveau secret :
     - **Name** : `GITHUB_TOKEN`
     - **Value** : le token que vous venez de créer
     - **Add secret**

3. **Le workflow utilisera automatiquement ce token** pour cloner le repository privé.

### 🧪 Tester la Solution

Après avoir corrigé le workflow, testez-le :

```bash
# Sur votre machine locale
git add .github/workflows/cd-deploy.yml
git commit -m "Fix: handle git repository initialization in deployment"
git push origin main
```

Le workflow `CI - Main Build & Push` va se déclencher, puis `CD - Deploy Production` devrait maintenant fonctionner.

### 📋 Vérification

**Sur la VM GCP**, après le déploiement :

```bash
# Vérifier que le repository est cloné
cd /opt/cloudtaskhub
git status

# Vérifier que les fichiers sont présents
ls -la

# Vérifier que docker-compose.prod.yml existe
cat docker-compose.prod.yml | head -20
```

### 🐛 Autres Erreurs Possibles

#### Erreur : "open /opt/cloudtaskhub/.env.prod: no such file or directory"

**Symptôme** : Le déploiement échoue car le fichier `.env.prod` n'existe pas.

**Solution** : Le workflow a été corrigé pour créer automatiquement ce fichier. Si vous voyez encore cette erreur :

1. **Vérifier que le workflow est à jour** :
   - Le workflow doit créer automatiquement `.env.prod` avant le déploiement
   - Vérifiez dans GitHub Actions que la version corrigée est utilisée

2. **Créer manuellement le fichier** (solution temporaire) :
   ```bash
   # Sur la VM
   cd /opt/cloudtaskhub
   cat > .env.prod << EOF
   DOCKERHUB_USERNAME=votre_username_dockerhub
   IMAGE_TAG=latest
   EOF
   
   # Vérifier
   cat .env.prod
   ```

#### Erreur : "Permission denied"

**Solution** :
```bash
# Sur la VM
sudo chown -R $USER:$USER /opt/cloudtaskhub
```

#### Erreur : "Repository not found" (repo privé)

**Solution** : Configurez le token GitHub comme expliqué ci-dessus.

#### Erreur : "docker stack deploy" échoue

**Vérifier** :
1. Les réseaux Docker existent :
   ```bash
   docker network ls | grep -E "traefik-public|internal"
   ```

2. Docker Swarm est initialisé :
   ```bash
   docker info | grep Swarm
   ```

3. Les images Docker existent sur Docker Hub :
   ```bash
   docker pull DOCKERHUB_USERNAME/cloudtaskhub-gateway:latest
   ```

### 📞 Besoin d'Aide ?

Si le problème persiste :

1. **Vérifiez les logs GitHub Actions** :
   - Allez dans Actions > CD - Deploy Production
   - Cliquez sur le workflow qui a échoué
   - Lisez les logs détaillés

2. **Vérifiez les logs sur la VM** :
   ```bash
   # Se connecter à la VM
   ssh USERNAME@VM_IP
   
   # Vérifier le contenu de /opt/cloudtaskhub
   ls -la /opt/cloudtaskhub
   
   # Vérifier si c'est un repo Git
   cd /opt/cloudtaskhub
   git status
   ```

---

**Retour au tutoriel** : [Tutoriel Complet GCP](./tutoriel-complet-gcp.md#7-premier-déploiement)

