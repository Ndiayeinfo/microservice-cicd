# 🔧 Solution de Contournement : Limite Docker Hub

## ⚠️ Situation Actuelle

La limite Docker Hub est atteinte. Le workflow CI ne peut pas build les images car il ne peut pas puller `python:3.11-slim` depuis Docker Hub.

## ✅ Solution Immédiate : Utiliser des Images Existantes

Si vous avez déjà des images buildées précédemment sur `ghcr.io`, vous pouvez les utiliser sans rebuild.

### Option 1 : Déclencher le Déploiement Sans Build

1. **Allez sur GitHub > Actions**
2. **Sélectionnez "CI - Main Build & Push"**
3. **Cliquez sur "Run workflow"**
4. **Cochez "Skip build (utiliser images existantes)"**
5. **Cliquez sur "Run workflow"**

Cela déclenchera le workflow de déploiement sans rebuild, utilisant les images déjà disponibles sur `ghcr.io`.

### Option 2 : Vérifier les Images Disponibles

Vérifiez si des images existent déjà sur GitHub Container Registry :

1. Allez sur votre repository GitHub
2. Cliquez sur **Packages** (à droite)
3. Vérifiez si des images `cloudtaskhub-*` existent

Si des images existent, vous pouvez les utiliser directement.

### Option 3 : Attendre la Réinitialisation

**La limite Docker Hub se réinitialise toutes les 6 heures.**

1. Notez l'heure à laquelle vous avez atteint la limite
2. Attendez 6 heures
3. Relancez le workflow normalement

## 🚀 Déploiement Direct (Sans Build)

Si vous voulez déployer sans rebuild :

1. **Déclenchez manuellement le workflow de déploiement** :
   - Allez sur **Actions > CD - Deploy Production**
   - Cliquez sur **"Run workflow"**
   - Cela utilisera les images déjà disponibles sur `ghcr.io`

2. **Vérifiez que les images existent** :
   ```bash
   # Sur la VM
   docker pull ghcr.io/ndiayeinfo/cloudtaskhub-gateway:latest
   ```

## 📋 Checklist

- [ ] J'ai vérifié si des images existent sur `ghcr.io`
- [ ] Si oui, j'utilise le workflow de déploiement directement
- [ ] Si non, j'attends 6 heures pour la réinitialisation Docker Hub
- [ ] J'ai lu `docs/solution-docker-rate-limit.md` pour plus d'informations

## 💡 Pourquoi Cette Solution Fonctionne

- Les images buildées sont stockées sur `ghcr.io` (pas de limite)
- Le déploiement peut utiliser ces images sans rebuild
- Pas besoin de puller depuis Docker Hub pour le déploiement

## 🔄 Après la Réinitialisation

Une fois que la limite Docker Hub se réinitialise (après 6 heures) :

1. **Relancez le workflow CI normalement**
2. **Les images seront buildées et pushées vers `ghcr.io`**
3. **Le cache GitHub Actions évitera de repuller les images de base**

## 📞 Support

Si vous avez besoin d'aide :
- Consultez `docs/solution-docker-rate-limit.md`
- Vérifiez votre utilisation Docker Hub sur https://hub.docker.com

