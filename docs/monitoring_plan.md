# Plano de Monitoramento - Churn Prediction

## 1. Métricas de Negócio

### Retention Metrics
| Métrica | Target | Frequência | Owner |
|---|---|---|---|
| Taxa de Churn Previsto | < 27% | Diária | Revenue Team |
| Clientes em Risco Identificados | > 80% recall | Semanal | Retention Team |
| Conversão de Intervenções | > 35% | Semanal | Marketing |
| ROI de Retenção | > 3x | Mensal | CFO |

### Customer Metrics
| Métrica | Target | Frequência |
|---|---|---|
| Satisfação com Ofertas | > 4.0/5 | Mensal |
| NPS de Retidos | > 50 | Trimestral |
| Churn Real vs Predito | Correlação > 0.8 | Mensal |

## 2. Métricas de ML

### Model Performance
| Métrica | Baseline | Target | Alert |
|---|---|---|---|
| Accuracy | 82.34% | ≥ 80% | < 78% |
| Precision | 78.45% | ≥ 75% | < 70% |
| Recall | 81.02% | ≥ 78% | < 75% |
| F1-Score | 79.71% | ≥ 77% | < 74% |
| ROC-AUC | 89.56% | ≥ 85% | < 82% |

### Inference Metrics
| Métrica | Target | Alert |
|---|---|---|
| API Latency (p50) | < 50ms | > 100ms |
| API Latency (p95) | < 100ms | > 200ms |
| API Availability | ≥ 99.5% | < 99% |
| Predictions/sec | ≥ 100 | < 50 |
| Error Rate | < 1% | > 5% |

## 3. Data Drift Detection

### Features a Monitorar

#### Statistical Tests
```python
Método: Kolmogorov-Smirnov (KS) Test
Threshold: KS-statistic > 0.1
Frequência: Diária
Ação: Alert se > threshold
```

#### Features Críticas
1. **Monthly Charges**: Alta correlação com churn
   - Alert se: Média > 110% do baseline
2. **Tenure**: Temporal trend importante
   - Alert se: Distribuição muda > 20%
3. **Contract Type**: Feature importante
   - Alert se: Proporção Month-to-month > 60%

### Monitoring Pipeline
```
Raw Data
    ↓
Data Drift Detector (KS test, wasserstein distance)
    ↓
Feature Importance Shift Detector
    ↓
Alert if drift > threshold
    ↓
Trigger retraining decision
```

## 4. Model Drift Detection

### Prediction Distribution Drift
```
Monitorar:
- Distribuição de P(churn) predita
- Proporção de positive predictions
- Mudanças no score médio

Alert se:
- P(churn) média > 35% (histórico 20-25%)
- Desvio padrão > 20% do baseline
```

### Performance Degradation
```
Calcular:
- Proxy labels (churn observado vs predito)
- Rolling window accuracy (últimos 1000 predictions)
- F1-score temporal

Alert se:
- Accuracy < 78%
- F1-score < 74%
- Trend negativo por 3 dias
```

## 5. Infraestrutura de Monitoramento

### Stack Recomendado
```
Data Collection: MLflow, Prometheus
Alerting: PagerDuty, Slack
Visualization: Grafana, Evidently AI
Retraining: Airflow/Prefect
```

### Dashboards

#### Dashboard 1: Business Metrics
- Taxa de churn predito vs real
- Conversão de intervenções
- ROI de retenção

#### Dashboard 2: Model Performance
- Accuracy, Precision, Recall (rolling)
- ROC-AUC temporal
- Confusion matrix

#### Dashboard 3: Data Quality
- Data drift scores
- Feature distributions
- Missing values

#### Dashboard 4: API Health
- Latency (p50, p95, p99)
- Error rate
- Throughput
- Uptime

### Alertas

#### Crítico (Escalação Imediata)
```
1. API Unavailable (> 5 min)
2. Model Accuracy < 75%
3. Data drift KS > 0.15
4. Error rate > 10%
```

#### Warning (Check Manual)
```
1. Accuracy trending down 3+ dias
2. Data drift KS > 0.10
3. Latency p95 > 150ms
4. Error rate > 5%
```

#### Info (Logging)
```
1. Daily accuracy/metrics
2. Prediction distribution
3. Feature importance changes
```

## 6. Plano de Retrain

### Triggers para Retrain

| Trigger | Threshold | Ação |
|---|---|---|
| Performance Degradation | Accuracy < 78% | Retrain automático |
| Data Drift | KS > 0.15 | Análise + retrain se drift confirmado |
| Temporal Decay | Trend negativo 3 dias | Manual review + retrain |
| Scheduled | 3 meses | Retrain automático com novos dados |

### Processo de Retrain

```
1. Coleta de Dados
   - Últimos 3 meses (~ 10k amostras)
   - Validar qualidade, detectar anomalias

2. Preparação
   - Aplicar mesmo preprocessing
   - Feature engineering idêntico
   - Split train/val/test

3. Treinamento
   - Hyperparameter sweep (300 trials)
   - Early stopping em validation set
   - Track com MLflow

4. Avaliação
   - Performance vs modelo anterior
   - Análise de fairness/bias
   - Teste em data histórico de teste

5. Validação
   - Shadow deployment (1-2 semanas)
   - Monitorar performance em produção
   - Comparar com modelo antigo

6. Deploy
   - Blue-green deployment
   - Gradual rollout (10% → 50% → 100%)
   - Rollback automático se performance cai

7. Documentação
   - Model card atualizado
   - Changelog do modelo
   - Lições aprendidas
```

## 7. Plano de Resposta a Incidentes

### Cenário 1: Accuracy Cai Abruptamente

```
Detecção: Accuracy < 75% por 1 hora

Resposta:
1. Alert PagerDuty → On-call Engineer
2. Análise rápida:
   - Verificar dados de entrada (drift?)
   - Verificar API (erros?)
   - Verificar dependências (conectividade?)
3. Se dados OK: Rollback modelo anterior
4. Investigate root cause:
   - Data drift?
   - Feature distribution mudou?
   - Bug no preprocessing?
5. Retrain com dados corrigidos
6. Deploy novo modelo
7. Post-mortem em 24h
```

### Cenário 2: Data Drift Detectado

```
Detecção: KS-test > 0.15

Resposta:
1. Log evidência de drift
2. Análise manual:
   - Qual feature driftou?
   - É esperado (sazonalidade)?
   - Vai afetar performance?
3. Opções:
   a) Continue monitorando (esperado)
   b) Retrain com novos dados
   c) Adaptar features/preprocessing
4. Document mudança
5. Ajustar thresholds se necessário
```

### Cenário 3: API Latency Alta

```
Detecção: p95 latency > 200ms

Resposta:
1. Check recursos do servidor
2. Verificar modelo size/inference time
3. Analisar querys lentes
4. Escalar horizontalmente se needed
5. Considerar model quantization
6. Caching de predictions
```

## 8. Experiência do Usuário

### Feedback Loop

```
Predictions
    ↓
Intervenções (desconto, oferta)
    ↓
Ação do Cliente
    ↓
Outcome (stay/churn)
    ↓
Atualizar labels
    ↓
Análise de Acurácia Real
```

### Pesquisas

- **Mensal**: Satisfação com ofertas (1000 clientes)
- **Trimestral**: NPS de retidos vs não-intervencionados
- **Semestral**: Análise qualitativa de razões de churn

## 9. Cronograma de Monitoramento

### Diária
- 08:00: Report automático de overnight
- 12:00: Check dashboards (business + tech)
- 17:00: End-of-day summary

### Semanal (Segunda)
- Review performance metrics
- Data quality analysis
- Model drift assessment
- Team sync on alerts

### Mensal
- Performance review vs targets
- ROI analysis
- Feature importance changes
- Fairness audit

### Trimestral
- Comprehensive model evaluation
- Retrain decision
- Architecture review
- Stakeholder sync

## 10. Escalação

### Primeiro Nível
- **Responsável**: Data Science Specialist
- **Disponibilidade**: 8h/dia
- **SLA**: 2h para investigação

### Segundo Nível
- **Responsável**: ML Engineering Lead
- **Disponibilidade**: 24/7
- **SLA**: 1h para críticos

### Terceiro Nível
- **Responsável**: VP Data & Analytics
- **Acionado**: Incidentes de negócio
- **SLA**: 30 min (escalação)

## 11. Documentação

Manter atualizado:
- [ ] Este plano (revisado mensalmente)
- [ ] Model Card (com cada novo deploy)
- [ ] Runbooks de resposta a incidentes
- [ ] Data dictionary (com mudanças)
- [ ] ML Canvas (com learnings)

## 12. Success Criteria

Model considerado "em sucesso" se:

✅ Accuracy ≥ 80% por 3 meses
✅ API availability ≥ 99.5%
✅ Conversão de retenção > 30%
✅ ROI > 3x
✅ Sem incidentes críticos
✅ Fairness audit passou
✅ Stakeholders satisfeitos
