# MecâniQA Nuvem — Time Vitória

Projeto desenvolvido durante as aulas de **Computação em Nuvem**, com foco na construção de uma infraestrutura containerizada para a aplicação MecâniQA, utilizando **Docker, Docker Compose, Kubernetes, K9s e Terraform**.

## Objetivo

Construir uma base de infraestrutura para a aplicação MecâniQA, composta por uma API Java, um banco de dados MySQL e um serviço Redis.

O projeto evolui de uma execução individual dos serviços em containers para uma arquitetura com **orquestração local utilizando Docker Compose** e, posteriormente, **gerenciamento das aplicações com Kubernetes**.

Também foi utilizada a abordagem de **Infrastructure as Code (IaC)** com Terraform para definir recursos de infraestrutura de forma declarativa.

## Contexto

A MecâniQA é uma startup SaaS voltada para oficinas mecânicas. A aplicação possui uma arquitetura composta por:

* **Java** — aplicação principal e API
* **MySQL** — banco de dados transacional
* **Redis** — armazenamento em memória e cache

A infraestrutura anterior apresentava dificuldades relacionadas ao consumo de recursos e à estabilidade dos serviços. O projeto busca estabelecer uma base mais organizada e resiliente por meio do uso de containers e ferramentas de orquestração.

## Arquitetura

A infraestrutura desenvolvida está organizada da seguinte forma:

```text
MecâniQA
│
├── Java / Spring Boot
│   └── API
│
├── MySQL
│   └── Banco de dados
│
└── Redis
    └── Cache / armazenamento em memória

Docker
    └── Containers e imagens

Docker Compose
    └── Orquestração local
        ├── API
        ├── MySQL
        └── Redis

Kubernetes
    └── Cluster local
        ├── Deployments
        ├── Pods
        ├── Services
        └── ConfigMap

K9s
    └── Observação e administração do cluster

Terraform
    └── Infrastructure as Code
        └── Namespace Kubernetes
```

## Estrutura do projeto

```text
mecaniQA-nuvem-vitoria/
├── java/
│   └── Dockerfile
│
├── mysql/
│   └── Dockerfile
│
├── redis/
│   └── Dockerfile
│
├── mecaniqa-api/
│   ├── pom.xml
│   └── src/
│       └── main/
│           ├── java/
│           └── resources/
│
├── k8s/
│   ├── api-deployment.yaml
│   ├── api-service.yaml
│   ├── db-deployment.yaml
│   ├── db-init-configmap.yaml
│   ├── db-service.yaml
│   ├── redis-deployment.yaml
│   └── redis-service.yaml
│
├── terraform/
│   ├── providers.tf
│   └── namespace.tf
│
├── docker-compose.yml
└── README.md
```

## Serviços e portas

| Serviço    | Porta |
| ---------- | ----: |
| Java / API |  8080 |
| MySQL      |  3306 |
| Redis      |  6379 |

No Kubernetes, a API é disponibilizada por meio de um **Service do tipo NodePort**, enquanto MySQL e Redis utilizam **Services do tipo ClusterIP**, mantendo esses serviços disponíveis internamente no cluster.

## Dockerfiles

Cada serviço possui seu próprio `Dockerfile`, permitindo a criação de imagens independentes:

* `java/Dockerfile`
* `mysql/Dockerfile`
* `redis/Dockerfile`

### Java

A API utiliza **Java 17** com a imagem base:

```text
eclipse-temurin:17-jdk-alpine
```

A aplicação é executada na porta `8080`.

### MySQL

O banco de dados utiliza **MySQL 8.0** e a porta `3306`.

### Redis

O Redis utiliza a imagem **Redis 7 Alpine** e a porta `6379`.

## Docker Compose

O arquivo `docker-compose.yml` realiza a orquestração local dos três serviços:

* API Java
* MySQL
* Redis

O Docker Compose também fornece uma rede interna para os serviços. Dessa forma, a API pode acessar o banco de dados utilizando o nome do serviço:

```text
db
```

Em vez de utilizar um endereço IP fixo.

O MySQL utiliza um **volume nomeado** para manter os dados fora do ciclo de vida do container:

```text
db_data:/var/lib/mysql
```

## Kubernetes

Após a etapa de orquestração com Docker Compose, os serviços foram convertidos para recursos declarativos do Kubernetes.

Foi utilizado um **cluster Kubernetes local com Kind**.

Os principais recursos utilizados foram:

* **Deployments** — mantêm os Pods desejados em execução.
* **Pods** — unidades de execução dos containers no Kubernetes.
* **Services** — fornecem comunicação estável entre os serviços.
* **ConfigMap** — utilizado para disponibilizar o script inicial do MySQL.

### Deployments

A API possui três réplicas:

```yaml
replicas: 3
```

MySQL e Redis possuem uma réplica cada.

O Deployment da API foi testado removendo manualmente um Pod. O Kubernetes criou automaticamente outro Pod para manter a quantidade desejada de três réplicas.

### Services

A comunicação entre os serviços utiliza os nomes dos Services:

```text
api
db
redis
```

A API utiliza um Service **NodePort** para permitir acesso externo ao cluster local.

MySQL e Redis utilizam Services **ClusterIP**, mantendo a comunicação desses serviços dentro do cluster.

### MySQL

O banco é configurado com:

```text
MYSQL_ROOT_PASSWORD=123456
MYSQL_DATABASE=mecaniqa
```

Um ConfigMap fornece o script de inicialização:

```text
init.sql
```

responsável pela criação do banco `mecaniqa`.

## K9s

O **K9s** foi utilizado para observar e administrar o cluster Kubernetes.

Com ele foram verificadas informações como:

* Pods
* Deployments
* Services
* Logs
* Estado dos containers
* Número de reinicializações

Também foi realizado um teste de auto-recuperação removendo um Pod da API e observando sua recriação automática pelo Deployment.

Durante a inspeção, os Pods permaneceram em estado:

```text
Running
```

sem reinicializações.

## Terraform

Foi utilizado **Terraform** como ferramenta de Infrastructure as Code.

Neste projeto, o Terraform utiliza o provider do Kubernetes para definir declarativamente um namespace:

```text
mecaniqa
```

O recurso está definido em:

```text
terraform/namespace.tf
```

A infraestrutura é inicializada e gerenciada por meio de:

```bash
terraform init
terraform plan
terraform apply
```

Após a aplicação da configuração, o namespace `mecaniqa` foi criado no cluster Kubernetes.

O `terraform plan` também foi utilizado posteriormente para verificar que a infraestrutura existente correspondia à configuração declarada.

## Tecnologias

* Docker
* Docker Compose
* Kubernetes
* Kind
* kubectl
* K9s
* Terraform
* Java 17
* Spring Boot
* MySQL 8.0
* Redis 7
* Git
* GitHub

## Execução

### Docker Compose

Para iniciar os serviços utilizando Docker Compose:

```bash
docker compose up -d
```

Para verificar os containers:

```bash
docker compose ps
```

Para interromper os serviços:

```bash
docker compose down
```

O volume nomeado do MySQL permanece armazenado após o `docker compose down`.

### Kubernetes

Com o cluster Kubernetes local em execução, os manifests podem ser aplicados utilizando:

```bash
kubectl apply -f k8s/
```

Para verificar os Pods:

```bash
kubectl get pods
```

Para verificar os Deployments:

```bash
kubectl get deployments
```

Para verificar os Services:

```bash
kubectl get services
```

## Equipe

**Time Vitória**

| Integrante      | Função               |
| --------------- | -------------------- |
| Aeverton        | Integrante da equipe |
| Caio            | Integrante da equipe |
| Carlos Henrique | Integrante da equipe |
| Jonatas         | Integrante da equipe |
| Maciel          | Integrante da equipe |

As funções de Piloto, Copiloto, QA, Arquiteto e Scrum Master são distribuídas de acordo com o rodízio definido pela equipe durante os encontros.

## Repositório

Código-fonte do projeto:

```text
https://github.com/natzinho/mecaniQA-nuvem-vitoria.git
```

## Atividade

A atividade faz parte do programa de trainee da **MecâniQA - Automotive Tech** e tem como objetivo desenvolver conhecimentos práticos em **virtualização, containers, imagens Docker, orquestração, Kubernetes, observabilidade e Infrastructure as Code**.

O projeto acompanha a evolução da infraestrutura desde o isolamento dos serviços em containers até seu gerenciamento declarativo em um cluster Kubernetes.

