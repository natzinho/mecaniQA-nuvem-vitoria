# Runbooks - MecâniQA Tech

## 1. Runbook - CPU acima de 80% da capacidade reservada

### 1.1 Objetivo

Orientar a equipe técnica na identificação e resolução de problemas relacionados ao consumo elevado de CPU nos Pods do simulador IoT.

### 1.2 Condição de acionamento

O alerta será disparado quando o consumo de CPU do processo do simulador ultrapassar 4% de um núcleo, equivalente a 80% dos 50m de CPU solicitados pelo contêiner, durante 5 minutos consecutivos.

### 1.3 Possíveis causas

- Aumento na quantidade de sensores simulados.
- Redução excessiva do intervalo entre as simulações.
- Aumento do processamento de operações.
- Sobrecarga dos Pods.
- Problemas de desempenho na aplicação.

### 1.4 Procedimento de diagnóstico

**Etapa 1 — Verificar os Pods**

Consultar o estado dos Pods do simulador:

```bash
kubectl get pods -n mecaniqa -l app=iot-simulator
```

Verificar se todos estão em execução e prontos.

**Etapa 2 — Verificar o consumo de recursos**

```bash
kubectl top pods -n mecaniqa -l app=iot-simulator
```

Comparar o consumo de CPU apresentado com os recursos solicitados e os limites configurados.

**Etapa 3 — Verificar o HPA**

```bash
kubectl get hpa -n mecaniqa
kubectl describe hpa iot-simulator-hpa -n mecaniqa
```

Verificar se o escalonamento automático está funcionando e se a quantidade de réplicas está próxima do limite máximo de 5.

**Etapa 4 — Consultar os logs**

```bash
kubectl logs -n mecaniqa -l app=iot-simulator --all-containers=true --prefix=true --since=15m
```

Procurar mensagens de erro ou indícios de processamento excessivo.

**Etapa 5 — Consultar o Prometheus**

Verificar a métrica utilizada pelo alerta:

```promql
max(100 * rate(process_cpu_seconds_total{job="iot-simulator"}[1m]))
```

Confirmar se o valor permanece acima de 4.

### 1.5 Ações corretivas

1. Se houver aumento excessivo de sensores, reduzir temporariamente a quantidade de simulações.
2. Se o intervalo estiver muito baixo, aumentar o intervalo entre as operações.
3. Verificar se o HPA está aumentando as réplicas automaticamente.
4. Se o HPA atingir o máximo de 5 Pods e a CPU continuar elevada, avaliar a necessidade de revisar os recursos disponíveis e a configuração de escalonamento.
5. Após qualquer alteração, acompanhar a aplicação e verificar novamente o consumo.

Exemplo de redução temporária da carga:

```bash
kubectl set env deployment/iot-simulator -n mecaniqa SENSOR_COUNT=3 SIMULATION_INTERVAL_SECONDS=5
```

Após a correção, acompanhar a atualização:

```bash
kubectl rollout status deployment/iot-simulator -n mecaniqa
```

### 1.6 Critérios para considerar o incidente resolvido

- O consumo de CPU permanece abaixo do limite do alerta.
- Os Pods estão em estado `Running` e prontos.
- O HPA apresenta métricas disponíveis e escalonamento adequado.
- O alerta do Grafana retorna ao estado Normal.
- A aplicação continua realizando as simulações.

### 1.7 Escalonamento

Se o problema persistir após as ações corretivas, encaminhar o incidente ao responsável pela infraestrutura e ao responsável pelo desenvolvimento do simulador.

Registrar o horário do incidente, os valores de consumo, os logs coletados, as ações realizadas e o resultado obtido.

### 1.8 Registro do incidente

Toda ocorrência deverá ser documentada para permitir a análise posterior da causa e o aprimoramento dos procedimentos operacionais.

---

## 2. Runbook - Memória acima de 85% da capacidade reservada

### 2.1 Objetivo

Orientar a equipe técnica na identificação e resolução de problemas relacionados ao consumo elevado de memória nos Pods do simulador IoT.

### 2.2 Condição de acionamento

O alerta será disparado quando a memória residente (RSS) do processo do simulador ultrapassar 27,2 MiB durante 5 minutos consecutivos.

Esse valor corresponde a 85% dos 32 MiB de memória solicitados pelo contêiner.

### 2.3 Possíveis causas

- Aumento na quantidade de sensores simulados.
- Crescimento do consumo de memória durante o processamento.
- Acúmulo de dados em memória.
- Possível vazamento de memória na aplicação.
- Sobrecarga dos Pods.

### 2.4 Procedimento de diagnóstico

**Etapa 1 — Verificar os Pods**

```bash
kubectl get pods -n mecaniqa -l app=iot-simulator
```

Verificar se os Pods estão em execução e prontos.

**Etapa 2 — Verificar o consumo de memória**

```bash
kubectl top pods -n mecaniqa -l app=iot-simulator
```

Comparar o consumo apresentado com os recursos configurados:

- Memória solicitada: 32 MiB.
- Limite de memória: 128 MiB.

**Etapa 3 — Consultar o HPA**

```bash
kubectl get hpa -n mecaniqa
kubectl describe hpa iot-simulator-hpa -n mecaniqa
```

Verificar a utilização de memória e se o HPA está realizando o escalonamento esperado.

**Etapa 4 — Consultar os logs**

```bash
kubectl logs -n mecaniqa -l app=iot-simulator --all-containers=true --prefix=true --since=15m
```

Procurar mensagens relacionadas a falta de memória, reinicializações ou falhas no processamento.

**Etapa 5 — Consultar o Prometheus**

Verificar a métrica utilizada pelo alerta:

```promql
max(process_resident_memory_bytes{job="iot-simulator"}) / 1024 / 1024
```

Confirmar se o valor permanece acima de 27,2 MiB.

### 2.5 Ações corretivas

1. Se houver aumento excessivo de sensores, reduzir temporariamente a quantidade de simulações.
2. Verificar se existe acúmulo desnecessário de dados na memória.
3. Avaliar os logs e o comportamento da aplicação para identificar possíveis vazamentos de memória.
4. Verificar se o HPA está aumentando a quantidade de Pods conforme a demanda.
5. Se necessário, solicitar ao responsável pela infraestrutura uma avaliação dos recursos disponíveis.

Exemplo de redução temporária da carga:

```bash
kubectl set env deployment/iot-simulator -n mecaniqa SENSOR_COUNT=3 SIMULATION_INTERVAL_SECONDS=5
```

Acompanhar a atualização:

```bash
kubectl rollout status deployment/iot-simulator -n mecaniqa
```

Se houver suspeita de acúmulo de memória no processo e as medidas anteriores não resolverem o problema, a equipe poderá avaliar uma reinicialização controlada do Deployment, após coletar os logs e as métricas necessários:

```bash
kubectl rollout restart deployment/iot-simulator -n mecaniqa
```

Essa ação é paliativa e não substitui a investigação de possíveis vazamentos de memória.

### 2.6 Critérios para considerar o incidente resolvido

- A memória residente do processo permanece abaixo de 27,2 MiB.
- Os Pods permanecem em estado `Running` e prontos.
- Não existem reinicializações recorrentes ou erros relacionados à memória.
- O HPA apresenta métricas disponíveis.
- O alerta do Grafana retorna ao estado Normal.
- A aplicação continua realizando as simulações.

### 2.7 Escalonamento

Se o consumo continuar elevado, encaminhar o incidente ao responsável pela infraestrutura e ao responsável pelo desenvolvimento do simulador.

Se houver suspeita de vazamento de memória, solicitar uma investigação específica no código da aplicação.

Registrar o horário do incidente, o consumo observado, os logs coletados, as ações realizadas e o resultado obtido.

### 2.8 Registro do incidente

Toda ocorrência deverá ser documentada para permitir a análise posterior da causa e o aprimoramento dos procedimentos operacionais.

---

## 3. Runbook - Taxa de erros da aplicação acima de 20%

### 3.1 Objetivo

Identificar e tratar o aumento de falhas nas operações realizadas pelo simulador IoT, evitando que erros persistentes comprometam a confiabilidade dos dados e do serviço.

### 3.2 Condição de acionamento

O alerta é acionado quando a taxa de erros ultrapassa **20% durante 5 minutos consecutivos**.

Expressão PromQL utilizada:

```promql
100 * sum(rate(iot_sensor_operations_total{job="iot-simulator",result="error"}[1m])) / clamp_min(sum(rate(iot_sensor_operations_total{job="iot-simulator"}[1m])), 1e-9)
```

O cálculo representa a proporção de operações com resultado `error` em relação ao total de operações registradas.

### 3.3 Possíveis causas

- Aumento de falhas durante a execução das operações dos sensores.
- Problemas de comunicação ou processamento.
- Sobrecarga dos Pods.
- Alteração inadequada nas configurações do simulador.
- Erros introduzidos após uma atualização da aplicação.
- Comportamento anormal na geração ou no processamento dos dados.

### 3.4 Procedimentos de diagnóstico

**Etapa 1 — Verificar os Pods do simulador**

```bash
kubectl get pods -n mecaniqa -l app=iot-simulator
```

Verifique se todos os Pods estão em estado `Running` e se estão prontos para receber operações.

**Etapa 2 — Consultar os logs da aplicação**

```bash
kubectl logs -n mecaniqa -l app=iot-simulator --all-containers=true --prefix=true --since=15m
```

Procure mensagens de erro, falhas de processamento ou comportamentos inesperados.

**Etapa 3 — Verificar os recursos e a escalabilidade**

```bash
kubectl top pods -n mecaniqa -l app=iot-simulator
kubectl get hpa -n mecaniqa
kubectl describe hpa iot-simulator-hpa -n mecaniqa
```

Verifique se existe consumo elevado de CPU ou memória e se o HPA está conseguindo ajustar a quantidade de réplicas.

**Etapa 4 — Verificar a configuração do Deployment**

```bash
kubectl describe deployment iot-simulator -n mecaniqa
```

Confira as variáveis de ambiente e as configurações da aplicação, especialmente `SIMULATION_ERROR_PROBABILITY`.

No ambiente do projeto, o manifesto define inicialmente essa probabilidade em `0.1` (10%). Verifique se houve alguma alteração antes de modificar essa configuração.

**Etapa 5 — Consultar a métrica no Prometheus**

Utilize a expressão abaixo no Prometheus ou no Grafana:

```promql
100 * sum(rate(iot_sensor_operations_total{job="iot-simulator",result="error"}[1m])) / clamp_min(sum(rate(iot_sensor_operations_total{job="iot-simulator"}[1m])), 1e-9)
```

Verifique se a taxa permanece acima de 20% e se o comportamento ocorre em todos os Pods ou está concentrado em algum deles.

### 3.5 Ações corretivas

1. Identificar nos logs quais operações estão apresentando falhas.
2. Verificar se a configuração de probabilidade de erro foi alterada indevidamente.
3. Se houver sobrecarga, avaliar a redução da quantidade de sensores ou o aumento do intervalo de simulação.
4. Caso o problema esteja relacionado a uma atualização, avaliar a reversão para uma versão anterior estável da aplicação.
5. Se necessário, solicitar apoio à equipe de desenvolvimento para investigar e corrigir a origem das falhas.

Não configure a probabilidade de erro como zero apenas para fazer o alerta desaparecer. A correção deve tratar a causa do problema e preservar a finalidade de simulação do projeto.

Após aplicar uma correção, acompanhe a atualização:

```bash
kubectl rollout status deployment/iot-simulator -n mecaniqa
```

### 3.6 Critérios de resolução

O incidente pode ser considerado resolvido quando:

- A taxa de erros permanecer abaixo de 20%.
- Os Pods estiverem em estado `Running` e prontos.
- Os logs não apresentarem falhas recorrentes.
- As operações dos sensores voltarem a apresentar comportamento esperado.
- O alerta retornar ao estado `Normal` no Grafana.

### 3.7 Escalonamento

Se o problema persistir, encaminhar o incidente à equipe de desenvolvimento e à equipe responsável pela infraestrutura.

Registrar as evidências coletadas, os horários do incidente, as ações executadas e os resultados obtidos.

### 3.8 Registro do incidente

Documentar cada ocorrência com:

- Data e horário de início e término.
- Taxa de erros observada.
- Pods afetados.
- Mensagens relevantes dos logs.
- Causa identificada ou hipótese investigada.
- Ações corretivas executadas.
- Responsável pelo atendimento.
- Resultado após a correção.

---

## 4. Runbook - Taxa de sucesso da aplicação abaixo de 80%

### 4.1 Objetivo

Identificar e corrigir situações em que a proporção de operações bem-sucedidas do simulador IoT fica abaixo do limite esperado, comprometendo a confiabilidade da execução e dos dados gerados.

### 4.2 Condição de acionamento

O alerta é acionado quando a taxa de operações com resultado `success` fica abaixo de **80% durante 5 minutos consecutivos**.

Expressão PromQL utilizada:

```promql
100 * sum(rate(iot_sensor_operations_total{job="iot-simulator",result="success"}[1m])) / clamp_min(sum(rate(iot_sensor_operations_total{job="iot-simulator"}[1m])), 1e-9)
```

O cálculo representa a proporção de operações bem-sucedidas em relação ao total de operações registradas pelo simulador.

### 4.3 Possíveis causas

- Aumento da quantidade de operações com falha.
- Problemas de comunicação ou processamento dos sensores.
- Sobrecarga de CPU ou memória nos Pods.
- Configuração inadequada da probabilidade de erros.
- Alterações recentes no código ou na configuração da aplicação.
- Instabilidade em serviços dos quais a aplicação depende.

### 4.4 Procedimentos de diagnóstico

**Etapa 1 — Verificar os Pods do simulador**

```bash
kubectl get pods -n mecaniqa -l app=iot-simulator
```

Verifique se todos os Pods estão em estado `Running` e prontos para executar suas operações.

**Etapa 2 — Consultar os logs da aplicação**

```bash
kubectl logs -n mecaniqa -l app=iot-simulator --all-containers=true --prefix=true --since=15m
```

Procure mensagens de erro, falhas de processamento e comportamentos inesperados.

**Etapa 3 — Verificar o consumo de recursos e o HPA**

```bash
kubectl top pods -n mecaniqa -l app=iot-simulator
kubectl get hpa -n mecaniqa
kubectl describe hpa iot-simulator-hpa -n mecaniqa
```

Avalie se os Pods estão próximos dos limites de CPU e memória e se o HPA está conseguindo ajustar a quantidade de réplicas.

**Etapa 4 — Verificar a configuração do Deployment**

```bash
kubectl describe deployment iot-simulator -n mecaniqa
```

Confira as variáveis de ambiente, especialmente `SIMULATION_ERROR_PROBABILITY`.

No ambiente do projeto, o manifesto define inicialmente essa probabilidade em `0.1` (10%). Verifique se houve alguma alteração antes de modificar a configuração.

**Etapa 5 — Consultar a métrica no Prometheus**

Utilize a expressão PromQL apresentada na seção 4.2 no Prometheus ou no Grafana.

Verifique se a taxa de sucesso permanece abaixo de 80% e se o comportamento ocorre em todos os Pods ou está concentrado em algum deles.

Também é importante comparar a taxa de sucesso com a taxa de erros para identificar se a redução está relacionada ao aumento de operações malsucedidas.

### 4.5 Ações corretivas

1. Identificar nos logs quais operações estão apresentando falhas.
2. Verificar se a configuração de probabilidade de erro foi alterada indevidamente.
3. Caso exista sobrecarga, avaliar a redução da quantidade de sensores ou o aumento do intervalo de simulação.
4. Se o problema estiver relacionado a uma atualização recente, avaliar a reversão para uma versão anterior estável.
5. Verificar a comunicação entre os componentes e a disponibilidade dos serviços dependentes.
6. Se necessário, solicitar apoio à equipe de desenvolvimento para investigar a origem das falhas.

Não configure a probabilidade de erro como zero apenas para elevar artificialmente a taxa de sucesso. A correção deve resolver a causa do problema e preservar a finalidade da simulação.

Após aplicar uma correção, acompanhe a atualização:

```bash
kubectl rollout status deployment/iot-simulator -n mecaniqa
```

### 4.6 Critérios de resolução

O incidente pode ser considerado resolvido quando:

- A taxa de sucesso permanecer igual ou acima de 80%.
- Os Pods estiverem em estado `Running` e prontos.
- Os logs não apresentarem falhas recorrentes.
- As operações dos sensores voltarem a apresentar comportamento esperado.
- O alerta retornar ao estado `Normal` no Grafana.

### 4.7 Escalonamento

Se o problema persistir, encaminhar o incidente à equipe de desenvolvimento e à equipe responsável pela infraestrutura.

Registrar as evidências coletadas, os horários do incidente, as ações executadas e os resultados obtidos.

### 4.8 Registro do incidente

Documentar cada ocorrência com:

- Data e horário de início e término.
- Taxa de sucesso observada.
- Pods afetados.
- Mensagens relevantes dos logs.
- Causa identificada ou hipótese investigada.
- Ações corretivas executadas.
- Responsável pelo atendimento.
- Resultado após a correção.
