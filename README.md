# Teste Python da Angular e-Commerce

Este é o projeto de teste Python da Angular e-Commerce usando Django e Postgres.


### Pré-requisitos
- [Docker](https://docs.docker.com/engine/install/) e [Docker Compose](https://docs.docker.com/compose/install/) instalados na sua máquina

1. Crie um arquivo docker-compose.yml e um arquivo .env no mesmo diretório, alterando as variáveis DATABASE_URL de acordo com as variáveis do POSTGRES.

# .env
```
DATABASE_URL=postgres://POSTGRES_USER:POSTGRES_PASSWORD@db:5432/PORSTGRES_DB
POSTGRES_PASSWORD=
POSTGRES_USER=
POSTGRES_DB=
```

# docker-compose.yml
```YAML
version: '3.9'
services:
  db:
    container_name: 'db'
    image: postgres
    env_file: .env
    ports:
      - 5434:5432
    volumes:
      - pg-data:/var/lib/postgresql/data
    healthcheck:
      test: ['CMD', 'pg_isready', '-h', 'db', '-p', '5432']
      interval: 2s
      timeout: 5s
      retries: 10
      start_period: 1s

  django:
    container_name: projects-api
    image: fabio08/angular-e_django_project:1.1
    env_file: .env
    tty: true
    ports:
      - 8000:8000
    depends_on:
      db:
        condition: service_healthy

volumes:
  pg-data:

```
2. execute o arquivo usando docker composer
```
$ docker-compose -f path/to/the/docker-compose.yml up -d
```
3. entre no container e crie um superuser
```
$ docker exec -it django bash
$ python3 manage.py createsuperuser
```
4. Agora você pode fazer login como administrador em http://127.0.0.1:8000/admin

# Sobre o Deploy
A aplicação é construída usando uma arquitetura de 3 camadas, consistindo de um balanceador de carga, dois servidores que executam a aplicação Django e um servidor de banco de dados PostgreSQL. Os servidores que executam a aplicação Django estão hospedados em instâncias do Amazon Elastic Compute Cloud (EC2) que executam contêineres Docker, localizados em sub-redes públicas diferentes e em AZs diferentes, garantindo alta disponibilidade. Os contêineres Docker servem como ponto de entrada para a aplicação Django. O servidor de banco de dados é hospedado em uma instância do Amazon Relational Database Service (RDS), localizada em uma sub-rede privada em outra Zona de Disponibilidade (AZ) protegida por um grupo de segurança que aceita somente requisições das instâncias EC2.

![deploy2d](https://i.imgur.com/6YlzCca.png)
![deploy3d](https://i.imgur.com/waQYSNV.png)

# Video

### TODO
- [ ] Deploy the application online
- [ ] Write Tests
- [ ] Record the Video