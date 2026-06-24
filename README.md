# Tech Challenge Fase 01 - Previsão de Churn com MLP PyTorch

## 📋 Descrição do Projeto

Pipeline completo de machine learning para previsão de churn de clientes usando rede neural MLP implementada em PyTorch. O projeto inclui:

- **Pré-processamento de dados**: Normalização, encoding de variáveis categóricas
- **Engenharia de features**: Seleção e construção de features
- **Modelos de baseline**: DummyClassifier e LogisticRegression
- **Modelo principal**: MLP com PyTorch e early stopping
- **API REST**: FastAPI para servir predições
- **Tracking**: MLflow para experimentos
- **Testes**: Cobertura com pytest
- **Documentação**: ML Canvas, Model Card, Plano de Monitoramento

## 🏗️ Arquitetura

```
tech-challenge-fase01/
├── src/
│   ├── api/          # FastAPI endpoints
│   ├── data/         # Carregamento e pré-processamento
│   ├── features/     # Engenharia de features
│   ├── models/       # MLP, baselines e treinamento
│   ├── utils/        # Logging e métricas
│   └── config.py     # Configurações globais
├── notebooks/        # EDA e modelagem exploratória
├── tests/            # Testes unitários e de integração
├── scripts/          # Scripts de treinamento
├── data/             # Datasets (raw e processed)
├── models/           # Modelos treinados
├── docs/             # Documentação
└── mlruns/           # MLflow tracking
```

## 🚀 Quick Start

### Instalação

```bash
make install
```

### Treinamento

```bash
make train
```

### Rodar API

```bash
make run-api
```

### Testes

```bash
make test
```

### Linting

```bash
make lint
```

## 📊 Dataset

O projeto usa o dataset **Telco Customer Churn** da IBM, disponível em:
- [Kaggle](https://www.kaggle.com/blastchar/telco-customer-churn)

Coloque o arquivo `WA_Fn-UseC_-Telco-Customer-Churn.csv` em `data/raw/`

## 🔧 Configuração

Todas as configurações estão em `src/config.py`:
- Paths dos dados e modelos
- Seeds para reprodutibilidade
- Hiperparâmetros da MLP
- Configurações da API

## 📈 MLflow

Acompanhe os experimentos:

```bash
mlflow ui
```

Acesse http://localhost:5000

## 🧪 Testes

```bash
make test          # Rodar testes com cobertura
make test-smoke    # Testes smoke apenas
```

## 📚 Documentação

- `docs/ml_canvas.md` - Canvas do problema de ML
- `docs/model_card.md` - Card do modelo
- `docs/monitoring_plan.md` - Plano de monitoramento

## 📝 Notebooks

- `notebooks/01_eda.ipynb` - Análise Exploratória de Dados
- `notebooks/02_modeling.ipynb` - Modelagem e Experimentos

## 🔗 API Endpoints

- `GET /health` - Health check
- `POST /predict` - Fazer predição

### Exemplo de requisição

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 35,
    "tenure": 12,
    "monthly_charges": 65.5,
    "total_charges": 786.0,
    ...
  }'
```

## ⚙️ Comandos do Makefile

| Comando | Descrição |
|---------|-----------|
| `make install` | Instala dependências |
| `make lint` | Roda ruff |
| `make test` | Roda testes com cobertura |
| `make run-api` | Inicia API FastAPI |
| `make train` | Treina modelo |
| `make clean` | Limpa arquivos temporários |

## 📦 Dependências Principais

- **PyTorch**: Framework de deep learning
- **Scikit-Learn**: ML clássico e pré-processamento
- **MLflow**: Tracking de experimentos
- **FastAPI**: Web framework para API
- **Pandas**: Manipulação de dados
- **Pytest**: Framework de testes

## 👥 Autor

Tech Challenge Fase 01

## 📄 Licença

MIT

## 🔒 Quality & Security

Este repositório inclui um pipeline CI/CD focado em qualidade de código e segurança usando ferramentas gratuitas para repositórios públicos.

Badges (substitua os valores `YOUR_PROJECT`/`YOUR_ORG` pelos seus identificadores do SonarCloud):

- Quality Gate: [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=YOUR_ORG_YOUR_PROJECT&metric=alert_status)](https://sonarcloud.io)
- Coverage: [![Coverage](https://sonarcloud.io/api/project_badges/measure?project=YOUR_ORG_YOUR_PROJECT&metric=coverage)](https://sonarcloud.io)
- Security Rating: [![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=YOUR_ORG_YOUR_PROJECT&metric=security_rating)](https://sonarcloud.io)

Como funciona localmente:

1. Rodar todos os testes com cobertura:

```bash
make test
```

2. Rodar Semgrep localmente (via Docker):

```bash
make semgrep-local
```

3. Rodar Sonar Scanner local (requer instalação do sonar-scanner):

```bash
make sonar-local
```

## 🖼️ Diagrama da Arquitetura (draw.io)

O diagrama do repositório foi criado em `docs/repo_architecture.drawio`.

Para incluir uma imagem PNG no README siga estes passos:

1. Abra `docs/repo_architecture.drawio` no editor web diagrams.net (https://app.diagrams.net/) ou na app desktop.
2. Arquivo → Export as → PNG → exporte para `docs/repo_architecture.png`.
3. Commit e push do arquivo PNG:

```powershell
git add docs/repo_architecture.png
git commit -m "docs: add repository architecture diagram PNG"
git push origin YOUR_BRANCH
```

Após commitar, a imagem ficará disponível no README:

![Repository Architecture](docs/repo_architecture.png)

Se preferir, gere o PNG manualmente na interface e commit imediatamente.


