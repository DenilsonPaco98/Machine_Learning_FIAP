# Instruções de configuração: SonarCloud, Semgrep e Branch Protection

Siga estes passos para ativar o pipeline de qualidade e segurança para repositórios públicos.

1) SonarCloud
   - Acesse: https://sonarcloud.io e faça login com GitHub (OAuth).
   - Clique em **+** → **Analyze new project** → selecione o repositório.
   - No Painel do projeto, anote **Organization key** e **Project key**.
   - Em **My Account → Security** gere um token (SONAR_TOKEN).
   - No GitHub: Settings → Secrets and variables → Actions → New repository secret
     - Nome: `SONAR_TOKEN` → Valor: token gerado
     - Nome: `SONAR_PROJECT_KEY` → Valor: `YOUR_SONARCLOUD_PROJECT_KEY`
     - Nome: `SONAR_ORGANIZATION` → Valor: `YOUR_SONARCLOUD_ORGANIZATION`
   - Em SonarCloud → Administration → Analysis Method, desabilite "Automatic Analysis" se desejar usar GH Actions.

2) Semgrep (opcional, recomendado)
   - Registre-se em https://semgrep.dev (gratuito).
   - Gere um token de aplicação (SEMGREP_APP_TOKEN) e adicione como secret no GitHub (Settings → Secrets...
   - O token permite enviar resultados para o dashboard do Semgrep; sem token, a ação roda localmente e gera SARIF.

3) Branch Protection
   - GitHub → Settings → Branches → Add rule
   - Branch name pattern: `main`
   - Ativar: Require status checks to pass before merging
   - Selecionar checks obrigatórios (aparecerão após primeiro run do workflow):
     - `CI / test-and-scan` (nome do job)
     - `CI / gate-check` (Quality Gate)
   - Salvar

4) Rodando localmente
   - Semgrep via Docker: `make semgrep-local`
   - Sonar Scanner: instalar o `sonar-scanner` e então `make sonar-local`

5) Observações
   - SonarCloud é gratuito para repositórios públicos, mas há limitações de features para planos gratuitos.
   - Semgrep gratuito é suficiente para repositórios públicos e gera SARIF compatível com GitHub.
