# Animações de Black Friday da Giotto Mobilidade

Cada MP4 tem 10 segundos em Full HD a 30 fps, sem áudio. As motos entram pela direita. As demais camadas entram em sequência e a arte completa fica em tela nos cinco segundos finais.

- [Banner Mobilidade](banner_mobilidade_v01.mp4)
- [Banner Mobilidade Elétrica](banner_mobilidade_eletrica_v01.mp4)
- [Bis Elétrica](bis_eletrica_v01.mp4)

O arquivo renderizar_motion.py na raiz do projeto contém a sequência de entradas. Cada arte tem ajustes individuais em 03_projeto_animacao/motion.json. Para renderizar novamente, execute na raiz do projeto, por exemplo, `/usr/bin/python3 renderizar_motion.py bis_eletrica`. O comando usa Pillow e FFmpeg e substitui a exportação v01 correspondente.
