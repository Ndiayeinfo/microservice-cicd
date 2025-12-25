#!/bin/bash
# Script de diagnostic pour Traefik Dashboard
# À exécuter sur la VM GCP

echo "=========================================="
echo "DIAGNOSTIC TRAEFIK DASHBOARD"
echo "=========================================="
echo ""

echo "1. Vérification du service Traefik..."
docker service ls | grep traefik
echo ""

echo "2. État détaillé du service..."
docker service ps cloudtaskhub_traefik --no-trunc
echo ""

echo "3. Ports exposés par le service..."
docker service inspect cloudtaskhub_traefik | grep -A 10 "Ports"
echo ""

echo "4. Ports en écoute sur la VM..."
sudo netstat -tlnp 2>/dev/null | grep -E ":(80|8080)" || sudo ss -tlnp 2>/dev/null | grep -E ":(80|8080)"
echo ""

echo "5. Configuration Traefik (labels)..."
docker service inspect cloudtaskhub_traefik | grep -A 30 "Labels"
echo ""

echo "6. Test local port 8080..."
curl -v http://localhost:8080/dashboard/ 2>&1 | head -20
echo ""

echo "7. Test local port 80 /dashboard..."
curl -v http://localhost/dashboard/ 2>&1 | head -20
echo ""

echo "8. Logs Traefik (dernières 30 lignes)..."
docker service logs cloudtaskhub_traefik --tail 30
echo ""

echo "9. Vérification des erreurs dans les logs..."
docker service logs cloudtaskhub_traefik --tail 100 | grep -i error
echo ""

echo "=========================================="
echo "DIAGNOSTIC TERMINÉ"
echo "=========================================="

