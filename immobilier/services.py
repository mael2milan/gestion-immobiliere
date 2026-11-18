from decimal import Decimal

from .models import Bien


def score_compatibilite(acheteur, bien, communes):
    score = 0

    # Commune : 35 points
    if not communes or bien.commune_id in communes:
        score += 35

    # Budget : 30 points
    if bien.prix_demande <= acheteur.budget_max:
        score += 30
    elif bien.prix_demande <= acheteur.budget_max * Decimal("1.10"):
        score += 15

    # Superficie : 20 points
    if bien.superficie >= acheteur.superficie_min:
        score += 20
    elif bien.superficie >= acheteur.superficie_min * 0.90:
        score += 10

    # Chambres : 10 points
    if bien.nb_chambres >= acheteur.chambres_min:
        score += 10

    # Garage : 5 points
    if not acheteur.garage_souhaite or bien.nb_garages >= 1:
        score += 5

    return score


def recommander_biens(acheteur, seuil=65):
    communes = {
        commune.code_insee
        for commune in acheteur.communes_recherchees.all()
    }

    biens = Bien.objects.filter(
        etape_vente=Bien.EtapeVente.MISE_EN_VENTE
    ).select_related("commune", "agent")

    recommandations = []

    for bien in biens:
        score = score_compatibilite(acheteur, bien, communes)

        if score >= seuil:
            recommandations.append({
                "bien": bien,
                "score": score,
            })

    recommandations.sort(
        key=lambda resultat: (
            -resultat["score"],
            resultat["bien"].prix_demande,
            resultat["bien"].pk,
        )
    )

    return recommandations[:5]