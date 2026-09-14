export interface Service {
  slug: string;
  title: string;
  shortTitle: string;
  summary: string;
  intro: string;
  points: string[];
}

export const services: Service[] = [
  {
    slug: 'independants',
    title: 'Comptabilité pour indépendants',
    shortTitle: 'Indépendants',
    summary: 'Structurer la comptabilité courante et garder une lecture claire des obligations de l’activité.',
    intro: 'Un accompagnement conçu pour les indépendants, consultants, freelances et raisons individuelles qui souhaitent une comptabilité organisée et compréhensible.',
    points: [
      'Tenue comptable et organisation des pièces',
      'Rapprochements et suivi courant',
      'Préparation des éléments utiles au bouclement',
      'Explications claires sur les prochaines étapes',
    ],
  },
  {
    slug: 'pme',
    title: 'Comptabilité et pilotage pour PME',
    shortTitle: 'PME',
    summary: 'Relier la tenue comptable à une lecture utile de la rentabilité et de la trésorerie.',
    intro: 'Pour les TPE, Sàrl et PME qui ont besoin d’un suivi structuré, de chiffres lisibles et d’un interlocuteur identifié.',
    points: [
      'Comptabilité courante et suivi des pièces',
      'Bouclement selon le périmètre du mandat',
      'Suivi de trésorerie et analyse de rentabilité selon l’offre',
      'Reporting et rendez-vous de pilotage selon l’offre retenue',
    ],
  },
  {
    slug: 'salaries',
    title: 'Gestion des salaires',
    shortTitle: 'Salaires',
    summary: 'Organiser la gestion courante des salaires et le suivi social prévu dans le mandat.',
    intro: 'Une gestion structurée pour les entreprises qui emploient des collaborateurs et veulent centraliser les opérations courantes liées aux salaires.',
    points: [
      'Gestion courante des salaires selon le mandat',
      'Suivi AVS et assurances sociales',
      'Organisation des informations nécessaires',
      'Coordination avec la comptabilité courante',
    ],
  },
  {
    slug: 'tva',
    title: 'TVA',
    shortTitle: 'TVA',
    summary: 'Préparer et structurer les informations nécessaires au suivi TVA de l’entreprise.',
    intro: 'La TVA est intégrée au suivi comptable lorsque le mandat et la situation de l’entreprise le prévoient.',
    points: [
      'Organisation des données comptables utiles',
      'Contrôles de cohérence dans le cadre du mandat',
      'Préparation du suivi périodique',
      'Explications sur les éléments qui nécessitent votre attention',
    ],
  },
  {
    slug: 'creation-entreprise',
    title: 'Création d’entreprise',
    shortTitle: 'Création d’entreprise',
    summary: 'Poser des bases administratives et comptables claires dès le démarrage.',
    intro: 'Un accompagnement pour structurer les premières étapes comptables et administratives de votre activité sans ajouter de complexité inutile.',
    points: [
      'Cadrage des besoins comptables',
      'Organisation des flux et des pièces',
      'Choix d’un niveau d’accompagnement adapté',
      'Préparation d’un suivi clair dès le lancement',
    ],
  },
  {
    slug: 'bouclement',
    title: 'Bouclement annuel',
    shortTitle: 'Bouclement annuel',
    summary: 'Préparer la clôture des comptes de manière structurée et compréhensible.',
    intro: 'Le bouclement rassemble les éléments comptables de l’exercice et permet d’obtenir une lecture structurée de la période écoulée.',
    points: [
      'Préparation et contrôle des éléments comptables',
      'Organisation des informations manquantes',
      'Clôture selon le périmètre convenu',
      'Synthèse des principaux points à comprendre',
    ],
  },
  {
    slug: 'conseil-fiscal',
    title: 'Conseil fiscal',
    shortTitle: 'Conseil fiscal',
    summary: 'Comprendre les obligations et préparer les décisions fiscales avec une information structurée.',
    intro: 'L’accompagnement fiscal est adapté à la situation réelle de l’entreprise et au périmètre du mandat, sans promesse d’optimisation absolue.',
    points: [
      'Lecture de la situation dans le cadre du mandat',
      'Explication des obligations applicables',
      'Préparation des éléments nécessaires',
      'Identification des sujets qui demandent une décision ou une validation',
    ],
  },
];
