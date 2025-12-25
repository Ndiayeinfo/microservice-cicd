# 🔧 Dépannage : Workflow GitHub Actions ne démarre pas

## ✅ Checklist de Vérification

### 1. Vérifier la Branche

Le workflow `ci-main.yml` se déclenche **uniquement** sur un push vers la branche `main`.

**Vérifier votre branche actuelle** :

```bash
# Voir la branche actuelle
git branch

# Voir toutes les branches (locales et distantes)
git branch -a
```

**Si vous n'êtes pas sur `main`** :

```bash
# Aller sur la branche main
git checkout main

# Ou créer la branche main si elle n'existe pas
git checkout -b main

# Pousser vers GitHub
git push -u origin main
```

> ⚠️ **Note** : Si votre branche par défaut s'appelle `master` au lieu de `main`, vous devez soit :
> - Renommer la branche en `main`
> - Ou modifier le workflow pour utiliser `master`

### 2. Vérifier que les Workflows sont Activés

1. Allez sur votre repository GitHub
2. Cliquez sur **Settings** (Paramètres)
3. Dans le menu de gauche, allez dans **Actions > General**
4. Vérifiez que **"Allow all actions and reusable workflows"** est sélectionné
5. Vérifiez que **"Workflow permissions"** est sur **"Read and write permissions"**

### 3. Vérifier l'Onglet Actions

1. Allez sur votre repository GitHub
2. Cliquez sur l'onglet **Actions** (en haut)
3. Vérifiez si vous voyez des workflows en cours ou en attente

**Si vous ne voyez rien** :
- Le workflow n'a peut-être pas été déclenché
- Vérifiez que vous avez bien pushé sur `main`

**Si vous voyez des workflows mais qu'ils sont en attente** :
- Vérifiez que vous avez configuré les secrets GitHub (voir ci-dessous)

### 4. Vérifier les Secrets GitHub

Le workflow `ci-main.yml` nécessite ces secrets :

- ✅ `DOCKERHUB_USERNAME`
- ✅ `DOCKERHUB_TOKEN`

**Vérifier les secrets** :

1. Allez sur **Settings > Secrets and variables > Actions**
2. Vérifiez que ces secrets existent
3. Si un secret manque, le workflow échouera

### 5. Vérifier la Syntaxe des Workflows

**Vérifier que les fichiers workflow existent** :

```bash
# Dans votre projet local
ls -la .github/workflows/
```

Vous devriez voir :
- `ci-main.yml`
- `ci-pr.yml`
- `cd-deploy.yml`
- etc.

**Vérifier la syntaxe YAML** :

Les workflows doivent être des fichiers YAML valides. Si vous avez modifié les workflows, vérifiez qu'il n'y a pas d'erreurs de syntaxe.

### 6. Vérifier les Logs GitHub Actions

1. Allez sur **Actions** dans votre repository
2. Cliquez sur un workflow (même s'il a échoué)
3. Cliquez sur le job qui a échoué
4. Lisez les logs pour voir l'erreur exacte

## 🐛 Problèmes Courants et Solutions

### Problème 1 : "Workflow not triggered"

**Symptôme** : Aucun workflow n'apparaît dans l'onglet Actions après un push.

**Solutions** :

1. **Vérifier la branche** :
   ```bash
   git branch
   # Si vous n'êtes pas sur main, faites :
   git checkout main
   git push origin main
   ```

2. **Vérifier que le fichier workflow existe** :
   ```bash
   cat .github/workflows/ci-main.yml
   ```

3. **Vérifier que le workflow est bien dans le repository GitHub** :
   - Allez sur GitHub
   - Cliquez sur `.github/workflows/ci-main.yml`
   - Vérifiez que le fichier existe et contient bien `branches: [ main ]`

### Problème 2 : "Workflow triggered but failed immediately"

**Symptôme** : Le workflow démarre mais échoue tout de suite.

**Solutions** :

1. **Vérifier les secrets** :
   - `DOCKERHUB_USERNAME` doit exister
   - `DOCKERHUB_TOKEN` doit exister et être valide

2. **Vérifier les logs** :
   - Allez dans Actions > Cliquez sur le workflow qui a échoué
   - Lisez l'erreur exacte

### Problème 3 : "Workflow runs but jobs are skipped"

**Symptôme** : Le workflow démarre mais tous les jobs sont "skipped".

**Causes possibles** :

1. **Condition `if` qui échoue** : Vérifiez les conditions dans le workflow
2. **Branche incorrecte** : Le workflow ne se déclenche que sur `main`

### Problème 4 : "Repository is private and workflows are disabled"

**Symptôme** : Vous avez un repository privé et les workflows ne fonctionnent pas.

**Solution** :

1. Allez dans **Settings > Actions > General**
2. Vérifiez que **"Allow all actions and reusable workflows"** est activé
3. Pour les repos privés, vous devez avoir un plan GitHub qui supporte les Actions (gratuit pour les repos publics, payant pour les privés)

## 🧪 Test Rapide

Pour tester si les workflows fonctionnent :

```bash
# 1. Assurez-vous d'être sur main
git checkout main

# 2. Faites un petit changement
echo "# Test workflow" >> README.md

# 3. Commit et push
git add README.md
git commit -m "Test: trigger workflow"
git push origin main

# 4. Allez sur GitHub > Actions
# Vous devriez voir le workflow "CI - Main Build & Push" démarrer
```

## 📋 Vérification Complète

Exécutez cette checklist dans l'ordre :

- [ ] Je suis sur la branche `main` (`git branch` affiche `* main`)
- [ ] J'ai pushé vers `origin main` (`git push origin main`)
- [ ] Les workflows sont activés dans Settings > Actions > General
- [ ] Les secrets `DOCKERHUB_USERNAME` et `DOCKERHUB_TOKEN` existent
- [ ] Le fichier `.github/workflows/ci-main.yml` existe
- [ ] J'ai vérifié l'onglet Actions sur GitHub
- [ ] J'ai lu les logs d'erreur si le workflow a échoué

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

# Voir si les workflows existent
ls -la .github/workflows/

# Voir le contenu du workflow principal
cat .github/workflows/ci-main.yml | head -20
```

## 💡 Astuce : Forcer le Déclenchement

Si rien ne fonctionne, vous pouvez forcer le déclenchement manuellement :

1. Allez sur GitHub > Actions
2. Cliquez sur "CI - Main Build & Push" dans la liste de gauche
3. Cliquez sur "Run workflow" (en haut à droite)
4. Sélectionnez la branche `main`
5. Cliquez sur "Run workflow"

> ⚠️ **Note** : Cette option n'est disponible que si le workflow a déjà été exécuté au moins une fois.

## 📞 Besoin d'Aide Supplémentaire ?

Si le problème persiste :

1. **Vérifiez les logs GitHub Actions** : Ils contiennent toujours l'erreur exacte
2. **Vérifiez la documentation GitHub** : https://docs.github.com/en/actions
3. **Vérifiez les permissions** : Settings > Actions > General > Workflow permissions

---

**Retour au tutoriel** : [Tutoriel Complet GCP](./tutoriel-complet-gcp.md#74-premier-push-et-déploiement-automatique)

