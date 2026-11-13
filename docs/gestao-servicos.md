# Gestão de Serviços - MecâniQA

## 1. Objetivo

Este documento estabelece os indicadores e objetivos de nível de serviço da plataforma MecâniQA, considerando disponibilidade, desempenho, monitoramento, escalabilidade e recuperação de falhas.

Os valores apresentados representam metas propostas para o projeto acadêmico, não um contrato comercial de prestação de serviços.

## 2. SLA - Service Level Agreement

O SLA representa o nível de serviço estabelecido como compromisso de disponibilidade.

**Disponibilidade estabelecida: 99,9%.**

Considerando um período de 30 dias, esse percentual permite aproximadamente 43 minutos e 12 segundos de indisponibilidade.

## 3. SLO - Service Level Objective

O SLO representa o objetivo interno de qualidade que a equipe pretende alcançar.

**Disponibilidade desejada: 99,95%.**

A meta é mais rigorosa que o SLA, permitindo aproximadamente 21 minutos e 36 segundos de indisponibilidade em um período de 30 dias.

## 4. SLI - Service Level Indicator

Os SLIs são os indicadores utilizados para acompanhar o comportamento da aplicação.

| Indicador | Objetivo |
|---|---|
| Disponibilidade | Percentual de tempo em que o serviço permanece acessível. |
| Taxa de erros | Identificar falhas nas requisições da aplicação. |
| Taxa de sucesso | Acompanhar o percentual de operações bem-sucedidas. |
| Uso de CPU | Identificar consumo elevado de processamento. |
| Uso de memória | Identificar consumo elevado de memória. |

O monitoramento utiliza Prometheus e Grafana, com alertas configurados para CPU, memória, taxa de erros e taxa de sucesso.

A disponibilidade é definida como indicador de serviço, mas sua medição contínua por uma verificação específica de disponibilidade ainda precisa ser implementada.

## 5. RTO - Recovery Time Objective

O RTO representa o tempo máximo desejado para recuperar o serviço após uma interrupção.

**Meta proposta: até 4 horas.**

A recuperação considera a identificação da falha, a restauração dos componentes necessários e a validação do funcionamento da aplicação.

Essa meta ainda precisa ser comprovada por um teste de recuperação cronometrado.

## 6. RPO - Recovery Point Objective

O RPO representa a quantidade máxima de dados que se admite perder em uma situação de recuperação.

**Meta proposta: até 24 horas.**

Foi implementado um CronJob Kubernetes para executar backups diários do banco MySQL, armazenando os arquivos SQL em um PersistentVolumeClaim separado.

O procedimento de geração e armazenamento do backup foi validado.

Entretanto, a recuperação ainda não foi testada. Além disso, como o volume de backup permanece no mesmo cluster, recomenda-se manter cópias externas para proteção contra perda do cluster ou do nó.

## 7. Monitoramento e resposta a incidentes

A infraestrutura utiliza:

- **Prometheus:** coleta e disponibilização de métricas.
- **Grafana:** visualização de indicadores e gerenciamento de alertas.
- **Kubernetes HPA:** escalabilidade horizontal automática.
- **Runbooks:** procedimentos operacionais para diagnóstico e resposta a incidentes.

Foram configurados quatro alertas:

1. CPU acima de 80% da capacidade reservada.
2. Memória acima de 85% da capacidade reservada.
3. Taxa de erros acima de 20%.
4. Taxa de sucesso abaixo de 80%.

## 8. Considerações finais

A plataforma MecâniQA possui mecanismos de monitoramento, alertas, escalabilidade automática, persistência de dados e backups automatizados.

As metas de SLA, SLO, RTO e RPO estabelecem referências para a gestão do serviço. A comprovação integral dessas metas depende da continuidade das medições e da realização de testes de recuperação e disponibilidade.
