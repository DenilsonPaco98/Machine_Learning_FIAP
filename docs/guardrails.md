# Guardrails: Qualidade e Segurança

Este documento descreve as ferramentas, como interpretar resultados e como agir em caso de problemas.

1) Overview das ferramentas

- SonarCloud: análise estática para bugs, vulnerabilidades, code smells e cobertura. (Grátis para repositórios públicos)
- Semgrep: SAST moderno com regras específicas para Python e segurança.
- Trivy: scanner de vulnerabilidades para imagens e sistema de arquivos.
- OSV Scanner: checa vulnerabilidades conhecidas nas dependências.
- Gitleaks: detecta credenciais e secrets comprometidos em commits.
- Actionlint: valida sintaxe e boas práticas nos arquivos de workflow do GitHub Actions.

2) Como interpretar resultados

- SonarCloud:
  - Quality Gate: PASS/FAIL. Se FAIL, o PR deve ser bloqueado.
  - Priorize Bugs e Vulnerabilities (nível Critical/Blocker).
  - Cobertura: compare com o mínimo configurado (>70%).

- Semgrep:
  - As regras são categorizadas (ERROR/WARNING/INFO). Priorize CORRECT/ERROR.
  - Regras de segurança (p/security-audit) demandam atenção imediata.

- Trivy / OSV:
  - Vulnerabilidades com CVSS alto (>=7) devem ser tratadas imediatamente.

- Gitleaks:
  - Se encontrar secrets, rotacione a credencial imediatamente e aplique um secret scan remoto.

3) Playbook de resposta rápida (incidente de segurança)

- Passo 1: Isolar o commit
  - Reverter o commit que expôs o segredo e bloquear o branch temporariamente.

- Passo 2: Rotacionar credenciais
  - Identifique as credenciais e rotacione-as (p.ex. tokens, chaves AWS, DB).

- Passo 3: Avaliar o impacto
  - Determine se houve uso indevido das credenciais (logs, auditoria).

- Passo 4: Notificar time e atualizar issue
  - Abra um incidente no tracker (Jira/GitHub Issues) com steps e mitigação.

4) Como rodar localmente

```bash
make semgrep-local
make trivy-local
make gitleaks-local
make actionlint-local
```

5) Como melhorar continuamente

- Ajuste regras do Semgrep para reduzir falsos positivos
- Automatize rotinas de atualização de dependências
- Adote políticas de revisão para alterações em arquivos sensíveis (.github, infra)
