#!/bin/bash
echo "Copying IBM Cloud apikey into development environment..."
docker cp ~/.bluemix/apikey-team.json recommendations:/home/vscode 
docker exec recommendations sudo chown vscode:vscode /home/vscode/apikey-team.json
echo "Complete"
