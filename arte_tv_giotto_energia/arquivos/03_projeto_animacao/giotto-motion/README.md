# Giotto Black Friday — preparação estática

Status: estrutura inicial. Extração bloqueada até receber o arquivo original PNG/JPG. Não há elementos extraídos, fundo reconstruído ou frame validado. layers.json permanece vazio para evitar coordenadas fictícias. A composição recusa renderização sem as camadas.

## Desenvolvimento

No diretório deste arquivo, execute `npm ci`, `npm run typecheck` e `npm run studio`. Depois da extração, `npm run still` renderiza o frame estático. Composição GiottoBlackFriday: 1920 × 1080, 30 fps, 300 frames, sem movimentos.

Use o checkout existente: cada tarefa na nuvem já é isolada; não crie worktree sem solicitação.

## Próxima etapa

Preservar a imagem recebida em ../../01_arte_original/. Medir suas dimensões reais e mapear as coordenadas para 1920 × 1080 sem distorção. Extrair elementos com alfa por processamento de imagem conforme o prompt salvo em ../../04_prompts/etapa-01-separacao.md. Não gerar textos, números ou logo por IA. Registrar em src/data/layers.json identificador, nome, arquivo, x, y, width, height, zIndex, transformOrigin em pixels locais e offerId opcional.

Regiões encobertas do cenário não podem ser recuperadas exatamente de uma imagem achatada; documentar toda reconstrução. Validar transparência, bordas, brilhos e preços, renderizar frame, comparação lado a lado e mapa de diferenças. Nunca apresentar a estrutura inicial como separação concluída.

Exportações finais de vídeo pertencem a ../../../videos_finais/, apenas na etapa posterior de animação.
