# MecâniQA Nuvem - Time Vitória

Projeto desenvolvido durante as aulas de **Computação em Nuvem**, com foco na construção de uma infraestrutura containerizada, monitorada e escalável para a aplicação MecâniQA, utilizando Docker, Docker Compose, Kubernetes, K9s, Terraform, Prometheus e Grafana.

**Repositório:** https://github.com/natzinho/mecaniQA-nuvem-vitoria

---

## 1. Objetivo

Construir uma infraestrutura para a aplicação MecâniQA, composta por uma API Java, banco de dados MySQL e serviço Redis.

O projeto evolui de uma execução individual dos serviços em containers para uma arquitetura com Docker Compose e, posteriormente, gerenciamento das aplicações por meio do Kubernetes.

Também foram implementados mecanismos de:

- Monitoramento e observabilidade.
- Coleta e visualização de métricas.
- Alertas para identificação de incidentes.
- Escalabilidade horizontal automática.
- Persistência de dados.
- Backup automatizado.
- Procedimentos operacionais de resposta a incidentes.
- Gestão de níveis de serviço.

## 2. Contexto

A MecâniQA é uma startup SaaS voltada para oficinas mecânicas.

A aplicação possui três serviços principais:

| Serviço | Responsabilidade |
|---|---|
| Java / Spring Boot | Aplicação principal e API |
| MySQL | Banco de dados transacional |
| Redis | Armazenamento em memória e cache |

A infraestrutura busca melhorar a organização, o gerenciamento de recursos e a capacidade de recuperação dos serviços por meio de containers, orquestração e monitoramento.

## 3. Arquitetura

A infraestrutura desenvolvida utiliza as seguintes tecnologias:

```text
MecâniQA
│
├── Java / Spring Boot
│   └── API
│
├── MySQL
│   ├── Banco de dados
│   └── Persistência com PVC
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
└── Cluster local Kind
    ├── Deployments
    ├── Pods
    ├── Services
    ├── ConfigMaps
    ├── PersistentVolumeClaims
    ├── CronJobs
    └── Horizontal Pod Autoscaler

Observabilidade
├── Simulador IoT
├── Prometheus
└── Grafana
    ├── Dashboards
    └── Alertas

Terraform
└── Infrastructure as Code
    └── Namespace Kubernetes
```

## 4. Estrutura do projeto

```text
mecaniQA-nuvem-vitoria/
│
├── docs/
│   ├── backup-e-recuperacao.md
│   ├── gestao-servicos.md
│   └── runbooks.md
│
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
│
├── iot-simulator/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── simulator.py
│
├── k8s/
│   ├── api-deployment.yaml
│   ├── api-service.yaml
│   ├── db-deployment.yaml
│   ├── db-service.yaml
│   ├── db-init-configmap.yaml
│   ├── db-pvc.yaml
│   ├── db-backup-pvc.yaml
│   ├── db-backup-cronjob.yaml
│   ├── redis-deployment.yaml
│   ├── redis-service.yaml
│   ├── iot-simulator-deployment.yaml
│   ├── iot-simulator-service.yaml
│   ├── iot-simulator-hpa.yaml
│   ├── metrics-server.yaml
│   ├── prometheus-configmap.yaml
│   ├── prometheus-deployment.yaml
│   ├── prometheus-rbac.yaml
│   ├── grafana-deployment.yaml
│   └── grafana-service.yaml
│
├── monitoring/
│   └── grafana/
│       ├── dashboards/
│       │   ├── cpu.json
│       │   ├── memoria.json
│       │   ├── erro-aplicacao.json
│       │   └── sucesso-aplicacao.json
│       │
│       └── provisioning/
│           ├── alerting/
│           │   └── alert-rules.yaml
│           ├── dashboards.yaml
│           └── datasources.yaml
│
├── terraform/
│   ├── providers.tf
│   └── namespace.tf
│
├── tests/
│
├── docker-compose.yml
├── kustomization.yaml
└── README.md
```

A estrutura apresenta os principais diretórios e arquivos do projeto. Alguns arquivos auxiliares de configuração e validação não estão listados individualmente.

## 5. Tecnologias utilizadas

| Tecnologia | Utilização |
|---|---|
| Docker | Criação e execução de containers |
| Docker Compose | Orquestração local |
| Kubernetes | Orquestração dos serviços |
| Kind | Cluster Kubernetes local |
| kubectl | Administração do Kubernetes |
| K9s | Visualização e administração do cluster |
| Terraform | Infrastructure as Code |
| Java 17 | Aplicação principal |
| Spring Boot | Desenvolvimento da API |
| MySQL 8.0 | Banco de dados |
| Redis 7 | Cache |
| Python | Simulador IoT |
| Prometheus | Coleta de métricas |
| Grafana | Dashboards e alertas |
| Git / GitHub | Versionamento do projeto |

## 6. Docker e Docker Compose

Cada serviço possui seu próprio Dockerfile, permitindo a criação de imagens independentes:

- `java/Dockerfile`
- `mysql/Dockerfile`
- `redis/Dockerfile`

A API utiliza Java 17 com a imagem base `eclipse-temurin:17-jdk-alpine`.

O arquivo `docker-compose.yml` realiza a orquestração local dos serviços:

- API Java.
- MySQL.
- Redis.

Os serviços compartilham uma rede interna, permitindo que a API acesse o banco de dados pelo nome do serviço `db`, sem depender de um endereço IP fixo.

O MySQL utiliza um volume nomeado:

```yaml
db_data:/var/lib/mysql
```

Esse volume mantém os dados fora do ciclo de vida do container.

### Executar com Docker Compose

Iniciar os serviços:

```bash
docker compose up -d
```

Verificar os containers:

```bash
docker compose ps
```

Interromper os serviços:

```bash
docker compose down
```

O volume nomeado do MySQL permanece armazenado após o comando `docker compose down`.

## 7. Kubernetes

Foi utilizado um cluster Kubernetes local com Kind.

Os principais recursos utilizados são:

| Recurso | Finalidade |
|---|---|
| Deployment | Gerenciamento dos Pods |
| Pod | Execução dos containers |
| Service | Comunicação entre serviços |
| ConfigMap | Disponibilização de configurações |
| PersistentVolumeClaim | Solicitação de armazenamento persistente |
| CronJob | Execução de tarefas agendadas |
| HPA | Escalabilidade horizontal automática |

A API utiliza um Service do tipo `NodePort`, permitindo acesso externo ao cluster local.

MySQL e Redis utilizam Services do tipo `ClusterIP`, mantendo a comunicação desses serviços dentro do cluster.

A API possui três réplicas na configuração original, enquanto MySQL e Redis possuem uma réplica cada.

Foi realizado um teste de auto-recuperação removendo manualmente um Pod da API. O Kubernetes criou automaticamente outro Pod para manter a quantidade desejada de réplicas.

### Namespaces

O projeto possui recursos organizados em namespaces diferentes:

- `mecaniqa`: utilizado pelo Terraform e pelos recursos de monitoramento, simulador e Grafana.
- `default`: utilizado pelos recursos originais da API, MySQL e Redis, além dos novos recursos de persistência e backup do MySQL.

O `kustomization.yaml` da raiz é um overlay destinado à implantação do Grafana no namespace `mecaniqa`.

## 8. Terraform - Infrastructure as Code

O Terraform foi utilizado para definir declarativamente recursos de infraestrutura.

Neste projeto, foi utilizado o provider do Kubernetes para criar o namespace:

```text
mecaniqa
```

O recurso está definido em:

```text
terraform/namespace.tf
```

Os comandos principais são:

```bash
terraform init
terraform plan
terraform apply
```

O `terraform plan` permite verificar as alterações previstas antes da aplicação.

## 9. Simulador IoT e Prometheus

Foi desenvolvido um simulador em Python para gerar dados sintéticos de três equipamentos, identificados por `sensor_id`:

- `sensor-01`
- `sensor-02`
- `sensor-03`

Cada equipamento tenta produzir três leituras a cada cinco segundos. Uma falha simulada interrompe aquela tentativa.

Os dados são independentes e aleatórios, não representando diagnósticos ou telemetria real.

O fluxo de monitoramento é:

```text
Simulador Python
       |
       v
Service iot-simulator:8000
       |
       v
Prometheus
       |
       v
Grafana
```

O Prometheus realiza a coleta das métricas a cada 15 segundos.

### Métricas disponibilizadas

| Métrica | Tipo | Significado |
|---|---|---|
| `iot_engine_temperature_celsius` | Gauge | Temperatura dos equipamentos |
| `iot_oil_pressure_bar` | Gauge | Pressão do óleo |
| `iot_vibration_meters_per_second_squared` | Gauge | Vibração dos equipamentos |
| `iot_sensor_readings_total` | Counter | Total de leituras individuais |
| `iot_sensor_last_update_timestamp_seconds` | Gauge | Horário da última aquisição bem-sucedida |
| `iot_sensor_operations_total` | Counter | Tentativas de aquisição por equipamento e resultado |

O simulador também utiliza variáveis de ambiente para controlar a execução:

| Variável | Padrão | Finalidade |
|---|---|---|
| `METRICS_PORT` | `8000` | Porta das métricas |
| `SIMULATION_INTERVAL_SECONDS` | `5` | Intervalo de simulação |
| `SENSOR_COUNT` | `3` | Quantidade de equipamentos |
| `SIMULATION_ERROR_PROBABILITY` | `0.1` | Probabilidade de falha simulada |

### Descoberta automática de Pods

O Prometheus utiliza `kubernetes_sd_configs` para descobrir automaticamente os Pods do simulador.

A descoberta considera:

- Namespace: `mecaniqa`.
- Label: `app=iot-simulator`.
- Porta nomeada: `metrics`.

Foram configuradas permissões específicas por RBAC para permitir a descoberta dos Pods.

Dessa forma, as réplicas do simulador podem ser identificadas e monitoradas individualmente.

## 10. Grafana - Dashboards e alertas

O Grafana foi integrado ao Prometheus para visualizar as métricas e acompanhar o comportamento da aplicação.

Foram desenvolvidos quatro dashboards:

| Dashboard | Indicador |
|---|---|
| CPU | Consumo de CPU do processo |
| Memória | Memória residente do processo |
| Erro na aplicação | Taxa de operações com erro |
| Sucesso na aplicação | Taxa de operações bem-sucedidas |

Os arquivos JSON dos dashboards estão em:

```text
monitoring/grafana/dashboards/
```

A configuração do datasource e dos dashboards está em:

```text
monitoring/grafana/provisioning/
```

As métricas de CPU e memória são obtidas por meio das métricas de processo exportadas pelo simulador Python.

Elas representam o processo do simulador, não o consumo total do cluster.

### Alertas configurados

Foram configuradas quatro regras de alerta no Grafana:

| Alerta | Condição |
|---|---|
| CPU acima de 80% da capacidade reservada | Consumo acima do limite definido |
| Memória acima de 85% da capacidade reservada | Consumo acima do limite definido |
| Taxa de erros acima de 20% | Percentual de erros superior a 20% |
| Taxa de sucesso abaixo de 80% | Percentual de sucesso inferior a 80% |

As regras possuem período de avaliação de cinco minutos.

Os alertas são provisionados pelo arquivo:

```text
monitoring/grafana/provisioning/alerting/alert-rules.yaml
```

O provisionamento mantém as configurações declaradas nos arquivos do repositório.

## 11. Metrics Server e escalabilidade automática (HPA)

O Metrics Server foi instalado no cluster Kubernetes para fornecer métricas de utilização de CPU e memória ao Horizontal Pod Autoscaler.

Manifesto:

```text
k8s/metrics-server.yaml
```

Verificação:

```bash
kubectl top nodes
kubectl top pods -n mecaniqa
```

### Horizontal Pod Autoscaler

Foi configurado um HPA para o Deployment `iot-simulator`.

Manifesto:

```text
k8s/iot-simulator-hpa.yaml
```

Configuração:

| Parâmetro | Valor |
|---|---|
| Réplicas mínimas | 1 |
| Réplicas máximas | 5 |
| Meta de CPU | 70% |
| Meta de memória | 80% |
| Estabilização para redução | 300 segundos |

O HPA utiliza as solicitações de recursos do Deployment para calcular a utilização percentual de CPU e memória.

Aplicação:

```bash
kubectl apply -f k8s/iot-simulator-hpa.yaml
```

Acompanhamento:

```bash
kubectl get hpa -n mecaniqa
kubectl get deployment iot-simulator -n mecaniqa
kubectl top pods -n mecaniqa
```

### Teste de carga

Foi realizado um teste de carga aumentando a quantidade de sensores simulados e reduzindo o intervalo entre as leituras.

Comando utilizado:

```bash
kubectl set env deployment/iot-simulator -n mecaniqa SENSOR_COUNT=100 SIMULATION_INTERVAL_SECONDS=0.1
```

Durante o teste, o HPA identificou o aumento da utilização de CPU e escalou automaticamente o simulador até o limite configurado de cinco réplicas.

Após o teste, os parâmetros originais foram restaurados:

```bash
kubectl set env deployment/iot-simulator -n mecaniqa SIMULATION_ERROR_PROBABILITY=0.1 SENSOR_COUNT=3 SIMULATION_INTERVAL_SECONDS=5
```

Após a redução da carga, o HPA também reduziu a quantidade de réplicas.

### Evidências do teste

Foram registradas as seguintes capturas de tela:

- `01-pods-consumo-recursos.png` - consumo de recursos dos Pods.
- `02-hpa-escalabilidade.png` - escalonamento até cinco réplicas.
- `03-deployment-cinco-replicas.png` - cinco réplicas disponíveis.
- `04-alertas-grafana-firing.png` - alertas em estado `Firing`.
- `05-hpa-reducao-de-replicas.png` - redução posterior de réplicas.

## 12. Persistência do MySQL

Para evitar a perda dos dados durante a substituição ou recriação do Pod, foi configurado armazenamento persistente no Kubernetes.

Foi criado o PersistentVolumeClaim:

```text
mysql-pvc
```

Configuração:

| Propriedade | Valor |
|---|---|
| Capacidade | 5 GiB |
| StorageClass | standard |
| Access Mode | ReadWriteOnce |
| Namespace | default |

O volume é montado no diretório:

```text
/var/lib/mysql
```

Esse é o diretório utilizado pelo MySQL para armazenar seus dados.

A configuração está definida em:

```text
k8s/db-pvc.yaml
k8s/db-deployment.yaml
```

A persistência foi validada com o PVC em estado `Bound` e o MySQL em execução.

## 13. Backup automático e recuperação

Além da persistência, foi configurado um volume separado para armazenar os arquivos de backup.

PVC:

```text
mysql-backup-pvc
```

Capacidade: 5 GiB.

O backup é realizado por um Kubernetes CronJob:

```text
mysql-backup
```

Manifesto:

```text
k8s/db-backup-cronjob.yaml
```

### Funcionamento

O CronJob utiliza o `mysqldump` para exportar o banco `mecaniqa`.

O agendamento configurado é:

```text
0 2 * * *
```

Ou seja, uma execução diária às 2h, conforme o fuso horário do cluster.

Os arquivos são armazenados no diretório:

```text
/backups
```

Os nomes incluem a data e o horário da execução.

### Validação realizada

Em 13/11/2026, foi executado um backup manual a partir do CronJob.

Resultado:

| Item | Resultado |
|---|---|
| Job | `mysql-backup-teste` |
| Status | Complete |
| Arquivo | `mecaniqa-20261113-145138.sql` |
| Tamanho | 1,3 KB |
| PVC do banco | Bound |
| PVC de backup | Bound |
| Verificação do arquivo | Concluída |

O arquivo foi localizado dentro do volume de backup e a verificação confirmou que não estava vazio.

O banco estava sem tabelas e registros durante o teste, por isso o arquivo gerado possui tamanho reduzido.

### Recuperação

O procedimento de recuperação está documentado em:

```text
docs/backup-e-recuperacao.md
```

A restauração pode ser realizada por meio da importação de um arquivo SQL no banco MySQL.

Exemplo:

```bash
kubectl exec -i -n default deploy/db -- sh -c 'mysql -uroot -p"$MYSQL_ROOT_PASSWORD" mecaniqa' < backup.sql
```

O arquivo `backup.sql` deve estar disponível no diretório local em que o comando for executado.

**Limitação:** os volumes utilizam armazenamento local provisionado pela StorageClass `standard`. Embora o volume de backup seja separado do volume do banco, ambos permanecem no mesmo cluster. A perda do cluster ou do nó pode comprometer os dois volumes.

Recomenda-se copiar periodicamente os arquivos de backup para armazenamento externo.

A geração e o armazenamento do backup foram validados, mas a restauração ainda não foi testada.

## 14. Runbooks operacionais

Foram elaborados quatro runbooks para orientar a equipe na identificação e resposta a incidentes.

Documento:

```text
docs/runbooks.md
```

Os procedimentos abrangem:

1. CPU acima de 80% da capacidade reservada.
2. Memória acima de 85% da capacidade reservada.
3. Taxa de erros da aplicação acima de 20%.
4. Taxa de sucesso da aplicação abaixo de 80%.

Os runbooks apresentam procedimentos de diagnóstico, investigação e ações de recuperação para cada situação.

Eles complementam os alertas do Grafana e auxiliam na padronização da resposta a incidentes.

## 15. Gestão de serviços - SLA, SLO, SLI, RTO e RPO

Foi elaborado um documento de gestão de serviços para estabelecer objetivos de disponibilidade e recuperação da plataforma.

Documento:

```text
docs/gestao-servicos.md
```

### SLA - Service Level Agreement

Meta proposta de disponibilidade:

**99,9%.**

Representa o nível de serviço estabelecido como referência para a plataforma.

### SLO - Service Level Objective

Objetivo interno de disponibilidade:

**99,95%.**

É uma meta mais rigorosa que o SLA.

### SLI - Service Level Indicator

Indicadores utilizados para acompanhar o serviço:

- Disponibilidade.
- Taxa de erros.
- Taxa de sucesso.
- Utilização de CPU.
- Utilização de memória.

Os indicadores de erro, sucesso, CPU e memória são acompanhados por meio do Prometheus e Grafana.

A disponibilidade foi definida como indicador, mas ainda não possui uma medição contínua específica implementada.

### RTO - Recovery Time Objective

Meta proposta de recuperação do serviço:

**Até 4 horas.**

Representa o tempo máximo desejado para recuperar o funcionamento após uma interrupção.

### RPO - Recovery Point Objective

Meta proposta de perda máxima de dados:

**Até 24 horas.**

Está relacionada ao agendamento diário de backups do MySQL.

Os valores de RTO e RPO são objetivos de planejamento e ainda dependem de testes de recuperação para comprovação.

## 16. K9s

O K9s foi utilizado para observar e administrar o cluster Kubernetes.

Com a ferramenta, foram acompanhados:

- Pods.
- Deployments.
- Services.
- Logs.
- Estado dos containers.
- Número de reinicializações.

Também foi realizado um teste de auto-recuperação, removendo um Pod da API e observando sua recriação automática pelo Deployment.

## 17. Documentação complementar

Os documentos técnicos do projeto estão organizados no diretório `docs/`:

| Documento | Conteúdo |
|---|---|
| `runbooks.md` | Procedimentos de diagnóstico e resposta a incidentes |
| `backup-e-recuperacao.md` | Persistência, backup e recuperação do MySQL |
| `gestao-servicos.md` | SLA, SLO, SLI, RTO e RPO |

## 18. Considerações finais

O projeto MecâniQA Nuvem demonstra a evolução de uma infraestrutura baseada em containers para um ambiente gerenciado pelo Kubernetes.

Foram implementados mecanismos de observabilidade, monitoramento, alertas, escalabilidade horizontal automática, persistência de dados e backups automatizados.

A utilização de Prometheus e Grafana permite acompanhar indicadores operacionais, enquanto o HPA ajusta automaticamente a quantidade de réplicas conforme o consumo de recursos.

Os PersistentVolumeClaims mantêm os dados do MySQL fora do ciclo de vida do Pod, e o CronJob automatiza a geração de backups.

Os runbooks e a documentação de gestão de serviços complementam a infraestrutura, estabelecendo procedimentos de resposta a incidentes e objetivos de disponibilidade e recuperação.

## 19. Equipe

**Time Vitória**

| Integrante | Função |
|---|---|
| Aeverton | Integrante da equipe |
| Caio | Integrante da equipe |
| Carlos Henrique | Integrante da equipe |
| Jonatas | Integrante da equipe |
| Maciel | Integrante da equipe |
| Natan | Integrante da equipe |

As funções de Piloto, Copiloto, QA, Arquiteto e Scrum Master são distribuídas conforme o rodízio definido pela equipe durante os encontros.

## 20. Repositório

Código-fonte:

https://github.com/natzinho/mecaniQA-nuvem-vitoria.git

---

**Atividade:** programa de trainee da MecâniQA - Automotive Tech.

**Disciplina:** Computação em Nuvem.
