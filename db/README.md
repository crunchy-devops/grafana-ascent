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
pip3 install psycopg2-binary
```
## Create service
```shell
cd 
cd grafana-ascent/db
sudo cp grafana-simulator.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable grafana-simulator
sudo systemctl start grafana-simulator
sudo systemctl status grafana-simulator
setenforce 0  
journalctl -u grafana-simulator -f

```
