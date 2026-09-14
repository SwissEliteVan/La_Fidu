export interface PricingPlan {
  name: string;
  price: string;
  target: string;
  features: string[];
  note?: string;
}

export const pricingPlans: PricingPlan[] = [
  {
    name: 'Essentiel',
    price: 'Dès CHF 190 / mois HT',
    target: 'Pour une activité indépendante ou une raison individuelle simple.',
    features: [
      'Tenue comptable',
      'Jusqu’à 40 pièces par mois',
      'Rapprochement bancaire simple',
      'Espace client sécurisé',
      'Entretien annuel de synthèse',
    ],
  },
  {
    name: 'Sérénité',
    price: 'Dès CHF 390 / mois HT',
    target: 'Pour un indépendant établi, une petite entreprise ou une Sàrl.',
    features: [
      'Contenu de l’offre Essentiel',
      'Jusqu’à 120 pièces par mois',
      'Jusqu’à 2 collaborateurs',
      'Gestion courante des salaires',
      'Suivi AVS et assurances sociales',
      'Deux rendez-vous annuels',
      'Tableau de bord simplifié',
    ],
  },
  {
    name: 'Pilotage',
    price: 'Dès CHF 790 / mois HT',
    target: 'Pour une PME qui veut suivre sa rentabilité et sa trésorerie.',
    features: [
      'Contenu de l’offre Sérénité',
      'Jusqu’à 300 pièces par mois',
      'Jusqu’à 8 collaborateurs',
      'Reporting financier périodique',
      'Analyse de rentabilité et suivi de trésorerie',
      'Budget et prévisions',
      'Rendez-vous trimestriel et conseil de gestion',
    ],
  },
  {
    name: 'Sur mesure',
    price: 'Dès CHF 1’290 / mois HT ou sur devis',
    target: 'Pour une PME structurée avec des besoins plus spécifiques.',
    features: [
      'Comptabilité analytique selon les besoins',
      'Reporting personnalisé',
      'Gestion de plusieurs entités selon le mandat',
      'Consolidation selon les besoins',
      'Accompagnement stratégique',
    ],
    note: 'Le périmètre exact est défini avant le début du mandat.',
  },
];
