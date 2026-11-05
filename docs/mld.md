COMPTE(
    id_compte PK,
    identifiant,
    actif
)

AGENT(
    id_agent PK,
    nom, prenom, email,
    id_compte FK -> COMPTE, UNIQUE
)

VENDEUR(
    id_vendeur PK,
    nom, prenom, telephone, email
)

ACHETEUR(
    id_acheteur PK,
    nom, prenom, telephone,
    budget_max, superficie_min,
    chambres_min, garage_souhaite,
    id_agent FK -> AGENT
)

COMMUNE(
    code_insee PK,
    nom
)

BIEN(
    id_bien PK,
    type_bien, adresse, superficie,
    nb_chambres, nb_garages,
    prix_demande, etape_vente,
    id_agent FK -> AGENT,
    id_vendeur FK -> VENDEUR,
    code_insee FK -> COMMUNE
)

ACHETEUR_COMMUNE(
    id_acheteur PK, FK -> ACHETEUR,
    code_insee PK, FK -> COMMUNE
)

PROPOSITION(
    id_proposition PK,
    date_proposition, prix_presente,
    decision, date_reponse, commentaire,
    id_acheteur FK -> ACHETEUR,
    id_bien FK -> BIEN
)

VISITE(
    id_visite PK,
    debut, fin, statut, compte_rendu,
    id_acheteur FK -> ACHETEUR,
    id_bien FK -> BIEN,
    id_agent FK -> AGENT
)

RENDEZ_VOUS(
    id_rdv PK,
    debut, fin, objet, statut,
    id_agent FK -> AGENT,
    id_vendeur FK -> VENDEUR
)

OFFRE(
    id_offre PK,
    date_offre, montant, statut,
    id_acheteur FK -> ACHETEUR,
    id_bien FK -> BIEN
)
