# Estado do projeto Giotto Energia

## Material disponível

- Prompts completos das etapas 1 e 2 em `arte_tv_giotto_energia/arquivos/04_prompts/`.
- Vídeo fornecido pelo usuário e imagens de inspeção em `arte_tv_giotto_energia/arquivos/05_referencias/`.
- Base React, TypeScript e Remotion, dependências fixadas em package-lock.json, componentes de camadas/ofertas, dados comerciais e timeline em `arte_tv_giotto_energia/arquivos/03_projeto_animacao/giotto-motion/`.
- Pasta `arte_tv_giotto_energia/videos_finais/` reservada às exportações concluídas.

## Trabalho pendente

A imagem estática apareceu na conversa, mas seu arquivo não foi disponibilizado no sistema de arquivos. O vídeo de referência está preservado. Ainda não existem camadas extraídas, fundo limpo, comparação estática validada ou novos vídeos finais. `layers.json` está vazio e a composição estática recusa renderização sem os elementos.

Próximo passo: obter a arte original em arquivo ou preparar uma extração documentada da referência disponível, identificando as limitações da compressão e das áreas ocultas; depois concluir a validação das camadas e implementar/renderizar a animação solicitada. Não considerar o vídeo de referência uma entrega gerada.

## Retomar o desenvolvimento

Usar o checkout existente deste repositório, sem criar worktree salvo solicitação. Entrar em `arte_tv_giotto_energia/arquivos/03_projeto_animacao/giotto-motion`, executar `npm ci` e `npm run typecheck`. Os comandos `npm run studio` e `npm run still` destinam-se à composição após o preenchimento das camadas.

Os arquivos devem permanecer organizados neste repositório. Publicar atualizações solicitadas no GitHub e entregar as exportações finais na pasta dedicada.
