FROM n8nio/n8n:latest

# Copie ton export de workflow dans le conteneur
COPY ticket_automation.json /home/node/workflows/ticket_automation.json

# Crée le dossier de travail
RUN mkdir -p /home/node/.n8n

# (Optionnel) Copie un workflow d’import ou un script init.sh si besoin
# Mais ici, on se contente de le monter dans /home/node/workflows
