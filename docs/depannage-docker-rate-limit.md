# 🔧 Dépannage : Erreur Docker Hub Rate Limit (429)

## ❌ Problème : "Too Many Requests - You have reached your pull rate limit"

### 🔍 Explication

Docker Hub limite le nombre de pulls d'images pour les comptes gratuits :
- **Comptes anonymes** : 100 pulls toutes les 6 heures par IP
- **Comptes gratuits authentifiés** : 200 pulls toutes les 6 heures
- **Comptes payants** : Limite beaucoup plus élevée

Quand vous dépassez cette limite, vous recevez une erreur **429 Too Many Requests**.

## ✅ Solutions

### Solution 1 : Réduire le Parallélisme (Déjà Appliquée)

Le workflow `ci-main.yml` a été modifié pour réduire le parallélisme de 6 à 2 builds simultanés. Cela réduit la charge sur Docker Hub.

**Si le problème persiste**, vous pouvez réduire encore plus :

```yaml
max-parallel: 1  # Un seul build à la fois
```

### Solution 2 : Attendre que la Limite se Réinitialise

La limite se réinitialise toutes les 6 heures. Vous pouvez :
1. Attendre quelques heures
2. Relancer le workflow

### Solution 3 : Utiliser GitHub Container Registry (ghcr.io)

GitHub Container Registry n'a pas de limite de pull rate. C'est la meilleure solution à long terme.

**Modifier les Dockerfiles** pour utiliser `ghcr.io` :

```dockerfile
# Au lieu de :
FROM python:3.11-slim

# Utiliser :
FROM ghcr.io/docker-library/python:3.11-slim
```

**Ou créer un mirror** dans votre workflow.

### Solution 4 : Créer un Token Docker Hub avec Plus de Limites

Si vous avez un compte Docker Hub payant, vous aurez une limite beaucoup plus élevée.

### Solution 5 : Utiliser un Cache Local

Le workflow utilise déjà un cache, mais vous pouvez améliorer cela en utilisant un cache GitHub Actions :

```yaml
- name: Cache Docker layers
  uses: actions/cache@v3
  with:
    path: /tmp/.buildx-cache
    key: ${{ runner.os }}-buildx-${{ github.sha }}
    restore-keys: |
      ${{ runner.os }}-buildx-
```

## 🔍 Diagnostic

### Vérifier si vous êtes Authentifié

Dans les logs du workflow, vous devriez voir :
```
Login Succeeded
```

Si vous ne voyez pas cela, vérifiez que les secrets `DOCKERHUB_USERNAME` et `DOCKERHUB_TOKEN` sont configurés.

### Vérifier le Nombre de Pulls

Vous pouvez vérifier votre utilisation sur Docker Hub :
1. Allez sur https://hub.docker.com
2. Connectez-vous
3. Allez dans **Account Settings > Billing**
4. Vérifiez votre utilisation

## 🚀 Solution Recommandée : Utiliser GitHub Container Registry

Pour éviter complètement ce problème, migrez vers GitHub Container Registry :

1. **Modifier le workflow** pour utiliser `ghcr.io` :

```yaml
- name: Login to GitHub Container Registry
  uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}
```

2. **Modifier les tags** :

```yaml
tags: |
  ghcr.io/${{ github.repository_owner }}/cloudtaskhub-${{ matrix.service }}:latest
```

3. **Mettre à jour docker-compose.prod.yml** pour utiliser les images de `ghcr.io`

## 📋 Checklist

- [ ] Les secrets `DOCKERHUB_USERNAME` et `DOCKERHUB_TOKEN` sont configurés
- [ ] Le parallélisme est réduit à 2 (ou 1 si nécessaire)
- [ ] J'ai attendu quelques heures si j'ai dépassé la limite
- [ ] J'ai vérifié que l'authentification Docker Hub fonctionne dans les logs

## 💡 Astuce : Build Local pour Tester

Si vous voulez tester localement sans utiliser Docker Hub :

```bash
# Build local sans push
docker build -t cloudtaskhub-gateway:local ./services/gateway
```

## 🔗 Ressources

- [Docker Hub Rate Limiting](https://www.docker.com/increase-rate-limit)
- [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)

