# ⚡ Quick Start Guide

## 1️⃣ Instalação Rápida (5 minutos)

```bash
# Navegar para o projeto
cd tech-challenge-fase01

# Instalar dependências
make install

# Verificar instalação
python -c "import torch; import fastapi; print('✅ Tudo instalado!')"
```

## 2️⃣ Obter o Dataset (2 minutos)

### Opção A: Download Manual
1. Baixar em: https://www.kaggle.com/blastchar/telco-customer-churn
2. Colocar arquivo em: `data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv`

### Opção B: Script de Download (se tiver Kaggle CLI)
```bash
kaggle datasets download -d blastchar/telco-customer-churn -p data/raw/
unzip data/raw/telco-customer-churn.zip -d data/raw/
```

## 3️⃣ Treinar Modelo (10-15 minutos)

```bash
# Treinar pipeline completo
make train

# Ou executar script diretamente
python scripts/train_pipeline.py
```

O processo vai:
- ✅ Carregar dados
- ✅ Preprocessar (encoding, scaling)
- ✅ Treinar baselines
- ✅ Treinar MLP com early stopping
- ✅ Registrar em MLflow
- ✅ Salvar modelo

## 4️⃣ Rodar API (2 minutos)

```bash
# Terminal 1: Iniciar servidor
make run-api

# Terminal 2: Testar
curl http://localhost:8000/health

# Ou abrir no navegador
# http://localhost:8000/docs
```

## 5️⃣ Testes (3 minutos)

```bash
# Todos os testes com cobertura
make test

# Apenas smoke tests
make test-smoke

# Apenas testes de schema
pytest tests/test_schema.py -v

# Apenas testes de API
pytest tests/test_api.py -v
```

## 6️⃣ MLflow UI (1 minuto)

```bash
mlflow ui
```

Acesse: http://localhost:5000

## 📊 Exemplo de Requisição à API

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 35,
    "tenure": 12,
    "monthly_charges": 65.5,
    "total_charges": 786.0,
    "gender": "Male",
    "partner": "Yes",
    "dependents": "No",
    "phone_service": "Yes",
    "internet_service": "Fiber optic",
    "online_security": "No",
    "online_backup": "No",
    "device_protection": "No",
    "tech_support": "No",
    "streaming_tv": "No",
    "streaming_movies": "No",
    "contract": "Month-to-month",
    "paperless_billing": "Yes",
    "payment_method": "Electronic check"
  }'
```

### Resposta Esperada:
```json
{
  "prediction": 1,
  "probability": 0.75,
  "model_version": "0.1.0"
}
```

## 🔍 Estrutura de Pastas

```
tech-challenge-fase01/
├── src/                    # Código principal
│   ├── api/               # FastAPI endpoints
│   ├── data/              # Carregamento e preprocessamento
│   ├── features/          # Feature engineering
│   ├── models/            # MLP, baselines, trainer
│   └── utils/             # Logger, metrics
├── notebooks/             # EDA e modelagem
├── tests/                 # Testes pytest
├── scripts/               # Treinamento e API
├── data/                  # Dados (raw, processed)
├── models/                # Modelos treinados
├── docs/                  # Documentação
├── Makefile               # Comandos
└── pyproject.toml         # Dependências
```

## 🛠️ Troubleshooting

### Erro: "Dataset not found"
```bash
# Verificar arquivo
ls -la data/raw/

# Esperado:
# WA_Fn-UseC_-Telco-Customer-Churn.csv
```

### Erro: "Module not found"
```bash
# Reinstalar
make clean
make install
```

### API retorna 503 "Model not loaded"
```bash
# Treinar modelo primeiro
python scripts/train_pipeline.py

# Verificar arquivos
ls -la models/
ls -la data/processed/
```

### Erro de CUDA (se usando GPU)
```bash
# Forçar CPU
export CUDA_VISIBLE_DEVICES=""
make train
```

## 📈 Verificar Performance

Após treinar, verificar:

1. **Logs de Treinamento**
   ```bash
   tail -100 logs/app.log
   ```

2. **Métricas em MLflow**
   ```bash
   mlflow ui
   # Acesso: http://localhost:5000
   ```

3. **Modelo Salvo**
   ```bash
   ls -lah models/mlp_model.pth
   ```

## 🎯 Fluxo Recomendado

```
1. make install              # Instalar dependências
2. [Baixar dataset]          # Colocar em data/raw/
3. make train                # Treinar modelo
4. make run-api              # Rodar API (terminal novo)
5. mlflow ui                 # Visualizar (terminal novo)
6. make test                 # Rodar testes
7. Explorar notebooks        # 01_eda.ipynb, 02_modeling.ipynb
```

## 📚 Documentação Completa

- `README.md` - Overview do projeto
- `docs/ml_canvas.md` - ML Canvas
- `docs/model_card.md` - Model Card
- `docs/monitoring_plan.md` - Plano de Monitoramento
- `SETUP_COMPLETE.md` - Resumo de implementação

## ⏱️ Tempo Total Estimado

| Etapa | Tempo |
|-------|-------|
| Instalação | 5 min |
| Dataset | 2 min |
| Treinamento | 15 min |
| API | 2 min |
| Testes | 3 min |
| **TOTAL** | **~30 min** |

## ✅ Checklist Final

- [ ] Dependências instaladas (`pip list | grep torch`)
- [ ] Dataset em `data/raw/`
- [ ] Modelo treinado (`ls models/mlp_model.pth`)
- [ ] API rodando (`curl http://localhost:8000/health`)
- [ ] Testes passando (`make test`)
- [ ] MLflow ativo (`http://localhost:5000`)

## 🎉 Parabéns!

Você tem um sistema completo de ML em produção!

---

**Dúvidas?** Consulte os arquivos de documentação ou os comentários no código.

**Pronto para começar?** Execute: `make install`
