# Evidências — Ficha Prática 05 (DevOps)

Repositório: <https://github.com/PedroRaposo02/app-suporte-lab>
Pull Request: <https://github.com/PedroRaposo02/app-suporte-lab/pull/1>

Ambiente: Git 2.45.2, Python 3.12.0 (local) / 3.13 (container e CI), Docker 28.1.1, Git Bash em Windows 11.

---

## 1. Histórico

`git log --oneline --graph --decorate --all` (repositório `app-suporte`, após o Exercício 7.4):

```
*   bac5517 (HEAD -> main, origin/main, github/main) merge: integrar feature/api-docker (PR #1)
|\
| * 6260112 (github/feature/api-docker, feature/api-docker) ci: identificar commit do build e etiquetar imagem com a revisao (desafio C)
| * 7dabff2 feat: registar resultado de cada pedido /health nos logs (desafio B)
| * d0e27b3 test: validar rota GET /health com servidor HTTP real (desafio A)
| * cabd0f7 fix: repor rota GET /health (corrige regressao de 9bfb9e9)
| * 9bfb9e9 test(simulacao): alterar rota /health para /status para simular regressao
| * 2355af0 ci: adicionar workflow com jobs validar e construir (smoke test)
| * d39adad build: adicionar Dockerfile com healthcheck e .dockerignore
| * 53f8858 feat: adicionar API HTTP /health e testes unitarios
|/
*   90676cb (tag: v1.0.0) merge: integrar docs/operacoes apos revisao
|\
| * ddcd757 (origin/docs/operacoes) docs: acrescentar verificacao de logs e estado do container
|/
*   7107996 merge: integrar fix/estado-servico resolvendo conflito em status.txt (status=HEALTHY)
|\
| * b0082fd (fix/estado-servico) fix: definir estado saudavel
* | a67b3fd chore: sinalizar estado de aviso
|/
* 96c9e0c (feature/healthcheck) feat: adicionar definicao do healthcheck
* f0b7dab feat: adicionar ficheiros iniciais da App de Suporte
```

### Exercício 1

- Ficheiros *untracked* após a criação: `OPERACOES.md`, `README.md`, `status.txt`.
- Após `git add README.md`: `README.md` em *Changes to be committed*; os outros dois continuam *untracked*.
- `git log -1 --oneline` → `f0b7dab feat: adicionar ficheiros iniciais da App de Suporte`
- `git status` → `nothing to commit, working tree clean`

### Exercício 2

- 2.1: `healthcheck.txt` não existia na `main` antes do merge. O merge foi **fast-forward** (`Updating f0b7dab..96c9e0c / Fast-forward`), porque a `main` não tinha commits novos desde a criação da branch.
- 2.2: mensagem do Git:
  ```
  Auto-merging status.txt
  CONFLICT (content): Merge conflict in status.txt
  Automatic merge failed; fix conflicts and then commit the result.
  ```
  Conteúdo de `status.txt` durante o conflito:
  ```
  <<<<<<< HEAD
  status=WARNING
  =======
  status=HEALTHY
  >>>>>>> fix/estado-servico
  ```
  Entre `<<<<<<< HEAD` e `=======` está a versão da branch atual (`main`); entre `=======` e `>>>>>>>` está a versão da branch que se está a integrar.
- Resolução: ficheiro reescrito com `status=HEALTHY\n`, `git add status.txt`, `git commit`.
- Commits anteriores ao merge: `a67b3fd` (main, WARNING) e `b0082fd` (fix, HEALTHY). Commit de integração: `7107996`.
- `grep -qx 'status=HEALTHY' status.txt` → código de saída 0; `git status` → *working tree clean*, sem merge pendente.

### Exercício 3

- Remoto local criado com `git init --bare -b main app-suporte-remoto.git`.
- Commit publicado pelo colega: `ddcd757 docs: acrescentar verificacao de logs e estado do container`.
- `git diff main...origin/docs/operacoes`:
  ```diff
  @@ -1 +1,2 @@
   # Procedimentos operacionais
  +Verificar logs e estado do container
  ```
- Integrado com `git merge --no-ff` → merge commit `90676cb`; publicado com `git push origin main`.
- No colega: `git pull --ff-only origin main` → `Fast-forward 7107996..90676cb`.
- `diff app-suporte/OPERACOES.md app-suporte-colega/OPERACOES.md` → sem diferenças.

> Nota: o Git for Windows tem `core.autocrlf=true` ao nível do sistema, o que converteu os ficheiros do clone para CRLF e fez com que o primeiro commit do colega alterasse também a primeira linha. Foi configurado `core.autocrlf=false` nos repositórios do laboratório e o commit do colega foi corrigido (`--amend`) antes de ser revisto.

## 2. Branches e remotos

`git branch -a`:

```
  feature/api-docker
  feature/healthcheck
  fix/estado-servico
* main
  remotes/github/feature/api-docker
  remotes/github/main
  remotes/origin/docs/operacoes
  remotes/origin/main
```

`git remote -v`:

```
github	https://github.com/PedroRaposo02/app-suporte-lab.git (fetch)
github	https://github.com/PedroRaposo02/app-suporte-lab.git (push)
origin	../app-suporte-remoto.git (fetch)
origin	../app-suporte-remoto.git (push)
```

## 3. Tag

- `git rev-parse --short HEAD` (na `main`, antes da tag) → `90676cb`
- `git tag -a v1.0.0 -m "Versao inicial da App de Suporte"` e `git push origin v1.0.0`
- `git ls-remote --tags origin`:
  ```
  b4149e7c3ca04dd590f9b199108d290a92e47433	refs/tags/v1.0.0
  90676cb8738eed64871dfe086d50d1f9eff26a9d	refs/tags/v1.0.0^{}
  ```
- Relação tag ↔ commit: a tag anotada é um objeto próprio (`b4149e7`, com autor, data e mensagem) que aponta para o commit `90676cb` (merge de `docs/operacoes`). A linha `^{}` mostra o commit para onde a tag aponta após *dereference*.

## 4. Docker

Comandos:

```
docker build -t app-suporte:1.1.0 .
docker run -d --name app-suporte -p 127.0.0.1:8000:8000 app-suporte:1.1.0
```

`curl -i http://127.0.0.1:8000/health`:

```
HTTP/1.0 200 OK
Server: BaseHTTP/0.6 Python/3.13.18
Content-Type: text/plain; charset=utf-8
Content-Length: 15

status=HEALTHY
```

Healthcheck (`docker inspect --format '{{.State.Health.Status}}' app-suporte`): `starting` nos primeiros segundos e depois `healthy`.

```
NAMES         IMAGE               STATUS                    PORTS
app-suporte   app-suporte:1.1.0   Up 19 seconds (healthy)   127.0.0.1:8000->8000/tcp
```

`docker logs app-suporte`:

```
172.17.0.1 - - [13/Nov/2026 16:00:30] "GET /health HTTP/1.1" 200 -
127.0.0.1 - - [13/Nov/2026 16:00:32] "GET /health HTTP/1.1" 200 -
```

(pedidos de `172.17.0.1` vêm do host através do port mapping; os de `127.0.0.1` são do HEALTHCHECK dentro do container.)

Execução local da API (antes do Docker): `/health` → `200 OK`, `/outro` → `404 Not Found`.

### Papel de cada instrução do Dockerfile

| Instrução | Papel |
|---|---|
| `FROM python:3.13-slim` | Imagem base com Python 3.13 numa distribuição mínima |
| `WORKDIR /app` | Diretório de trabalho para as instruções seguintes e para o processo |
| `COPY app.py status.txt ./` | Copia apenas os ficheiros necessários à execução |
| `USER 10001:10001` | Executa o processo com um utilizador sem privilégios (não root) |
| `EXPOSE 8000` | Documenta a porta onde o serviço escuta (não publica a porta por si só) |
| `HEALTHCHECK` | Comando periódico que o Docker executa para marcar o container como `healthy`/`unhealthy` |
| `CMD ["python", "app.py"]` | Comando por omissão ao iniciar o container |

Códigos HTTP da API: estado saudável → **200**; estado inválido (ex.: `status=WARNING`) → **503**; endpoint inexistente → **404**.
`read_status()` lê `status.txt` (junto a `app.py`) e remove espaços/quebras de linha; `is_healthy()` devolve `True` apenas se o conteúdo for exatamente `status=HEALTHY`.

## 5. CI

### Análise do workflow (`.github/workflows/ci.yml`)

- **Trigger:** `push` para `main` e `pull_request` com destino `main`.
- **Jobs:** `validar` (checkout, Python 3.13, verificar ficheiros, testes unitários) e `construir` (checkout, build da imagem, smoke test).
- **Dependência:** `needs: validar` — `construir` só arranca depois de `validar` terminar com sucesso; se `validar` falhar, `construir` é ignorado.
- **Condição de falha:** qualquer comando com código de saída ≠ 0 (ex.: `test -f`, `grep -qx`, testes) falha o step; no smoke test, se `curl` não obtiver resposta 2xx em 20 tentativas, mostra os logs e faz `exit 1`.
- **`curl -fsS`:** `-f` faz o curl terminar com erro (código 22) perante respostas HTTP ≥ 400, para que um 404/503 falhe o step; `-s` silencia a barra de progresso; `-S` mantém as mensagens de erro visíveis apesar do `-s`.

### Execuções no GitHub Actions

| Run | Commit | Evento | validar | construir | Resultado |
|---|---|---|---|---|---|
| [43458563781](https://github.com/PedroRaposo02/app-suporte-lab/actions/runs/43458563781) | `2355af0` | pull_request | ✓ 7s | ✓ 11s | success |
| [43458703493](https://github.com/PedroRaposo02/app-suporte-lab/actions/runs/43458703493) | `9bfb9e9` | pull_request | ✓ | ✗ Executar smoke test | **failure** |
| [43458947032](https://github.com/PedroRaposo02/app-suporte-lab/actions/runs/43458947032) | `cabd0f7` | pull_request | ✓ | ✓ | success |
| [43459080033](https://github.com/PedroRaposo02/app-suporte-lab/actions/runs/43459080033) | `6260112` | pull_request | ✓ | ✓ | success |
| [43459232988](https://github.com/PedroRaposo02/app-suporte-lab/actions/runs/43459232988) | `bac5517` | push (main, após merge do PR) | ✓ | ✓ | success |

### Alternativa local (6.4)

```
Ran 2 tests in 0.000s
OK
ficheiros OK
status=HEALTHY
Smoke test OK
```

## 6. Incidente (Exercício 7)

| Evidência | Resultado observado |
|---|---|
| Commit que introduziu a regressão | `9bfb9e9 test(simulacao): alterar rota /health para /status para simular regressao` |
| Testes unitários | **Passam** (2/2 OK) — só testam `is_healthy()`, que não foi alterada |
| Construção da imagem Docker | **Sucesso** (step `Construir imagem` ✓) |
| Resposta HTTP do endpoint `/health` | `HTTP/1.0 404 Not Found` |
| Job ou etapa com falha | Job `construir` → step `Executar smoke test` (run 43458703493) |
| Mensagem principal dos logs | `curl: (22) The requested URL returned error: 404`; `"GET /health HTTP/1.1" 404 -`; `Process completed with exit code 1.` |
| Causa identificada | Em `app.py` a condição de encaminhamento passou de `self.path != "/health"` para `self.path != "/status"`, pelo que `/health` devolve 404 |

`git diff HEAD~1..HEAD` (no commit da regressão):

```diff
-        if self.path != "/health":
+        if self.path != "/status":
```

**Correção:** commit `cabd0f7 fix: repor rota GET /health (corrige regressao de 9bfb9e9)`.
**Evidência da recuperação:** testes unitários OK; smoke test local `HTTP/1.0 200 OK` + `status=HEALTHY`; pipeline [43458947032](https://github.com/PedroRaposo02/app-suporte-lab/actions/runs/43458947032) com `validar` e `construir` em *success*.

### 7.4 Consolidação

PR #1 integrado na `main` (merge commit `bac5517`) e `main` local atualizada com `git pull --ff-only github main`.

**Proposta de versão: `v1.1.0`** (SemVer `MAJOR.MINOR.PATCH`). Desde `v1.0.0` foram acrescentadas funcionalidades novas e compatíveis (API `/health`, imagem Docker, pipeline de CI, logs) e uma correção. Não há alterações incompatíveis → incrementa-se o **MINOR**. É também coerente com a tag da imagem `app-suporte:1.1.0`. A tag não foi criada nem publicada como release, conforme pedido.

## 7. Reflexão — respostas às questões

**Q1.** Guardar no disco altera apenas o Working Directory; o Git vê o ficheiro como modificado/untracked. `git add` copia o estado atual para a Staging Area, escolhendo o que vai entrar no próximo commit. `git commit` grava a Staging Area como um snapshot permanente no histórico, com autor, data e mensagem.

**Q2.** Ambas as branches alteraram a mesma linha a partir do mesmo ancestral, e o Git não sabe qual das alterações é correta, ou se o resultado deve combinar as duas. Escolher automaticamente uma versão poderia perder trabalho ou introduzir um estado errado. Neste caso o requisito do serviço (`status=HEALTHY`) é que define o resultado.

**Q3.** `app-suporte` é um repositório normal, com Working Directory onde se editam ficheiros e uma pasta `.git` com o histórico. `app-suporte-remoto.git` é *bare*: só tem o conteúdo da pasta `.git`, sem Working Directory, e serve apenas como ponto central para `push`/`fetch`.

**Q4.** `git fetch` descarrega commits e referências do remoto (`origin/*`) sem alterar as branches locais nem o Working Directory. `git pull` faz `fetch` e logo a seguir integra (merge ou rebase) na branch atual. `fetch` é preferível quando se quer rever as alterações antes de as integrar (`git log`, `git diff`), como na revisão do trabalho do colega, ou quando a branch local tem trabalho que não se quer misturar ainda.

**Q5.** Não. Uma tag é só um nome que aponta para um commit no histórico. Instalar em produção exige construir um artefacto, publicá-lo e fazer o deployment, normalmente por uma pipeline com aprovações. A tag pode servir de *trigger* para essa pipeline, mas por si só não instala nada.

**Q6.** Não. Os testes só verificam a lógica da função `is_healthy()` de forma isolada. Não arrancam o servidor nem verificam o encaminhamento (`/health`), os códigos HTTP, os headers, a leitura de `status.txt` ou a porta. Testar o serviço em execução exercita tudo isto em conjunto, tal como um cliente real o usaria.

**Q7.** `docker build` só confirma que a imagem foi montada (a base existe e os ficheiros foram copiados). Não executa a aplicação, por isso erros de runtime, rotas erradas, permissões do utilizador não-root, ficheiros em falta em execução ou portas incorretas só aparecem ao correr o container e fazer pedidos.

**Q8.** Problemas de integração e de execução: rota errada (como no Exercício 7), servidor que não arranca ou não escuta na porta certa, `status.txt` não copiado para a imagem, erros de permissões com `USER 10001`, falhas de dependências da imagem base, port mapping incorreto, resposta com código HTTP errado.

**Q9.** Porque medem coisas diferentes. Os testes unitários só cobriam `is_healthy()`, que continuava correta. A regressão estava no encaminhamento HTTP (`self.path`), que nenhum teste unitário exercitava. O smoke test faz um pedido real a `/health` e por isso detetou o 404. (O desafio A acrescenta um teste que cobre esta lacuna.)

**Q10.** O sintoma observado (`GET /health` → 404 em vez de 200), o ambiente (container `app-suporte:ci`, runner do GitHub Actions), o commit/versão afetado (`9bfb9e9`) e o último commit que funcionava (`2355af0`), o job e step que falhou com o link para o run, as linhas relevantes dos logs, os passos para reproduzir, o impacto (healthcheck falha e o container fica `unhealthy`) e a causa provável, se identificada (diff em `app.py`). Sem incluir segredos nem dados sensíveis.

## Desafios opcionais

**A — Melhorar os testes** (`d0e27b3`): classe `HealthEndpointTests` em `tests/test_app.py` arranca o `ThreadingHTTPServer` numa porta efémera e valida `GET /health` → 200 + `status=HEALTHY\n` e uma rota inexistente → 404. Foi confirmado que, ao repor a regressão (`/status`), este teste falha (`FAILED (errors=1)`), ao contrário dos testes originais.

**B — Observabilidade** (`7dabff2`): cada pedido a `/health` regista uma linha como:

```
172.17.0.1 - - [13/Nov/2026 16:05:00] health_check path=/health result=status=HEALTHY http=200
```

Informação mínima para diagnosticar uma falha: timestamp, origem do pedido, caminho pedido, estado lido (`status.txt`) e código HTTP devolvido. Pedidos a rotas erradas continuam a gerar `code 404, message Not Found`.

**C — Evoluir a pipeline** (`6260112`): o job `construir` tem o step `Identificar commit` e o build acrescenta a label OCI `org.opencontainers.image.revision=<sha>` e a tag `app-suporte:sha-<sha curto>`. Em PRs usa-se `github.event.pull_request.head.sha`, porque `github.sha` seria o merge commit temporário. Log do run 43459080033:

```
Commit do build: 6260112bf54621ff24cf8b053173345d3435c649
Imagem sha256:7f2f0766... construida a partir do commit 6260112bf54621ff24cf8b053173345d3435c649
```

Assim, a partir de qualquer imagem (`docker image inspect`) chega-se ao commit exato no Git, e vice-versa através da tag `sha-<sha>`.

**D — Release e rollback:**

- **Tags Git** (`v1.1.0`, anotadas): identificam o código-fonte de uma versão; são criadas na `main` após o CI passar.
- **Tags de imagem Docker** (`app-suporte:1.1.0`, `app-suporte:sha-6260112`): nomes legíveis, mas **mutáveis** (podem ser reatribuídas a outra imagem). Usar a tag SemVer para pessoas e a tag `sha-` para rastreabilidade.
- **Digests** (`app-suporte@sha256:…`): identificam o conteúdo exato e são **imutáveis**. O deployment deve referenciar o digest, para garantir que o que foi testado é exatamente o que corre.
- **Rollback:** registar para cada release o trio *tag Git → sha do commit → digest da imagem*. Para reverter, volta-se a fazer deploy do digest da versão anterior conhecida como boa (sem rebuild), confirma-se com o smoke test/healthcheck e só depois se corrige o código numa nova versão PATCH (ex.: `v1.1.1`).

## Checklist de conclusão

- [x] Criei o repositório com a branch `main` e commits descritivos.
- [x] Utilizei uma branch para implementar uma alteração isolada.
- [x] Integrei uma branch e resolvi um conflito de merge.
- [x] Configurei um remoto Git e simulei a colaboração entre dois profissionais.
- [x] Criei e consultei a tag anotada `v1.0.0`.
- [x] Construí uma imagem Docker e validei o endpoint `/health`.
- [x] Executei testes unitários e um smoke test.
- [x] Criei um workflow CI ou executei a alternativa local.
- [x] Reproduzi uma regressão e identifiquei a respetiva causa.
- [x] Confirmei a correção e registei as evidências.
