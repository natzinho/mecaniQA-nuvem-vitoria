
# Persistência, Backup e Recuperação — MecâniQA

## 1. Persistência do banco de dados

Foi configurado um PersistentVolumeClaim (PVC) chamado `mysql-pvc`, com capacidade de 5 GiB e StorageClass `standard`.

O volume é montado no diretório `/var/lib/mysql` do contêiner MySQL, mantendo os dados armazenados independentemente do ciclo de vida do Pod.

## 2. Backup automático

Foi criado um segundo PVC, chamado `mysql-backup-pvc`, também com capacidade de 5 GiB, destinado exclusivamente aos arquivos de backup.

O backup é executado por um Kubernetes CronJob chamado `mysql-backup`, com agendamento diário às 2h da manhã, conforme o fuso horário do cluster.

A ferramenta `mysqldump` realiza a exportação do banco `mecaniqa`, incluindo rotinas e triggers.

Os arquivos são armazenados em `/backups`, com nomes que incluem data e horário da execução.

## 3. Validação realizada

Em 13/11/2026, foi executado um backup manual a partir do CronJob.

Resultados:
- Job: `mysql-backup-teste`.
- Status: `Complete`.
- Arquivo gerado: `mecaniqa-20261113-145138.sql`.
- Tamanho: 1,3 KB.
- PVC do banco: `Bound`.
- PVC de backup: `Bound`.
- Verificação do arquivo no volume: concluída com sucesso.

O banco estava sem tabelas e registros durante o teste. Por isso, o arquivo gerado é pequeno.

## 4. Procedimento de recuperação

Para restaurar um backup:

1. Identificar o arquivo SQL desejado no volume de backups.
2. Copiar o arquivo para o ambiente de administração.
3. Garantir que o MySQL esteja em execução.
4. Executar a importação:

```bash
kubectl exec -i -n default deploy/db -- sh -c 'mysql -uroot -p"$MYSQL_ROOT_PASSWORD" mecaniqa' < backup.sql
```

O arquivo `backup.sql` deve estar no diretório local em que o comando for executado.

**Atenção:** a restauração deve ser realizada com cuidado, preferencialmente em ambiente de teste antes de afetar dados de produção.

## 5. Limitações e considerações

- Os volumes utilizam armazenamento local provisionado pela StorageClass `standard`.
- O PVC de backup é separado do PVC do banco, mas ambos permanecem no mesmo cluster.
- A perda do cluster ou do nó pode comprometer os dois volumes.
- Recomenda-se copiar periodicamente os arquivos de backup para armazenamento externo ao cluster.
- O procedimento de geração do backup foi validado, mas a restauração ainda não foi testada.

## 6. Objetivos de recuperação

Para o projeto, são definidos como objetivos propostos:

- RPO: até 24 horas, considerando a execução diária dos backups.
- RTO: até 4 horas, como meta de recuperação do serviço.

Esses valores são metas de planejamento e ainda precisam ser comprovados por testes de recuperação.

