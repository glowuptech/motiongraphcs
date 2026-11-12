// Storyboard solicitado. Intervalos [início, fim), em frames.
// Planejamento; a composição animada depende da extração das camadas originais.
export const timeline = {
  fps: 30, width: 1920, height: 1080, durationInFrames: 300,
  opening: [0, 30], ninetyDays: [30, 66], offers: [66, 171],
  offerEntrances: {"315":66,"471":87,"628":108,"785":129,"942":150},
  conditions: [171, 198], promotion: [198, 246], footer: [246, 264],
  stableFinal: [264, 300],
} as const;
