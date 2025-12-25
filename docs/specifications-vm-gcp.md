# 💻 Spécifications de la Machine Virtuelle GCP

## 📊 Recommandations pour CloudTaskHub

### Configuration Standard (Recommandée)

**Type de machine** : `e2-standard-2`

| Composant | Spécification | Justification |
|-----------|---------------|---------------|
| **vCPU** | 2 cores | Suffisant pour 6 microservices + infrastructure |
| **RAM** | 8 Go | Permet de faire tourner tous les services confortablement |
| **Disque** | 30 Go SSD (Standard Persistent Disk) | Espace pour Docker images, logs, données |
| **OS** | Ubuntu 22.04 LTS | Support long terme, stable, bien documenté |
| **Région** | Proche de vous (ex: `europe-west1`) | Réduit la latence |

**Coût estimé** :
- ~$0.067/heure
- ~$48/mois si la VM tourne 24/7
- ~$16/mois si la VM tourne 8h/jour

### Configuration Économique (Pour Tests)

**Type de machine** : `e2-standard-1`

| Composant | Spécification |
|-----------|---------------|
| **vCPU** | 1 core |
| **RAM** | 4 Go |
| **Disque** | 20 Go SSD |
| **OS** | Ubuntu 22.04 LTS |

**Coût estimé** :
- ~$0.033/heure
- ~$24/mois si 24/7
- ~$8/mois si 8h/jour

⚠️ **Note** : Avec cette configuration, vous devrez peut-être réduire le nombre de réplicas dans `docker-compose.prod.yml` (changer `replicas: 2` à `replicas: 1`).

### Configuration Production (Pour Plus Tard)

**Type de machine** : `e2-standard-4` ou `n2-standard-4`

| Composant | Spécification |
|-----------|---------------|
| **vCPU** | 4 cores |
| **RAM** | 16 Go |
| **Disque** | 50-100 Go SSD |
| **OS** | Ubuntu 22.04 LTS |

**Coût estimé** :
- ~$0.134/heure (e2-standard-4)
- ~$96/mois si 24/7

## 🔍 Répartition des Ressources

Avec la configuration standard (`e2-standard-2`) :

| Service | CPU | RAM | Justification |
|---------|-----|-----|---------------|
| Traefik | 0.1 | 100 MB | Reverse proxy léger |
| Gateway | 0.2 | 200 MB | Point d'entrée, orchestrateur |
| Auth | 0.1 | 150 MB | Service simple |
| Project | 0.1 | 150 MB | Service simple |
| Billing | 0.1 | 150 MB | Service simple |
| Notification | 0.1 | 150 MB | Service simple |
| Analytics | 0.1 | 150 MB | Service simple |
| Jaeger | 0.2 | 500 MB | Collecte de traces |
| Prometheus | 0.3 | 1 GB | Collecte de métriques |
| Grafana | 0.1 | 200 MB | Dashboards |
| **Système** | 0.5 | 1 GB | OS, Docker, overhead |
| **Total** | ~2.0 | ~4 GB | Avec marge de sécurité |

> 💡 **Note** : Ces estimations sont approximatives. En production, surveillez l'utilisation réelle avec `docker stats` et ajustez si nécessaire.

## 📈 Scaling

### Vertical Scaling (Upgrade de la VM)

Si vous manquez de ressources :

1. **Arrêter la VM** dans GCP Console
2. **Modifier le type de machine** (ex: e2-standard-2 → e2-standard-4)
3. **Redémarrer la VM**

### Horizontal Scaling (Plus de Machines)

Pour un vrai cluster Swarm :

1. Créer plusieurs VMs
2. Initialiser Swarm sur la première (manager)
3. Joindre les autres avec `docker swarm join --token ...`

## 💰 Optimisation des Coûts

### 1. Arrêter la VM Quand Inutilisée

```bash
# Dans GCP Console
Compute Engine > VM instances > Arrêter
```

**Économie** : ~70% si vous utilisez la VM 8h/jour au lieu de 24/7

### 2. Utiliser des Preemptible VMs (Avancé)

Les VMs preemptibles sont ~80% moins chères mais peuvent être arrêtées par GCP à tout moment.

⚠️ **Non recommandé pour ce projet** car Docker Swarm nécessite une stabilité.

### 3. Réserver une Instance (Pour Production)

Si vous gardez la VM 24/7, réservez-la pour ~30% de réduction.

## 🔧 Commandes de Vérification

```bash
# Voir l'utilisation CPU et RAM
docker stats

# Voir l'espace disque
df -h

# Voir les processus
top
htop  # Si installé : sudo apt install htop

# Voir l'utilisation mémoire détaillée
free -h

# Voir l'utilisation disque par répertoire
du -sh /opt/cloudtaskhub /var/lib/docker
```

## 📊 Monitoring des Ressources

### Via GCP Console

1. Allez dans **Compute Engine > VM instances**
2. Cliquez sur votre VM
3. Onglet **Monitoring** : Graphiques CPU, RAM, disque, réseau

### Via Prometheus/Grafana

Une fois déployé, vous pouvez créer des dashboards Grafana pour surveiller :
- Utilisation CPU par service
- Utilisation RAM par service
- Requêtes/seconde
- Temps de réponse

## ⚠️ Limitations à Connaître

### Quotas GCP

Par défaut, GCP limite :
- **8 vCPU** par région (pour les comptes gratuits)
- **100 Go** de disque
- **1 To** de bande passante sortante/mois (gratuit)

Pour augmenter, allez dans **IAM & Admin > Quotas**.

### Limites Docker Swarm

- **1 manager** suffit pour ce projet
- Pour la haute disponibilité, il faut **3 ou 5 managers** (impair)
- Les workers peuvent être ajoutés sans limite théorique

## 🎯 Recommandation Finale

**Pour apprendre et tester** : `e2-standard-1` (1 vCPU, 4 Go RAM)  
**Pour un déploiement stable** : `e2-standard-2` (2 vCPU, 8 Go RAM)  
**Pour la production** : `e2-standard-4` ou plus (4+ vCPU, 16+ Go RAM)

---

**💡 Astuce** : Commencez avec `e2-standard-1` pour économiser, puis upgradez si nécessaire. GCP permet de changer le type de machine facilement.

