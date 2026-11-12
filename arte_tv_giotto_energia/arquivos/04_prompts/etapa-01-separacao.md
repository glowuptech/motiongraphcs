# ETAPA 1 — Separação profissional de elementos para Motion Graphics

## OBJETIVO

Preciso transformar a arte publicitária anexada da **Black Friday Giotto Energia** em uma composição organizada em camadas independentes, para posteriormente produzir um motion graphic profissional de aproximadamente 10 segundos utilizando Remotion.

**ATENÇÃO: NESTA ETAPA NÃO CRIE A ANIMAÇÃO.**

Seu trabalho é exclusivamente analisar a arte, separar seus elementos e preparar todos os arquivos para a etapa de animação.

## REGRA PRINCIPAL — FIDELIDADE VISUAL ABSOLUTA

A imagem anexada é a referência visual definitiva.

Não quero um redesign, uma nova interpretação ou uma versão aproximada.

Preserve rigorosamente:

- Identidade visual e logotipo da Giotto Energia.
- Cores, gradientes e iluminação.
- Tipografia, pesos e proporções.
- Textos, números, preços e pontuação.
- Bordas arredondadas e contornos verdes.
- Sombras, brilhos e efeitos luminosos.
- Imagem da casa, placas solares e paisagem.
- Ar-condicionado e elementos promocionais.
- Posicionamento, alinhamento e espaçamento de todos os elementos.

A composição reconstruída deve ficar visualmente indistinguível da imagem original quando todas as camadas estiverem visíveis.

**Não utilize inteligência artificial generativa para recriar textos, números ou logotipos.** Utilize extração da imagem original ou reconstrução vetorial controlada.

## 1. CONFIGURAÇÃO DO PROJETO

- Resolução: 1920 × 1080 pixels.
- Proporção: 16:9.
- FPS futuro: 30.
- Tecnologia: React + TypeScript + Remotion.
- Elementos visuais exportados em PNG com transparência ou SVG quando apropriado.
- Todas as camadas devem manter suas coordenadas exatas em relação à imagem original.

## 2. SEPARAÇÃO DAS CAMADAS

### GRUPO A — BACKGROUND

Criar uma camada exclusiva contendo:

- Céu noturno azul-esverdeado.
- Casa moderna com placas solares.
- Paisagem e vegetação.
- Textura quadriculada tecnológica.
- Iluminação e gradientes originais.

Remova somente os elementos gráficos sobrepostos, reconstruindo cuidadosamente as regiões ocultas.

Salvar como `background.png`.

### GRUPO B — LOGOTIPO

Isolar o logotipo completo da Giotto Energia, incluindo símbolo, nome e slogan.

Salvar como `logo.png`, com fundo transparente.

Não modificar o desenho do logotipo.

### GRUPO C — TÍTULOS

Separar individualmente:

1. `black-friday.png` — BLACK FRIDAY.
2. `primeira-parcela.png` — Primeira parcela só daqui a.
3. `90-dias.png` — 90 DIAS!
4. `confira-ofertas.png` — Confira nossas ofertas.

Preservar sombras, brilhos e efeitos de luminosidade.

### GRUPO D — OFERTAS

Existem cinco ofertas. Cada oferta deve ter três componentes independentes:

1. Caixa com borda verde e fundo escuro.
2. Etiqueta verde indicando a potência.
3. Texto completo com parcelamento e valor à vista.

Conteúdo obrigatório:

**Oferta 1 — 315 kWh**
- 36x de R$ 329,72
- À vista: R$ 7.900,00

**Oferta 2 — 471 kWh**
- 36x de R$ 435,23
- À vista: R$ 9.900,00

**Oferta 3 — 628 kWh**
- 36x de R$ 531,16
- À vista: R$ 11.900,00

**Oferta 4 — 785 kWh**
- 36x de R$ 672,63
- À vista: R$ 15.300,00

**Oferta 5 — 942 kWh**
- 36x de R$ 742,97
- À vista: R$ 16.900,00

Organizar cada oferta como um grupo, mas manter seus componentes independentes para permitir animações de entrada, escala e movimento.

### GRUPO E — CONDIÇÕES

Separar:

- CONDIÇÕES ESPECIAIS.
- Até 36x no boleto, sujeito à análise de crédito.
- Ou até 21x no cartão de crédito!

### GRUPO F — SORTEIO DO AR-CONDICIONADO

Isolar:

1. Banner verde com cantos arredondados.
2. Texto principal do banner.
3. Texto em destaque sobre o sorteio.
4. Imagem do ar-condicionado, com transparência.
5. Texto “9000 BTUs”.
6. Brilhos e efeitos luminosos associados ao produto.

Preservar exatamente o conteúdo e as características visuais do anúncio original.

### GRUPO G — RODAPÉ

Separar:

- APROVEITE A BLACK FRIDAY GIOTTO ENERGIA!
- Consulte condições de pagamento e participação no sorteio.
- Linhas decorativas verdes da parte inferior.

## 3. PROCESSO DE EXTRAÇÃO

Analise as posições e dimensões dos elementos na imagem original.

Utilize processamento de imagens, máscaras, recortes com canal alfa e reconstrução vetorial quando necessário.

Para elementos com fundo incorporado, remova o fundo sem cortar contornos, brilhos ou sombras.

Na reconstrução de regiões ocultas, preserve a continuidade visual do cenário.

Se algum elemento não puder ser extraído com precisão, reconstrua-o por SVG ou HTML/CSS com características equivalentes às originais.

Não substitua elementos da identidade visual por versões genéricas.

Não aplique modificações artísticas.

## 4. ESTRUTURA DOS ARQUIVOS

Crie a seguinte organização:

```text
giotto-motion/
├── public/
│   └── assets/
│       ├── background/
│       ├── logo/
│       ├── titles/
│       ├── offers/
│       │   ├── offer-315/
│       │   ├── offer-471/
│       │   ├── offer-628/
│       │   ├── offer-785/
│       │   └── offer-942/
│       ├── conditions/
│       ├── promotion/
│       ├── footer/
│       └── effects/
├── src/
│   ├── components/
│   ├── compositions/
│   └── data/
│       └── layers.json
└── previews/
```

O arquivo `layers.json` deve registrar, para cada elemento:

- Identificador.
- Nome.
- Arquivo de origem.
- Coordenadas X e Y.
- Largura e altura.
- Ordem de sobreposição (z-index).
- Centro de transformação para animação.

As camadas exportadas devem permitir reconstruir a arte sem necessidade de reposicionamento manual.

## 5. RECONSTRUÇÃO NO REMOTION

Prepare uma composição React chamada `GiottoBlackFriday`.

Ela deve inicialmente exibir todos os elementos, sem nenhuma animação.

Crie componentes reutilizáveis para as ofertas e mantenha as propriedades de cada uma organizadas em dados estruturados.

O objetivo é que, posteriormente, cada elemento possa receber movimentos independentes.

## 6. VALIDAÇÃO VISUAL OBRIGATÓRIA

Antes de finalizar:

1. Renderize um frame estático em 1920 × 1080.
2. Compare esse frame com a imagem original.
3. Verifique alinhamento, proporções, cores e tipografia.
4. Confira cuidadosamente os cinco preços.
5. Verifique se os elementos estão completos e se não há partes cortadas.
6. Gere uma imagem de comparação visual lado a lado.
7. Gere, se possível, um mapa de diferenças entre a referência e a reconstrução.

Corrija divergências antes de considerar o trabalho concluído.

Se existir alguma limitação de fidelidade, identifique exatamente quais elementos foram afetados.

## 7. ENTREGÁVEIS

Entregue:

- Projeto Remotion organizado.
- Elementos separados com transparência.
- Fundo sem os elementos publicitários.
- Arquivo JSON com posicionamento das camadas.
- Frame renderizado com a arte completa.
- Comparação com a imagem original.
- Lista de elementos preparados para animação.

**Não iniciar os movimentos nesta etapa.**

O objetivo é obter uma composição visualmente fiel e completamente separada, que servirá como base para o motion graphic profissional de 10 segundos.