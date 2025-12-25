# 📊 Guide : Configuration du Dashboard Grafana

## 🎯 Objectif

Créer un dashboard Grafana pour visualiser les métriques de vos microservices CloudTaskHub.

## 📋 Étapes de Configuration

### 1. Accéder à Grafana

1. Allez sur `http://VOTRE_IP:3000`
2. Connectez-vous avec :
   - **Username** : `admin`
   - **Password** : `admin`
3. Vous serez demandé de changer le mot de passe (optionnel pour les tests)

### 2. Configurer la Source de Données Prometheus

1. Dans Grafana, allez dans **Configuration** (icône engrenage) > **Data Sources**
2. Cliquez sur **Add data source**
3. Sélectionnez **Prometheus**
4. Configurez :
   - **URL** : `http://prometheus:9090`
   - Cliquez sur **Save & Test**
5. Vous devriez voir "Data source is working" ✅

### 3. Importer le Dashboard

#### Option A : Import depuis le fichier JSON

1. Allez dans **Dashboards** (icône carré) > **Import**
2. Cliquez sur **Upload JSON file**
3. Sélectionnez le fichier `grafana/dashboard-cloudtaskhub.json`
4. Cliquez sur **Load**
5. Sélectionnez la source de données Prometheus
6. Cliquez sur **Import**

#### Option B : Création manuelle

Si vous préférez créer le dashboard manuellement :

1. **Créer un nouveau dashboard** :
   - Dashboards > New > New Dashboard

2. **Ajouter un panneau "Requêtes HTTP par Service"** :
   - Add panel > Time series
   - Query : `sum(rate(http_requests_total{status=~"2.."}[5m])) by (job)`
   - Legend : `{{job}} - 2xx`
   - Ajoutez aussi les requêtes 4xx et 5xx

3. **Ajouter un panneau "Total Requêtes"** :
   - Add panel > Stat
   - Query : `sum(increase(http_requests_total[1h]))`

4. **Ajouter un panneau "Taux d'Erreur"** :
   - Add panel > Stat
   - Query : `sum(rate(http_requests_total{status=~"[45].."}[5m])) / sum(rate(http_requests_total[5m])) * 100`
   - Unit : Percent (0-100)

5. **Ajouter un tableau "Requêtes par Endpoint"** :
   - Add panel > Table
   - Query : `sum(rate(http_requests_total[5m])) by (handler, job, status)`

## 📊 Panneaux du Dashboard

Le dashboard inclut :

1. **Requêtes HTTP par Service** : Graphique montrant le taux de requêtes par service (2xx, 4xx, 5xx)
2. **Total Requêtes HTTP** : Nombre total de requêtes sur la dernière heure
3. **Taux d'Erreur** : Pourcentage d'erreurs (4xx + 5xx)
4. **Requêtes par Endpoint** : Tableau détaillé par endpoint, service et statut
5. **Latence par Service (P95)** : Latence au 95ème percentile
6. **Requêtes par Méthode HTTP** : Graphique en camembert (GET, POST, etc.)

## 🔧 Personnalisation

Vous pouvez personnaliser le dashboard :

- **Modifier les requêtes PromQL** : Cliquez sur un panneau > Edit
- **Ajouter de nouveaux panneaux** : Add panel
- **Changer les couleurs** : Panel options > Standard options > Color scheme
- **Modifier la période** : Utilisez le sélecteur de temps en haut à droite

## 📚 Requêtes PromQL Utiles

Voici quelques requêtes PromQL utiles pour vos dashboards :

```promql
# Taux de requêtes par service
sum(rate(http_requests_total[5m])) by (job)

# Requêtes réussies (2xx)
sum(rate(http_requests_total{status=~"2.."}[5m])) by (job)

# Requêtes en erreur (4xx + 5xx)
sum(rate(http_requests_total{status=~"[45].."}[5m])) by (job)

# Latence moyenne
avg(http_request_duration_seconds) by (job)

# Latence P95
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, job))

# Total de requêtes sur 1h
sum(increase(http_requests_total[1h]))
```

## 🎨 Thèmes et Apparence

Grafana supporte les thèmes clair et sombre :
- Cliquez sur votre profil (en bas à gauche) > Preferences
- Choisissez votre thème préféré

## 💡 Astuces

1. **Sauvegarder le dashboard** : Cliquez sur l'icône de sauvegarde (disquette) en haut
2. **Partager le dashboard** : Share > Get link ou Export
3. **Créer des alertes** : Panel > Alert > Create alert rule
4. **Ajouter des annotations** : Utilisez les annotations pour marquer les déploiements

## 🔗 Ressources

- **Documentation Grafana** : https://grafana.com/docs/
- **PromQL Guide** : https://prometheus.io/docs/prometheus/latest/querying/basics/
- **Dashboard Examples** : https://grafana.com/grafana/dashboards/

---

**Retour au tutoriel** : [Tutoriel Complet GCP](./tutoriel-complet-gcp.md#94-configurer-grafana-optionnel)

