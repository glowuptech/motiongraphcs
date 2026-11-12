# Entrega Motion Giotto Black Friday

Vídeos renderizados em Remotion e finalizados em FFmpeg. Arquivos na pasta videos_finais: giotto-black-friday-motion-10s.mp4 (AAC), giotto-black-friday-motion-muted.mp4 (sem faixa de áudio) e giotto-black-friday-final-frame.png.

Validação ffprobe: 1920 × 1080, 30 FPS, 300 frames, duração do contêiner 10,000 segundos, H.264 e yuv420p. TypeScript passou. Inspeção visual dos frames 0,30,60,90,150,190,230,270,299 em inspecao-motion.jpg. Comparação PNG entre frames 264 e 299: diferença máxima zero. Cinco ofertas mantidas. Entradas determinísticas com spring/easing, posição, escala e desfoque; faixa luminosa na abertura. Sem fade-out.

Trilha eletrônica e efeitos sintetizados originalmente, sem samples de terceiros. Gerador e eventos sincronizados em scripts/generate_audio.py. Não foi realizada avaliação auditiva; áudio foi sintetizado com amplitude limitada e eventos posicionados por frame.

Limitações visuais: camadas herdadas da etapa 1 têm halos e contaminação do fundo; entrada do produto e bordas das caixas podem mostrar essas limitações. O cenário da abertura usa preenchimento harmônico que suaviza regiões ocultas, sem recuperar detalhes inexistentes no PNG. O fundo original da recomposição retorna entre frames 240–264, sob a arte montada. Não é uma reprodução perfeita do cenário oculto nem garantia de acabamento premium. As áreas visíveis da casa e dos painéis foram mantidas. Inspecionar o vídeo antes de veicular.

Projeto editável: arquivos/03_projeto_animacao/giotto-motion. npm ci, npm run studio e npm run render:motion. Requer Chromium em /usr/bin/chromium e FFmpeg. Timeline em src/config/animation-timeline.ts. A composição principal é GiottoBlackFridayMotion; a composição estática GiottoBlackFriday foi mantida. O ZIP etapa-01-camadas.zip representa apenas a etapa 1; o projeto atualizado está no repositório.
