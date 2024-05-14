# /bin/bash   

cd ~/Projects/support     

git pull 
docker compose bouild &&docker compose down && docker compose up -d   

echo "🚀 Successfully deployed"