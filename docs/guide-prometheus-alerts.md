# 🚨 Guide : Alertes Prometheus

## 📋 Vue d'Ensemble

Ce guide explique comment utiliser les alertes Prometheus configurées pour CloudTaskHub.

## 🔔 Alertes Configurées

### 1. HighErrorRate (Taux d'Erreur Élevé)

**Déclenchement** : Quand le taux d'erreur (4xx + 5xx) dépasse 5% pendant 5 minutes

**Sévérité** : Warning

**Requête** :
```promql
sum(rate(http_requests_total{status=~"[45].."}[5m])) by (job)
/
sum(rate(http_requests_total[5m])) by (job)
* 100 > 5
```

**Action** : Vérifier les logs du service concerné

### 2. ServiceDown (Service Inaccessible)

**Déclenchement** : Quand un service n'est plus accessible pendant 2 minutes

**Sévérité** : Critical

**Requête** :
```promql
up{job=~"gateway|auth|project|billing|notification|analytics"} == 0
```

**Action** : Vérifier l'état du service avec `docker service ps`

### 3. HighLatency (Latence Élevée)

**Déclenchement** : Quand la latence P95 dépasse 1 seconde pendant 5 minutes

**Sévérité** : Warning

**Requête** :
```promql
histogram_quantile(0.95, 
  sum(rate(http_request_duration_seconds_bucket[5m])) by (le, job)
) > 1
```

**Action** : Vérifier la charge du service ou les problèmes de réseau

### 4. NoRequests (Aucune Requête)

**Déclenchement** : Quand un service ne reçoit aucune requête pendant 10 minutes (mais est accessible)

**Sévérité** : Warning

**Requête** :
```promql
sum(rate(http_requests_total[10m])) by (job) == 0
and
up{job=~"gateway|auth|project|billing|notification|analytics"} == 1
```

**Action** : Vérifier que le service est bien utilisé ou s'il y a un problème de routing

### 5. LowRequestRate (Taux de Requêtes Bas)

**Déclenchement** : Quand le Gateway reçoit moins de 0.01 requêtes/seconde pendant 10 minutes

**Sévérité** : Info

**Requête** :
```promql
sum(rate(http_requests_total[5m])) by (job) < 0.01
and
job == "gateway"
```

**Action** : Information seulement - peut indiquer une période d'inactivité normale

## 🔍 Vérifier les Alertes dans Prometheus

1. Allez sur `http://VOTRE_IP:9090`
2. Cliquez sur **Alerts** dans le menu
3. Vous verrez la liste des alertes et leur état :
   - **Inactive** : L'alerte n'est pas déclenchée
   - **Pending** : L'alerte est en attente (durée `for` pas encore atteinte)
   - **Firing** : L'alerte est active

## 🔧 Personnaliser les Alertes

Pour modifier les seuils ou ajouter de nouvelles alertes :

1. Éditez le fichier `prometheus-alerts.yml`
2. Modifiez les seuils dans les expressions PromQL
3. Redéployez la stack :
   ```bash
   docker stack deploy -c docker-compose.prod.yml cloudtaskhub --with-registry-auth
   ```

## 📊 Exemples de Personnalisation

### Changer le seuil d'erreur à 10%

```yaml
- alert: HighErrorRate
  expr: |
    sum(rate(http_requests_total{status=~"[45].."}[5m])) by (job)
    /
    sum(rate(http_requests_total[5m])) by (job)
    * 100 > 10  # Changé de 5 à 10
```

### Ajouter une alerte pour un service spécifique

```yaml
- alert: GatewayHighLatency
  expr: |
    histogram_quantile(0.95, 
      sum(rate(http_request_duration_seconds_bucket{job="gateway"}[5m])) by (le)
    ) > 2
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "Latence très élevée sur Gateway"
    description: "La latence P95 du Gateway est de {{ $value }}s"
```

## 🔗 Intégration avec Alertmanager (Optionnel)

Pour recevoir des notifications (email, Slack, etc.) quand les alertes se déclenchent :

1. **Installer Alertmanager** :
   - Ajoutez Alertmanager dans `docker-compose.prod.yml`
   - Configurez les notifications (email, Slack, etc.)

2. **Configurer Prometheus** :
   - Ajoutez la configuration Alertmanager dans `prometheus.yml`

Voir la documentation Prometheus pour plus de détails : https://prometheus.io/docs/alerting/latest/alertmanager/

## 📚 Ressources

- **Prometheus Alerting** : https://prometheus.io/docs/alerting/latest/overview/
- **PromQL Guide** : https://prometheus.io/docs/prometheus/latest/querying/basics/
- **Alerting Rules** : https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/

---

**Retour au tutoriel** : [Tutoriel Complet GCP](./tutoriel-complet-gcp.md#93-utiliser-prometheus-pour-les-métriques)

