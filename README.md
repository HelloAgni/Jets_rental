# Fictional superjet rental API service.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![SQLalchemy](https://img.shields.io/badge/SQLAlchemy-D71F00.svg?style=for-the-badge&logo=SQLAlchemy&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)

---
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FHelloAgni%2FJets_rental&count_bg=%2379C83D&title_bg=%23555555&icon=teamspeak.svg&icon_color=%23E7E7E7&title=views&edge_flat=false)](https://hits.seeyoufarm.com)   
```bash
# Create and activate venv
# python -m venv venv
python3.10 -m venv venv
. venv/bin/activate

# Upgrade pip and install requirements
python -m pip install --upgrade pip
pip install -r dev-requirements.txt 

# Docker compose
# Move to folder infra
cd infra/
sudo docker compose -f docker-compose-v2.yaml up -d

http://localhost:8000/docs/
```
<img src="https://github.com/HelloAgni/Jets_rental/blob/main/jet_img/jet-1.png" width="1100" height="180">