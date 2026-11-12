# Etapa 1 — separação revisada

Arte original preservada: 1672 × 941. Composição GiottoBlackFriday: 1920 × 1080, 30 FPS, estática.

34 camadas registradas: fundo; logo; quatro títulos; três componentes para cada uma das cinco ofertas; três textos de condições; cinco componentes da promoção; dois brilhos; três componentes de rodapé. PNGs com alfa contínuo, coordenadas e centros de transformação em src/data/layers.json. A camada auxiliar extraction-context foi removida.

## Validação

Frame renderizado pelo Remotion/Chromium em previews/frame.png. Reconstrução nativa por alfa: MAE 0, máximo 0. Comparação Full HD com redimensionamento Lanczos: MAE 2,344/255, influenciado pela interpolação do navegador. Comparação em previews/comparison.png; diferenças ampliadas 5× em previews/difference-x5.png; todos os recortes sobre quadriculado em previews/layers-contact-sheet.jpg.

Os cinco preços foram preservados por extração de pixels, sem reescrever caracteres. Não foi criada animação.

## Limitações visuais verificadas

O arquivo de origem é achatado. A transparência foi estimada contra preenchimentos harmônicos. Há contaminação de cor e pequenas margens do cenário em títulos, logotipo e textos. Etiquetas e caixas podem conter vestígios das áreas originalmente sobrepostas. O recorte do ar-condicionado inclui halo verde; brilhos foram separados, mas a decomposição de luz sobre a cena é estimada. As áreas do fundo atrás das ofertas e banner apresentam manchas e suavização; não representam recuperação exata da cena oculta.

A igualdade da composição montada não valida o isolamento para movimento: esses defeitos podem aparecer com deslocamento de camadas. Esta entrega documenta a separação executada, mas ainda NÃO atende integralmente ao padrão de isolamento profissional solicitado. Não declarar aprovação visual ou prontidão para animação.

## Reproduzir

npm ci; npm run typecheck; npm run still. Chromium: /usr/bin/chromium. Script único de extração: scripts/extract_layers.py, com Pillow, NumPy e OpenCV. O caminho do projeto é resolvido a partir do script.

## Inventário

- background — `assets/background/background.png`
- decoracao-inferior — `assets/footer/decoracao-inferior.png`
- brilho-titulo — `assets/effects/brilho-titulo.png`
- brilho-produto — `assets/effects/brilho-produto.png`
- confira-ofertas — `assets/titles/confira-ofertas.png`
- 90-dias — `assets/titles/90-dias.png`
- primeira-parcela — `assets/titles/primeira-parcela.png`
- black-friday — `assets/titles/black-friday.png`
- logo — `assets/logo/logo.png`
- box-942 — `assets/offers/offer-942/box-942.png`
- label-942 — `assets/offers/offer-942/label-942.png`
- text-942 — `assets/offers/offer-942/text-942.png`
- box-785 — `assets/offers/offer-785/box-785.png`
- label-785 — `assets/offers/offer-785/label-785.png`
- text-785 — `assets/offers/offer-785/text-785.png`
- box-628 — `assets/offers/offer-628/box-628.png`
- label-628 — `assets/offers/offer-628/label-628.png`
- text-628 — `assets/offers/offer-628/text-628.png`
- box-471 — `assets/offers/offer-471/box-471.png`
- label-471 — `assets/offers/offer-471/label-471.png`
- text-471 — `assets/offers/offer-471/text-471.png`
- box-315 — `assets/offers/offer-315/box-315.png`
- label-315 — `assets/offers/offer-315/label-315.png`
- text-315 — `assets/offers/offer-315/text-315.png`
- conditions-cartao — `assets/conditions/conditions-cartao.png`
- conditions-boleto — `assets/conditions/conditions-boleto.png`
- conditions-title — `assets/conditions/conditions-title.png`
- footer-copy — `assets/footer/footer-copy.png`
- footer-title — `assets/footer/footer-title.png`
- banner — `assets/promotion/banner.png`
- texto-sorteio — `assets/promotion/texto-sorteio.png`
- texto-banner — `assets/promotion/texto-banner.png`
- 9000-btus — `assets/promotion/9000-btus.png`
- ar-condicionado — `assets/promotion/ar-condicionado.png`
