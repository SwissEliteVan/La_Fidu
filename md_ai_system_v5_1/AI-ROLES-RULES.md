# RÈGLES DE RÔLES IA — DOUBLE CONTRÔLE

Règle système (N0). Elle rend obligatoire ce que le workflow suppose depuis le
début : **la vérification est faite par une autre IA que celle qui a produit**.

## 1. Principe

Une IA ne se vérifie pas elle-même. Deux paires sont donc indépendantes :

| Paire | Production | Contrôle |
|---|---|---|
| Analyse | IA1 établit les exigences et l'état réel | IA2 refait le constat depuis les sources et vérifie IA1 |
| Réalisation | IA3 exécute | IA4 contrôle le réel produit |

IA2 doit être une IA **différente** d'IA1.
IA4 doit être une IA **différente** d'IA3.

IA1 et IA3 peuvent être la même IA. IA2 et IA4 peuvent être la même IA.
Une organisation à deux IA suffit donc : A fait IA1 et IA3, B fait IA2 et IA4.

## 2. Configuration

Bloc `ai_roles` de `.md-ai-system/CONFIG.json` :

```json
"ai_roles": {
  "double_control": "required",
  "independent_pairs": [["ia1", "ia2"], ["ia3", "ia4"]],
  "declared_providers": {"ia1": "A", "ia2": "B", "ia3": "A", "ia4": "B"}
}
```

- `double_control` : `required` (défaut) ou `degraded`.
- `independent_pairs` : les couples qui doivent être tenus par deux IA distinctes.
- `declared_providers` : le nom de l'IA prévue pour chaque étape. Le nom est libre
  (`claude`, `chatgpt`, `deepseek`, `gemini`, `qwen`, `interne-1`…) mais doit
  identifier l'IA de façon stable pendant tout le projet.

`degraded` n'est pas un raccourci de confort : il supprime la vérification
indépendante. Il exige une décision humaine explicite, enregistrée comme décision
verrouillée avec sa justification, et l'IA doit rappeler à chaque contrôle que le
double contrôle est désactivé.

## 3. Enregistrement

Chaque étape terminée enregistre dans l'état de la catégorie :

```json
"ia2": {"provider": "B", "verdict": "VALIDÉ", "ts": "…", "summary": "…"}
```

et une ligne d'audit portant le même `provider`.

Conséquence : on peut prouver après coup, sans la conversation, **qui a produit et
qui a vérifié**. Une catégorie validée sans trace d'IA distincte est un écart.

## 4. Contrôles automatiques

`python TOOLS/mdai.py finish-stage` refuse :

- une étape de contrôle réalisée par la même IA que l'étape produite ;
- une étape réalisée par une IA différente de celle déclarée pour ce rôle
  (contournable par `--force`, qui ne contourne jamais l'indépendance) ;
- une étape de contrôle alors que l'étape produite n'a pas été enregistrée.

`python TOOLS/validate_system.py` refuse un cycle dont les paires ne sont pas
indépendantes, ou dont un fournisseur manque alors que `double_control` est
`required`.

## 5. Ce que l'IA de contrôle ne doit pas faire

- reprendre le résumé de l'étape produite comme s'il s'agissait du réel ;
- valider parce que « cela paraît cohérent » ;
- se contenter des fichiers cités par l'étape produite ;
- corriger elle-même l'écart qu'elle constate : elle refuse, la correction
  appartient au cycle suivant.

Une vérification qui n'a rien relu du réel n'est pas une vérification.

## 6. Changement d'IA en cours de projet

Autorisé. Le nom déclaré est mis à jour dans `CONFIG.json` avec
`python TOOLS/mdai.py init --ia2 <nom>`. Les cycles déjà validés gardent la trace
de l'IA qui les a réellement traités : l'historique n'est pas réécrit.

La seule contrainte permanente est l'indépendance des paires, pas l'identité des
fournisseurs.
