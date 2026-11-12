# Etapa 1 — extração inicial e validação estática

Arte original recebida no RAR e preservada em arquivos/01_arte_original. Dimensões nativas: 1672 × 941. Composição Remotion: 1920 × 1080.

Foram exportadas 31 camadas de conteúdo, fundo reconstruído e uma camada auxiliar de contexto residual (33 entradas em layers.json). As cinco ofertas têm caixa, etiqueta e texto separados. Textos, preços e logotipo foram extraídos dos pixels originais, sem geração ou substituição tipográfica.

## Verificações executadas

- TypeScript passou.
- Frame estático renderizado pelo Remotion com Chromium local.
- Reconstrução Python na resolução nativa: diferença zero antes da reamostragem.
- Frame Remotion Full HD comparado com a referência redimensionada: erro médio absoluto 2,268/255 por canal. Reamostragem independente e coordenadas fracionárias afetam bordas.
- Comparação lado a lado e mapa de diferenças amplificado em 5× disponíveis em previews.
- Inspeção visual do frame: cinco preços e textos preservados, composição completa.

## Limitações: ainda não aprovar para animação

A recomposição estática fiel não equivale a isolamento perfeito. Máscaras de textos incluem margem de contexto de 2 pixels; caixas e etiquetas incluem regiões retangulares do fundo. O produto tem máscara poligonal inicial. O inpainting determinístico não recupera a casa e a vegetação ocultas e produz suavização nas áreas grandes.

A camada extraction-context mantém resíduos do fundo intermediário para permitir recomposição fiel. Ela deve ser refinada e redistribuída antes de mover elementos; ocultar camadas agora pode revelar marcas e halos. Os brilhos do produto e do título ainda não estão isolados como efeitos independentes. A etapa 1 é uma versão de trabalho, não a separação profissional concluída.

## Reproduzir

Instalar Pillow, numpy e opencv-python-headless para os scripts. Executar scripts/extract_layers.py e depois scripts/refine_background.py. No projeto: npm ci, npm run typecheck e npm run still. Scripts de extração usam o caminho deste checkout em /workspace/motiongraphcs.

Não foi criada animação nesta etapa.
