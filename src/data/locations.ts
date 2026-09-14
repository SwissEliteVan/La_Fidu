export interface LocationPageData {
  slug: string;
  place: string;
  title: string;
  description: string;
  heading: string;
  intro: string;
  serviceContext: string;
}

export const locations: Record<'vevey' | 'riviera' | 'lausanne', LocationPageData> = {
  vevey: {
    slug: 'fiduciaire-vevey',
    place: 'Vevey',
    title: 'Fiduciaire à Vevey | LA FIDUCIAIRE',
    description: 'Fiduciaire pour indépendants, TPE et PME à Vevey : comptabilité, TVA, salaires, bouclement et pilotage selon le mandat.',
    heading: 'Une fiduciaire pour les entreprises et indépendants à Vevey',
    intro: 'LA FIDUCIAIRE accompagne les indépendants, TPE et PME qui exercent à Vevey avec une approche centrée sur la clarté, la proximité et des forfaits lisibles.',
    serviceContext: 'Le niveau d’accompagnement est adapté à la structure, au volume comptable et aux prestations réellement nécessaires.',
  },
  riviera: {
    slug: 'fiduciaire-riviera-vaudoise',
    place: 'Riviera vaudoise',
    title: 'Fiduciaire Riviera vaudoise | LA FIDUCIAIRE',
    description: 'Fiduciaire pour indépendants, TPE et PME sur la Riviera vaudoise : comptabilité et accompagnement adaptés au besoin réel.',
    heading: 'Une fiduciaire de proximité pour la Riviera vaudoise',
    intro: 'LA FIDUCIAIRE accompagne les indépendants, TPE et PME de la Riviera vaudoise avec une organisation digitale simple et une relation humaine.',
    serviceContext: 'Comptabilité courante, TVA, salaires, bouclement et pilotage sont cadrés selon le mandat retenu et la situation de l’entreprise.',
  },
  lausanne: {
    slug: 'fiduciaire-lausanne',
    place: 'Lausanne',
    title: 'Fiduciaire à Lausanne | LA FIDUCIAIRE',
    description: 'Fiduciaire pour indépendants, TPE et PME à Lausanne : comptabilité, salaires, TVA et pilotage selon le périmètre convenu.',
    heading: 'Une fiduciaire claire et accessible pour les entreprises à Lausanne',
    intro: 'LA FIDUCIAIRE accompagne les indépendants, consultants, TPE et PME qui exercent à Lausanne et recherchent un suivi comptable compréhensible et structuré.',
    serviceContext: 'L’accompagnement est défini à partir du volume, du nombre de collaborateurs et du niveau de suivi attendu.',
  },
};
