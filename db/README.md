# DB

Run the following command to create the database:
```shell
psql -U admin -h localhost -p 5432 -d grafana -f e-commerce.sql
```
ou via pgAdmin ou jetbrains

## Install psycopg2-binary 
```shell
python3 -m venv venv 
sudo dnf install -y python3-pip
source venv/bin/activate
pip3 install psycopg2-binary
```
Changer les paramètres de la base de données dans le fichier simulator.py

## Create service
```shell
cd 
cd grafana-ascent/db
sudo setenforce 0
sudo cp grafana-simulator.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable grafana-simulator
sudo systemctl start grafana-simulator
sudo systemctl status grafana-simulator

journalctl -u grafana-simulator -f

```
