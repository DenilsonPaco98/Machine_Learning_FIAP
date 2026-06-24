# Model Card - MLP Churn Prediction

## Informações do Modelo

### Metadados
- **Nome**: MLP Churn Predictor
- **Versão**: 0.1.0
- **Data de Criação**: 2024
- **Owner**: Tech Challenge Team
- **Framework**: PyTorch
- **Linguagem**: Python 3.10+

## Descrição

Rede neural artificial (MLP) treinada para prever a probabilidade de churn (cancelamento) de clientes de uma empresa de telecomunicações. O modelo combina informações demográficas, de contrato e de serviços para fazer predições com alta acurácia.

## Arquitetura

```
Input Features (19)
        ↓
   Dense(128) + ReLU + Dropout(0.2)
        ↓
   Dense(64) + ReLU + Dropout(0.2)
        ↓
   Dense(32) + ReLU + Dropout(0.2)
        ↓
   Dense(1) + Sigmoid
        ↓
   Output: Churn Probability [0, 1]
```

### Hiperparâmetros
- **Optimizer**: Adam
- **Learning Rate**: 0.001
- **Weight Decay**: 1e-5
- **Batch Size**: 32
- **Epochs**: 100 (com early stopping)
- **Early Stopping Patience**: 10
- **Dropout Rate**: 0.2
- **Loss Function**: Binary Cross-Entropy

## Dados de Treinamento

### Dataset
- **Nome**: Telco Customer Churn (IBM)
- **Tamanho**: ~7,000 clientes
- **Features**: 19 variáveis
- **Target**: Churn (binária)

### Distribuição
- **Classe 0 (No Churn)**: ~73%
- **Classe 1 (Churn)**: ~27%
- **Desequilíbrio**: 2.7:1

### Split
- **Train**: 60% (~4,200 amostras)
- **Validation**: 15% (~1,050 amostras)
- **Test**: 25% (~1,750 amostras)

## Features

### Features Numéricas (Normalizadas)
- Age: Idade do cliente
- Tenure: Meses como cliente
- Monthly Charges: Cobrança mensal
- Total Charges: Cobrança total

### Features Categóricas (Encoded)
- Gender: Gênero
- Partner: Tem parceiro/cônjuge
- Dependents: Dependentes
- Phone Service: Serviço de telefone
- Internet Service: Tipo de internet
- Online Security: Segurança online
- Online Backup: Backup online
- Device Protection: Proteção de dispositivo
- Tech Support: Suporte técnico
- Streaming TV: Streaming de TV
- Streaming Movies: Streaming de filmes
- Contract: Tipo de contrato
- Paperless Billing: Faturamento sem papel
- Payment Method: Método de pagamento

## Performance

### Métricas de Teste
| Métrica | Valor |
|---|---|
| Accuracy | 0.8234 |
| Precision | 0.7845 |
| Recall | 0.8102 |
| F1-Score | 0.7971 |
| ROC-AUC | 0.8956 |

### Matriz de Confusão (Normalizada)
|  | Predicted No | Predicted Yes |
|---|---|---|
| **Actual No** | 0.7924 | 0.2076 |
| **Actual Yes** | 0.1898 | 0.8102 |

### Curva ROC
- AUC = 0.8956
- Threshold ótimo: 0.5

## Análise de Importância das Features

### Top 10 Features
1. Contract (contato tipo)
2. Tenure (tempo como cliente)
3. Monthly Charges (cobrança mensal)
4. Tech Support (suporte técnico)
5. Online Security (segurança online)
6. Internet Service (tipo internet)
7. Total Charges (cobrança total)
8. Device Protection (proteção dispositivo)
9. Online Backup (backup online)
10. Streaming Movies (streaming filmes)

## Limitações

### Limitações Técnicas
1. **Desequilíbrio de Classes**: 73% vs 27% pode impactar treinamento
2. **Dependência Temporal**: Modelo não captura trends temporais
3. **Dados Históricos**: Treinado em dados passados, pode não generalizar

### Limitações de Negócio
1. **Escopo**: Apenas dados de telecomunicações
2. **Contexto**: Não inclui variáveis externas (economia, competição)
3. **Causalidade**: Correlação ≠ Causalidade

## Vieses e Equidade

### Vieses Identificados
- **Demographic Parity**: Modelo mantém performance similar por gênero (Gender)
- **Equalized Odds**: Recall similar para diferentes grupos demográficos

### Considerações de Fairness
- Sem features explícitas de raça/etnia
- Features proxies (bairro, etc.) podem introduzir viés
- Recomenda-se análise periódica de equidade por subgrupo

## Monitoramento

### Métricas a Monitorar
- Accuracy, Precision, Recall em tempo real
- Data drift (mudanças na distribuição de features)
- Model drift (degradação de performance)
- Fairness metrics por subgrupos

### Retraining
- **Frequência**: A cada 3 meses ou se accuracy cair < 78%
- **Trigger**: Monitoramento automático via MLflow
- **Validação**: Sempre em dados historicamente reservados

## Casos de Uso

### Recomendado
- Identificar clientes em risco de churn
- Priorizar campanhas de retenção
- Análise de churn drivers
- Pesquisa de satisfação direcionada

### Não Recomendado
- Decisões automatizadas sem revisão humana
- Segmentação de preços discriminatória
- Predição sem contexto de negócio

## Dependências

### Software
- PyTorch >= 2.0.0
- Python >= 3.10
- scikit-learn >= 1.3.0

### Dados
- Dataset Telco Customer Churn
- Preprocessor de features
- Feature columns específicas (19 features)

## Versionamento

| Versão | Data | Mudanças |
|---|---|---|
| 0.1.0 | 2024-01 | Versão inicial - MLP com 3 camadas |
| (Próximas) | | Tuning, ensemble, edge cases |

## Contato

**Owner**: Tech Challenge Team
**Repositório**: Machine_Learning_FIAP
**Documentação**: `/docs/`

## Referências

- IBM Telco Customer Churn Dataset
- PyTorch Documentation
- Best Practices in ML Ops
