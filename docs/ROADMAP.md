## ROADMAP — MoveSystem RH (Kanban-friendly, sem tempo)
Pacote: movesystem

Stack: Python + PySide6 (Qt) + SQLite
ORM/Migrations: SQLAlchemy 2.x + Alembic
Plataforma: Windows-only (inicial)
UI: MainWindow com MenuBar + abertura de telas na área central (abas)
Auth: login sem “lembrar usuário”; reset/alteração de senha por e-mail (etapa dedicada)
Permissões: por grupo, com 4 flags (view/create/update/delete) aplicadas em menu e CRUD
Legenda (Kanban): ✅ concluído | 🟡 em andamento | ⚪ não iniciado | R refactor | F feature

## ETAPA 0 — Acordo de trabalho + padrões
E0.1 — Criar PADROES.md (fluxo de trabalho + comunicação) (F)

Aceite: arquivo criado; define como abrir dúvidas/sugestões; define padrão de nomes; define política de branch/commit.

E0.2 — Definir Definition of Done (DoD) do projeto (F)

Aceite: checklist DoD documentado (rodar no Windows, logs, migrations quando necessário, lint/format ok, etc.).

E0.3 — Definir convenção de commits (Conventional Commits) (F)

Aceite: seção no PADROES.md com exemplos (feat:, fix:, refactor:, docs:, chore:).

## ETAPA 1 — Fundação do projeto (movesystem)
E1.1 — Criar estrutura base src/movesystem + tests/ (F)

Aceite: projeto importa movesystem sem erro; estrutura por camadas criada.

E1.2 — Criar pyproject.toml com dependências e scripts (F)

Aceite: comandos definidos (run/test/lint/format); ambiente instala sem conflitos.

E1.3 — Configurar ruff/format + .gitignore (F)

Aceite: ruff check e ruff format (ou equivalente) executam sem falhas no projeto vazio.

E1.4 — Implementar logging padrão (console + arquivo) (F)

Aceite: ao iniciar app, gera log no local definido e imprime no console em dev.

E1.5 — Implementar settings/config (dev) + paths (db/log) (F)

Aceite: settings carregam por ambiente; caminho do DB e do log configuráveis.

E1.6 — Smoke test inicial (pytest) (F)

Aceite: pytest roda; testa import e bootstrap mínimo (sem abrir UI).

## ETAPA 2 — Persistência profissional (SQLAlchemy + Alembic)
E2.1 — Criar DB layer (engine + session factory) abstraído (F)

Aceite: consegue abrir sessão e executar comando simples; DB URL vem do settings.

E2.2 — Inicializar Alembic e configurar env (F)

Aceite: alembic revision e alembic upgrade head funcionam.

E2.3 — Criar migration baseline (F)

Aceite: migration versionada; upgrade cria estrutura inicial.

E2.4 — Criar padrão de transação (commit/rollback) e base repository (F)

Aceite: repositório base existe; rollback em erro é garantido.

E2.5 — Teste de integração: DB limpo + migrations + insert simples (F)

Aceite: teste cria DB do zero, aplica migrations e valida persistência.

## ETAPA 3 — Segurança (usuários/grupos/permissões)
E3.1 — Model ORM: user/group/permission + associações (F)

Aceite: models criados com relacionamento; sem dependência da UI.

E3.2 — Migration: criar tabelas de segurança (F)

Aceite: upgrade cria tabelas; downgrade reverte.

E3.3 — Serviço de senha (hash + verify) (F)

Aceite: senhas nunca são armazenadas em texto; testes básicos de verify.

E3.4 — Repositórios de auth (User/Group/Permission) (F)

Aceite: CRUD mínimo e queries essenciais (buscar por username; permissões por grupo).

E3.5 — Use case de login (validação de credenciais) (F)

Aceite: retorna usuário + grupos/permissões; falha controlada.

E3.6 — Seed dev: ADMIN + permissões completas (F)

Aceite: script cria admin se não existir; idempotente em dev.

E3.7 — Serviço “tem_permissao(recurso, flag)” (F)

Aceite: recebe view/create/update/delete; retorna boolean confiável.

E3.8 — Testes: login e permissões (F)

Aceite: testes automatizados cobrindo cenários positivos/negativos.

## ETAPA 4 — UI Shell (MainWindow + Menu + Abas)
E4.1 — Criar MainWindow com MenuBar conforme layout (F)

Aceite: menus “Sistema/Cadastros/Documentos/Ajuda” exibidos.

E4.2 — Implementar QTabWidget central (abrir/focar/fechar abas) (F)

Aceite: abrir aba por ação; se já existir foca; fechar não quebra.

E4.3 — Implementar StatusBar (“Pronto”) (F)

Aceite: status aparece e pode ser atualizado.

E4.4 — Criar placeholders das telas (widgets vazios) (F)

Aceite: menu abre abas “Colaborador/Afastamento/Jurídico/Restaurante” (placeholder).

E4.5 — Aplicar permissão view no menu (F)

Aceite: itens sem view ficam desabilitados/ocultos (definimos uma estratégia e padronizamos).

E4.6 — Tratamento padrão de erro na UI (log + dialog) (R/F)

Aceite: exceção em action não derruba o app; log registrado; mensagem exibida.

## ETAPA 5 — Login dentro da principal + sessão
E5.1 — Implementar LoginDialog modal no startup (F)

Aceite: MainWindow inicia e exige login; sem login não acessa menus.

E5.2 — Criar contexto de usuário logado (CurrentUser) (F)

Aceite: usuário logado disponível para permissões e auditoria.

E5.3 — Atualizar menus após login (com permissões) (F)

Aceite: ao logar, menus refletem permissões do grupo.

E5.4 — Implementar Logout (F)

Aceite: limpa sessão e volta para login, sem reiniciar processo (se possível).

E5.5 — Política: cancelar login encerra app (F)

Aceite: comportamento implementado exatamente como definido.

E5.6 — Checklist de teste manual do fluxo (F)

Aceite: documento simples com passos e resultados esperados.

## ETAPA 6 — BaseForm (CRUD + estados + permissões por ação)
E6.1 — Definir contrato/hook methods do BaseForm (F)

Aceite: interface clara; documentada; subclasses sabem o que implementar.

E6.2 — Implementar estados VIEW/NEW/EDIT (F)

Aceite: transições corretas; campos habilitam/desabilitam.

E6.3 — Implementar barra CRUD padrão (Novo/Salvar/Editar/Excluir/Cancelar) (F)

Aceite: botões funcionais e conectados aos hooks.

E6.4 — Implementar validação e mensagens padrão (F)

Aceite: erros exibidos de forma consistente; confirma exclusão.

E6.5 — Integrar permissões (create/update/delete/view) (F)

Aceite: botões/ações bloqueiam corretamente por permissão.

E6.6 — Padronizar layout (título + corpo grid/abas + rodapé) (F)

Aceite: form herdeiro segue padrão sem repetir boilerplate.

E6.7 — Definir padrão de listagem/pesquisa (componente Qt) (F)

Aceite: escolhido e documentado; BaseForm oferece suporte.

## ETAPA 7 — Cadastro de Colaborador (primeiro módulo real)
E7.1 — Fechar escopo do Colaborador (campos + regras) (F)

Aceite: lista de campos obrigatórios e validações definida (documentada).

E7.2 — Model ORM Colaborador (F)

Aceite: model criado + relacionamentos mínimos (se houver).

E7.3 — Migration Colaborador (F)

Aceite: migration aplica e reverte.

E7.4 — Repositório Colaborador (CRUD) (F)

Aceite: operações CRUD com transação e tratamento de erro.

E7.5 — Use cases (create/update/delete/get/list) (F)

Aceite: regras de negócio fora da UI; testável.

E7.6 — ColaboradorForm herdando BaseForm (F)

Aceite: UI completa do MVP; CRUD funcionando via use cases.

E7.7 — Listagem + busca/filtro (mínimo) (F)

Aceite: consegue localizar colaborador por pelo menos 1 critério (ex.: nome/CPF/matrícula).

E7.8 — Permissões CRUD aplicadas no form (F)

Aceite: ações bloqueadas corretamente por grupo.

E7.9 — Testes (repo/use cases) (F)

Aceite: testes cobrindo cenários principais.

## ETAPA 8 — Alteração de senha por e-mail
E8.1 — Definir estratégia SMTP + token + expiração (F)

Aceite: comportamento documentado (tempo de expiração, reuso, rate-limit básico).

E8.2 — Model/Migration password_reset_token (F)

Aceite: token armazenado com expiração e flag de uso.

E8.3 — Use case solicitar reset (F)

Aceite: gera token; dispara e-mail (ou mock em dev).

E8.4 — Use case redefinir senha (F)

Aceite: valida token/expiração; atualiza senha; invalida token.

E8.5 — UI: solicitar e redefinir senha (modais) (F)

Aceite: fluxo utilizável; mensagens claras; sem expor token.

E8.6 — Testes tokens/expiração (F)

Aceite: testes unit cobrindo expiração e invalidação.

## ETAPA 9 — Próximos módulos (a definir depois)
(Afastamento/Jurídico/Restaurante entram quando você definir o que cada um fará.)