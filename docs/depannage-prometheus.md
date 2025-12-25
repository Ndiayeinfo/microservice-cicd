# 🔧 Dépannage : Prometheus ne démarre pas

## ❌ Problème : Prometheus ne démarre pas (ERR_CONNECTION_REFUSED)

### Causes Possibles

1. **Fichier d'alertes manquant ou invalide**
2. **Erreur de syntaxe dans prometheus.yml**
3. **Service non déployé**
4. **Port 9090 bloqué par le firewall**

## ✅ Solutions

### Solution 1 : Vérifier l'État du Service

**Sur la VM GCP** :

```bash
# Vérifier si le service existe
docker service ls | grep prometheus

# Vérifier l'état détaillé
docker service ps cloudtaskhub_prometheus --no-trunc

# Voir les logs d'erreur
docker service logs cloudtaskhub_prometheus --tail 50
```

### Solution 2 : Vérifier les Fichiers de Configuration

**Sur la VM GCP** :

```bash
# Vérifier que les fichiers existent
cd /opt/cloudtaskhub
ls -la prometheus.yml prometheus-alerts.yml

# Vérifier la syntaxe de prometheus.yml
docker run --rm -v $(pwd):/config prom/prometheus:latest \
  promtool check config /config/prometheus.yml

# Vérifier la syntaxe de prometheus-alerts.yml
docker run --rm -v $(pwd):/config prom/prometheus:latest \
  promtool check rules /config/prometheus-alerts.yml
```

### Solution 3 : Créer le Fichier d'Alertes si Manquant

Si le fichier `prometheus-alerts.yml` n'existe pas sur la VM :

```bash
# Sur la VM
cd /opt/cloudtaskhub

# Créer un fichier d'alertes minimal (vide)
cat > prometheus-alerts.yml << 'EOF'
groups:
  - name: cloudtaskhub_alerts
    interval: 30s
    rules: []
EOF

# Redémarrer Prometheus
docker service update --force cloudtaskhub_prometheus
```

### Solution 4 : Désactiver Temporairement les Alertes

Si vous voulez démarrer Prometheus sans alertes :

**Sur la VM** :

```bash
cd /opt/cloudtaskhub

# Éditer prometheus.yml
nano prometheus.yml

# Commenter la section rule_files :
# rule_files:
#   - "/etc/prometheus/prometheus-alerts.yml"

# Redémarrer
docker service update --force cloudtaskhub_prometheus
```

### Solution 5 : Vérifier le Firewall GCP

1. Allez dans **GCP Console > VPC network > Firewall**
2. Vérifiez qu'une règle existe pour TCP:9090
3. Si elle n'existe pas, créez-la :
   - **Name** : `allow-prometheus`
   - **Direction** : Ingress
   - **Targets** : All instances
   - **Source IP ranges** : `0.0.0.0/0`
   - **Protocols and ports** : TCP:9090

### Solution 6 : Vérifier les Logs Détaillés

**Sur la VM** :

```bash
# Logs complets
docker service logs cloudtaskhub_prometheus --tail 100

# Filtrer les erreurs
docker service logs cloudtaskhub_prometheus --tail 100 | grep -i error

# Vérifier les erreurs de configuration
docker service logs cloudtaskhub_prometheus --tail 100 | grep -i "config\|rule\|alert"
```

## 🔍 Diagnostic Complet

**Sur la VM GCP**, exécutez ce script de diagnostic :

```bash
echo "=== DIAGNOSTIC PROMETHEUS ==="
echo ""
echo "1. État du service :"
docker service ps cloudtaskhub_prometheus --no-trunc
echo ""
echo "2. Fichiers de configuration :"
ls -la /opt/cloudtaskhub/prometheus*.yml
echo ""
echo "3. Logs récents :"
docker service logs cloudtaskhub_prometheus --tail 30
echo ""
echo "4. Ports en écoute :"
sudo ss -tlnp | grep 9090 || echo "Port 9090 non ouvert"
echo ""
echo "5. Test de connexion locale :"
curl -v http://localhost:9090/-/healthy 2>&1 | head -10
```

## 🐛 Erreurs Courantes

### Erreur : "error loading rule files"

**Cause** : Le fichier `prometheus-alerts.yml` n'existe pas ou a une erreur de syntaxe

**Solution** : Vérifiez que le fichier existe et a une syntaxe YAML valide

### Erreur : "failed to load config"

**Cause** : Erreur de syntaxe dans `prometheus.yml`

**Solution** : Utilisez `promtool check config` pour valider

### Erreur : "bind: address already in use"

**Cause** : Un autre processus utilise le port 9090

**Solution** : Vérifiez avec `sudo ss -tlnp | grep 9090`

## ✅ Vérification Rapide

Après correction, vérifiez que Prometheus fonctionne :

```bash
# Sur la VM
curl http://localhost:9090/-/healthy

# Devrait retourner : Prometheus is Healthy.
```

Puis testez depuis l'extérieur :
```
http://VOTRE_IP:9090
```

---

**Retour au tutoriel** : [Tutoriel Complet GCP](./tutoriel-complet-gcp.md#93-utiliser-prometheus-pour-les-métriques)

