# 🔑 Guide SSH pour Windows - Génération des Clés

## Problème : "No such file or directory"

Si vous obtenez l'erreur `Saving key "~/.ssh/cloudtaskhub_deploy" failed: No such file or directory`, c'est parce que le répertoire `.ssh` n'existe pas sur Windows.

## ✅ Solution Rapide

### Option 1 : PowerShell (Recommandé)

Ouvrez **PowerShell** (pas CMD) et exécutez :

```powershell
# 1. Créer le répertoire .ssh
New-Item -ItemType Directory -Force -Path $env:USERPROFILE\.ssh

# 2. Vérifier que le répertoire existe
Test-Path $env:USERPROFILE\.ssh
# Devrait retourner : True

# 3. Générer la paire de clés SSH
ssh-keygen -t ed25519 -C "github-actions-cloudtaskhub" -f "$env:USERPROFILE\.ssh\cloudtaskhub_deploy"

# 4. Quand demandé pour le passphrase, appuyez simplement sur Entrée (deux fois)
# Cela créera les clés sans mot de passe (plus simple pour GitHub Actions)
```

### Option 2 : Git Bash

Si vous préférez utiliser Git Bash :

```bash
# 1. Créer le répertoire .ssh
mkdir -p ~/.ssh

# 2. Vérifier
ls -la ~/.ssh

# 3. Générer la paire de clés SSH
ssh-keygen -t ed25519 -C "github-actions-cloudtaskhub" -f ~/.ssh/cloudtaskhub_deploy

# 4. Quand demandé pour le passphrase, appuyez simplement sur Entrée (deux fois)
```

## 📍 Emplacement des Fichiers

Après la génération, les fichiers se trouvent à :

**PowerShell** :
- Clé privée : `C:\Users\VOTRE_USERNAME\.ssh\cloudtaskhub_deploy`
- Clé publique : `C:\Users\VOTRE_USERNAME\.ssh\cloudtaskhub_deploy.pub`

**Git Bash** :
- Clé privée : `~/.ssh/cloudtaskhub_deploy` (qui est `C:\Users\VOTRE_USERNAME\.ssh\cloudtaskhub_deploy`)
- Clé publique : `~/.ssh/cloudtaskhub_deploy.pub`

## 🔍 Vérifier que les Clés sont Créées

**PowerShell** :
```powershell
# Lister les fichiers
Get-ChildItem $env:USERPROFILE\.ssh\cloudtaskhub_deploy*

# Devrait afficher :
# cloudtaskhub_deploy      (fichier sans extension = clé privée)
# cloudtaskhub_deploy.pub  (fichier .pub = clé publique)
```

**Git Bash** :
```bash
ls -la ~/.ssh/cloudtaskhub_deploy*
```

## 📋 Prochaines Étapes

Une fois les clés créées :

1. **Afficher la clé publique** (pour la copier sur la VM) :

   **PowerShell** :
   ```powershell
   Get-Content $env:USERPROFILE\.ssh\cloudtaskhub_deploy.pub
   ```

   **Git Bash** :
   ```bash
   cat ~/.ssh/cloudtaskhub_deploy.pub
   ```

2. **Copier la clé publique sur la VM GCP** (voir le tutoriel complet section 6.1)

3. **Afficher la clé privée** (pour la mettre dans GitHub) :

   **PowerShell** :
   ```powershell
   Get-Content $env:USERPROFILE\.ssh\cloudtaskhub_deploy
   ```

   **Git Bash** :
   ```bash
   cat ~/.ssh/cloudtaskhub_deploy
   ```

4. **Ajouter la clé privée dans GitHub Secrets** (nom : `SERVER_SSH_KEY`)

## ⚠️ Notes Importantes

- **Ne partagez JAMAIS votre clé privée** (`cloudtaskhub_deploy` sans `.pub`)
- La clé privée va dans GitHub Secrets
- La clé publique va sur la VM GCP
- Si vous avez créé un passphrase, vous devrez le saisir à chaque utilisation (non recommandé pour GitHub Actions)

## 🐛 Dépannage

### Erreur : "ssh-keygen n'est pas reconnu"

**Solution** : Installez OpenSSH sur Windows :

```powershell
# Dans PowerShell en tant qu'administrateur
Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0
```

Ou utilisez Git Bash qui inclut ssh-keygen.

### Erreur : "Permission denied"

**Solution** : Vérifiez les permissions du répertoire :

```powershell
# Dans PowerShell
icacls $env:USERPROFILE\.ssh
```

Le répertoire doit être accessible uniquement par votre utilisateur.

---

**Retour au tutoriel** : [Tutoriel Complet GCP](./tutoriel-complet-gcp.md#secret-5--server_ssh_key)

