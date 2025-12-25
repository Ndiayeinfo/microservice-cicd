# 🔧 Dépannage : Accès au Dashboard Traefik

## ❌ Problème : Le dashboard Traefik n'est pas accessible

### Solutions

#### Solution 1 : Vérifier le Firewall GCP

Le port 8080 doit être ouvert dans le firewall GCP :

1. Allez dans **GCP Console > VPC network > Firewall**
2. Vérifiez qu'une règle existe pour le port 8080 :
   - **Name** : `allow-traefik-dashboard`
   - **Ports** : TCP:8080
   - **Source IP ranges** : `0.0.0.0/0` (ou votre IP)

Si la règle n'existe pas, créez-la :
- **Name** : `allow-traefik-dashboard`
- **Direction** : Ingress
- **Targets** : All instances in the network
- **Source IP ranges** : `0.0.0.0/0`
- **Protocols and ports** : TCP:8080
- **Create**

#### Solution 2 : Vérifier que Traefik écoute sur le port 8080

**Sur la VM GCP** :

```bash
# Vérifier que le service Traefik est en cours d'exécution
docker service ps cloudtaskhub_traefik

# Vérifier les ports ouverts
sudo netstat -tlnp | grep 8080
# ou
sudo ss -tlnp | grep 8080

# Vérifier les logs de Traefik
docker service logs cloudtaskhub_traefik --tail 50
```

#### Solution 3 : Accéder via le port 80 (après redéploiement)

Après avoir poussé la correction, le dashboard sera accessible via :

```
http://VOTRE_IP/dashboard/
```

ou

```
http://VOTRE_IP/api/rawdata
```

#### Solution 4 : Tester depuis la VM

**Sur la VM GCP**, testez localement :

```bash
# Tester le port 8080 localement
curl http://localhost:8080/dashboard/

# Tester le port 80 avec le routing
curl http://localhost/dashboard/
```

Si cela fonctionne localement mais pas depuis l'extérieur, c'est un problème de firewall.

#### Solution 5 : Vérifier la Configuration Traefik

**Sur la VM GCP** :

```bash
# Vérifier la configuration du service
docker service inspect cloudtaskhub_traefik --pretty

# Vérifier les labels
docker service inspect cloudtaskhub_traefik | grep -A 20 Labels
```

## ✅ Configuration Corrigée

La configuration a été mise à jour pour :

1. **Ajouter `--api.insecure=true`** : Permet l'accès au dashboard sans authentification
2. **Créer un entrypoint `dashboard` sur le port 8080** : `--entrypoints.dashboard.address=:8080`
3. **Configurer un router pour l'accès direct** : Dashboard accessible sur `http://IP:8080/`

## 🧪 Test après Redéploiement

Après avoir poussé la correction et redéployé :

1. **Accès direct sur port 8080** :
   ```
   http://35.205.129.107:8080/dashboard/
   ```

2. **Accès via routing sur port 80** :
   ```
   http://35.205.129.107/dashboard/
   ```

## 📋 Checklist de Diagnostic

- [ ] Le firewall GCP autorise le port 8080
- [ ] Le service Traefik est en cours d'exécution (`docker service ps cloudtaskhub_traefik`)
- [ ] Le port 8080 est ouvert sur la VM (`netstat -tlnp | grep 8080`)
- [ ] Les logs Traefik ne montrent pas d'erreurs (`docker service logs cloudtaskhub_traefik`)
- [ ] Le test local fonctionne (`curl http://localhost:8080/dashboard/`)

## 🔍 Commandes de Diagnostic Complètes

```bash
# Sur la VM GCP

# 1. Vérifier l'état du service
docker service ls | grep traefik

# 2. Vérifier les détails
docker service ps cloudtaskhub_traefik --no-trunc

# 3. Vérifier les ports
docker service inspect cloudtaskhub_traefik | grep -A 10 Ports

# 4. Tester localement
curl -v http://localhost:8080/dashboard/
curl -v http://localhost/dashboard/

# 5. Vérifier les logs
docker service logs cloudtaskhub_traefik --tail 100 | grep -i error
```

---

**Retour au tutoriel** : [Tutoriel Complet GCP](./tutoriel-complet-gcp.md#84-accéder-aux-interfaces-de-monitoring)

