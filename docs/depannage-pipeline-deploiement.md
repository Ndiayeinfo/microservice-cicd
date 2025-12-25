# 🔧 Dépannage : Pipeline de Déploiement ne s'exécute pas

## ❌ Problème : Le workflow de déploiement ne se déclenche pas

### 🔍 Diagnostic

Le workflow `cd-deploy.yml` se déclenche **uniquement** après que le workflow `CI - Main Build & Push` se termine avec **succès**.

**Chaîne de déclenchement** :
```
Push sur main 
  → Déclenche "CI - Main Build & Push" (ci-main.yml)
    → Si succès → Déclenche "CD - Deploy Production" (cd-deploy.yml)
```

## ✅ Checklist de Vérification

### 1. Vérifier que le Workflow CI se Déclenche

**Sur GitHub** :
1. Allez sur votre repository
2. Cliquez sur l'onglet **Actions**
3. Vérifiez si vous voyez le workflow **"CI - Main Build & Push"** dans la liste
4. Si vous ne le voyez pas, le workflow ne se déclenche pas

**Causes possibles** :
- ❌ Vous n'avez pas pushé sur la branche `main`
- ❌ GitHub Actions est désactivé dans les paramètres
- ❌ Le fichier `.github/workflows/ci-main.yml` n'existe pas ou a une erreur

### 2. Vérifier que le Workflow CI Réussit

**Sur GitHub** :
1. Allez sur **Actions**
2. Cliquez sur le dernier run de **"CI - Main Build & Push"**
3. Vérifiez le statut :
   - ✅ **Succès (vert)** → Le déploiement devrait se déclencher
   - ❌ **Échec (rouge)** → Le déploiement ne se déclenchera **PAS**
   - ⏳ **En cours** → Attendez la fin

**Causes d'échec courantes** :
- ❌ Secrets manquants (`DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`)
- ❌ Erreur de build Docker
- ❌ Scan Trivy détecte des vulnérabilités critiques
- ❌ Problème de connexion à Docker Hub

### 3. Vérifier que le Workflow CD se Déclenche

**Sur GitHub** :
1. Allez sur **Actions**
2. Cherchez le workflow **"CD - Deploy Production"**
3. Vérifiez s'il apparaît après un succès de **"CI - Main Build & Push"**

**Si le workflow CD n'apparaît pas** :
- Le workflow CI a peut-être échoué
- Le nom du workflow dans `cd-deploy.yml` ne correspond pas exactement

### 4. Vérifier le Nom du Workflow

Le workflow `cd-deploy.yml` cherche le workflow nommé **exactement** `"CI - Main Build & Push"`.

**Vérifier** :
```bash
# Voir le nom dans ci-main.yml
grep "^name:" .github/workflows/ci-main.yml

# Voir le nom recherché dans cd-deploy.yml
grep -A 2 "workflow_run" .github/workflows/cd-deploy.yml
```

**Les noms doivent correspondre exactement** (sensible à la casse) !

## 🔧 Solutions

### Solution 1 : Vérifier les Secrets GitHub

Le workflow CI nécessite ces secrets :
- ✅ `DOCKERHUB_USERNAME`
- ✅ `DOCKERHUB_TOKEN`

**Vérifier** :
1. Allez sur **Settings > Secrets and variables > Actions**
2. Vérifiez que ces secrets existent
3. Si un secret manque, ajoutez-le

### Solution 2 : Vérifier les Logs du Workflow CI

**Sur GitHub** :
1. Allez sur **Actions**
2. Cliquez sur le dernier run de **"CI - Main Build & Push"**
3. Cliquez sur un job qui a échoué
4. Lisez les logs pour identifier l'erreur

**Erreurs courantes** :
- `Error: Cannot perform an interactive login from a non TTY device` → Problème de connexion Docker Hub
- `Error: failed to solve` → Erreur de build Docker
- `FATAL: found critical vulnerabilities` → Scan Trivy bloque le build

### Solution 3 : Forcer le Déclenchement du Déploiement

Si le workflow CI réussit mais que le déploiement ne se déclenche pas, vous pouvez :

**Option A : Déclencher manuellement (si workflow_dispatch est activé)**

Modifiez `cd-deploy.yml` pour ajouter `workflow_dispatch` :

```yaml
on:
  workflow_run:
    workflows: ["CI - Main Build & Push"]
    types: [completed]
    branches: [main]
  workflow_dispatch:  # Ajoutez cette ligne
```

Puis sur GitHub :
1. Allez sur **Actions**
2. Sélectionnez **"CD - Deploy Production"**
3. Cliquez sur **"Run workflow"**

**Option B : Déclencher directement sur push (alternative)**

Modifiez `cd-deploy.yml` pour se déclencher aussi sur push :

```yaml
on:
  push:
    branches: [main]
  workflow_run:
    workflows: ["CI - Main Build & Push"]
    types: [completed]
    branches: [main]
```

⚠️ **Attention** : Cette option déploiera même si le build CI échoue.

### Solution 4 : Vérifier les Permissions GitHub Actions

**Sur GitHub** :
1. Allez sur **Settings > Actions > General**
2. Vérifiez que **"Allow all actions and reusable workflows"** est sélectionné
3. Vérifiez que **"Workflow permissions"** est sur **"Read and write permissions"**

### Solution 5 : Vérifier la Branche

Le workflow CI se déclenche uniquement sur `push` vers `main`.

**Vérifier votre branche** :
```bash
git branch
```

**Si vous n'êtes pas sur main** :
```bash
git checkout main
git push origin main
```

## 🧪 Test Rapide

Pour tester si le pipeline fonctionne :

```bash
# 1. Assurez-vous d'être sur main
git checkout main

# 2. Faites un petit changement
echo "# Test pipeline" >> README.md

# 3. Commit et push
git add README.md
git commit -m "Test: trigger pipeline"
git push origin main

# 4. Allez sur GitHub > Actions
# Vous devriez voir :
# - "CI - Main Build & Push" démarrer
# - Puis "CD - Deploy Production" démarrer après succès
```

## 📋 Checklist Complète

- [ ] Je suis sur la branche `main` (`git branch` affiche `* main`)
- [ ] J'ai pushé vers `origin main` (`git push origin main`)
- [ ] Les workflows sont activés dans **Settings > Actions > General**
- [ ] Les secrets `DOCKERHUB_USERNAME` et `DOCKERHUB_TOKEN` existent
- [ ] Le workflow **"CI - Main Build & Push"** apparaît dans l'onglet Actions
- [ ] Le workflow **"CI - Main Build & Push"** se termine avec succès (vert)
- [ ] Le workflow **"CD - Deploy Production"** apparaît après le succès du CI
- [ ] J'ai lu les logs d'erreur si un workflow a échoué

## 🔍 Commandes de Diagnostic

```bash
# Voir la branche actuelle
git branch

# Voir le dernier commit
git log -1

# Voir les remotes
git remote -v

# Voir l'état du repository
git status

# Voir les workflows
ls -la .github/workflows/

# Vérifier le nom du workflow CI
grep "^name:" .github/workflows/ci-main.yml

# Vérifier le nom recherché dans le workflow CD
grep -A 2 "workflow_run" .github/workflows/cd-deploy.yml
```

## 💡 Astuce : Voir l'Historique des Workflows

**Sur GitHub** :
1. Allez sur **Actions**
2. Vous verrez tous les workflows exécutés
3. Cliquez sur un workflow pour voir les détails
4. Les workflows en vert ont réussi, en rouge ont échoué

## 🐛 Erreurs Courantes

### Erreur : "Workflow run not found"

**Cause** : Le workflow `CI - Main Build & Push` n'existe pas ou a un nom différent.

**Solution** : Vérifiez que le nom dans `ci-main.yml` correspond exactement à celui dans `cd-deploy.yml`.

### Erreur : "Workflow run failed"

**Cause** : Le workflow CI a échoué, donc le CD ne se déclenche pas.

**Solution** : Corrigez les erreurs dans le workflow CI, puis relancez.

### Erreur : "No workflow run found"

**Cause** : Aucun workflow CI n'a été exécuté récemment.

**Solution** : Faites un push sur `main` pour déclencher le workflow CI.

## ✅ Vérification Finale

Après correction, vérifiez que le pipeline fonctionne :

1. **Push sur main** → Déclenche CI
2. **CI réussit** → Déclenche CD
3. **CD se termine** → Déploiement effectué sur la VM

Si tout fonctionne, vous devriez voir dans l'onglet Actions :
- ✅ CI - Main Build & Push (succès)
- ✅ CD - Deploy Production (succès)

