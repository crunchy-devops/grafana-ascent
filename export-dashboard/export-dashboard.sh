#!/bin/bash
HOST="http://localhost:3000"
KEY="votre_api_key_grafana"
DEST="./dashboards-git"

mkdir -p $DEST

# Récupérer tous les UIDs des dashboards
for uid in $(curl -s -H "Authorization: Bearer $KEY" $HOST/api/search?type=dash-db | jq -r '.[].uid'); do
    # Télécharger le JSON
    curl -s -H "Authorization: Bearer $KEY" $HOST/api/dashboards/uid/$uid | jq '.dashboard' > $DEST/$uid.json
done

# Git push
git add $DEST/*.json
git commit -m "Backup dashboards $(date)"
git push origin main