<h1 align="center">Fictional superjet rental service.</h1>

<div align="center">
  
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![SQLalchemy](https://img.shields.io/badge/SQLAlchemy-D71F00.svg?style=for-the-badge&logo=SQLAlchemy&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)  
</div>

<img src="https://github.com/HelloAgni/Jets_rental/blob/main/jet_img/jet-1.png" width="1100" height="170">

<div align="right">
  
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FHelloAgni%2FJets_rental&count_bg=%2379C83D&title_bg=%23555555&icon=teamspeak.svg&icon_color=%23E7E7E7&title=views&edge_flat=false)](https://hits.seeyoufarm.com)
</div>  

### Api for superjet rental service.
The application allows you to rent  superjet for a specific date, the minimum rental duration is one day.  
- It is possible to register users.
- Create and modify superjet objects according to the specified parameters.
- Book a rental for a specified date.
- Upload data from csv.

Data for preview and documentation available.  

---

***Fast Start with docker compose.*** 
```bash
# Clone
git clone <proj>

# Move to folder infra/
cd <proj>/infra/

sudo docker compose -f docker-compose-v2.yaml up -d
```
**Documentation:**  
http://127.0.0.1:8000/docs  

- **[Insert Test Data](http://127.0.0.1:8000/docs#/Load_data/insert_data_jet_rental_insert_data_jet_rental_post)**  
- **[Check Test Data](http://127.0.0.1:8000/docs#/Load_data/check_data_check_data_get)**

**Authorize test user:**
```
Username: super@mail.com  
Password: super  
```
---

***Dev local run with Postgres.***
```bash
# Copy .env to root project folder
cp infra/.env.local .env

# Create and activate venv
# python -m venv venv
python3.10 -m venv venv
. venv/bin/activate

# Upgrade pip and install requirements
python -m pip install --upgrade pip
pip install -r dev-requirements.txt

# If "fast start with docker compose" was used, delete the previous images/containers
sudo docker compose -f infra/docker-compose-v1.yaml up -d

# Make alembic migrations to DB
# From folder with alembic.ini
alembic upgrade head

# Run the server
uvicorn app.main:app --reload

# Super user and test user has been registered.
```
**Documentation:**  
http://127.0.0.1:8000/docs  

- **[Insert Test Data](http://127.0.0.1:8000/docs#/Load_data/insert_data_jet_rental_insert_data_jet_rental_post)**  
- **[Check Test Data](http://127.0.0.1:8000/docs#/Load_data/check_data_check_data_get)**

**Authorize test user:**
```
Username: super@mail.com  
Password: super  
```
