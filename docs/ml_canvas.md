# ML Canvas - Previsão de Churn

## Problema

**Definição**: Prever quais clientes da empresa de telecomunicações têm risco de cancelar seu contrato (churn).

**Motivação**: Reduzir taxa de churn e melhorar retenção de clientes através de intervenções direcionadas.

**Impact**: Cada cliente retido = economia significativa em custos de aquisição.

## Stakeholders

| Stakeholder | Necessidade | Métrica |
|---|---|---|
| Gerente de Retenção | Identificar clientes em risco | Recall alto (poucos falsos negativos) |
| CFO | ROI de campanhas retentivas | Precisão da predição |
| Operações | Priorizar esforços | Ranking de probabilidade |
| Clientes | Melhores ofertas | Personalização |

## Dados

### Fonte
- **Dataset**: Telco Customer Churn (IBM)
- **Registros**: ~7,000 clientes
- **Features**: 19 características (demográficas, contrato, serviços)
- **Target**: Churn (Yes/No)

### Características Principais
- **Demográficas**: Age, Gender, Partner, Dependents
- **Contrato**: Tenure, Contract Type, Paperless Billing
- **Serviços**: Internet Service, Online Security, Tech Support, etc.
- **Financeiro**: Monthly Charges, Total Charges

## Modelagem

### Abordagem
1. **Baseline**: DummyClassifier, LogisticRegression
2. **Modelo Principal**: MLP (Multi-Layer Perceptron) com PyTorch
3. **Arquitetura**: Input (19) → 128 → 64 → 32 → 1 (sigmoid)

### Dados de Treinamento
- **Train**: 60%
- **Validation**: 15%
- **Test**: 25%

## Métricas

### Métricas de Negócio
| Métrica | Target | Importância |
|---|---|---|
| Recall | > 80% | Identificar máximo de clientes em risco |
| Precision | > 75% | Eficiência das intervenções |
| F1-Score | > 77% | Equilíbrio recall/precision |

### Métricas de ML
- **Accuracy**: Proporção de predições corretas
- **Precision**: Taxa de verdadeiros positivos entre preditos positivos
- **Recall**: Taxa de verdadeiros positivos identificados
- **ROC-AUC**: Tradeoff sensitivity/specificity
- **F1**: Média harmônica de precision e recall

## Restrições

- **Latência**: API deve responder em < 100ms
- **Disponibilidade**: 99.5% uptime
- **Compliance**: LGPD - privacidade de dados
- **Fairness**: Sem discriminação por gênero, raça, etc.

## SLOs

| SLO | Threshold |
|---|---|
| Model Accuracy | ≥ 80% |
| API Latency (p95) | < 100ms |
| API Availability | ≥ 99.5% |
| Predictions per second | ≥ 100 |

## Processo de Decisão

```
Probabilidade de Churn
    ↓
p > 0.7 → Alta Prioridade (Ofereça desconto agressivo)
0.5 < p ≤ 0.7 → Média Prioridade (Contato humanizado)
p ≤ 0.5 → Baixa Prioridade (Monitorar)
```

## Plano de Execução

1. **Semana 1**: Preparação de dados, EDA
2. **Semana 2**: Baseline, Feature Engineering
3. **Semana 3**: Treinamento MLP, Tuning
4. **Semana 4**: API, Testes, Deploy
5. **Semana 5**: Monitoramento, Iteração

## Riscos

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| Data drift | Alta | Alto | Monitoramento contínuo |
| Class imbalance | Alta | Médio | SMOTE, class weights |
| Model fairness | Média | Alto | Análise de bias por grupo |
| Integração | Baixa | Alto | Testes completos |

## Próximos Passos

1. Validar performance em produção
2. Coletar feedback do negócio
3. Implementar A/B testing de intervenções
4. Monitorar drift e retreinar periodicamente
