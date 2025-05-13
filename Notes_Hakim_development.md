- Création du modèle adresses pour stocker les adresses avec les champs requis :
    id
    label
    housenumber
    street
    postcode
    citycode
    latitude
    longitude

    (voir fichier models.py)

- Création et application des des migrations :
    python3 manage.py makemigrations
    python3 manage.py migrate

- Utilisation de Django REST Framework pour la création d'API REST
    pip install djangorestframework requests



TESTS PENDANT LA PHASE DE DEVELOPPEMENT :
    - On lance le serveur de dév en local : python3 manage.py runserver, le serveur tourne sur 'http://127.0.0.1:8000/'
    - On teste les endpoints des API préalablement configurées :
        curl -X POST http://127.0.0.1:8000/api/addresses/ \
        -H "Content-Type: application/json" \
        -d '{"q": "97 bd Malesherbes, 75008 Paris"}'

        Réponse : 
        {"id":2,"label":"97 Boulevard Malesherbes 75008 Paris","housenumber":"97","street":"Boulevard Malesherbes","postcode":"75008","citycode":"75108","latitude":"48.878839","longitude":"2.314693"}% 

    - Pour obtenir les risques d'une adresse (remplacez {id} par l'ID retourné par la première requête) :

        Réponse pour l'exemple :
            {"adresse":{"libelle":"97 Boulevard Malesherbes 75008 Paris","longitude":2.314693,"latitude":48.878838},"commune":{"libelle":"Paris","codePostal":"75008","codeInsee":"75108"},"url":"https://georisques.gouv.fr/mes-risques/connaitre-les-risques-pres-de-chez-moi/rapport2?typeForm=adresse&city=Paris&codeInsee=75108&lon=2.314693&lat=48.878839&adresse=97+Boulevard+Malesherbes+75008+Paris","risquesNaturels":{"inondation":{"present":false,"libelle":"Inondation"},"remonteeNappe":{"present":false,"libelle":"Remontée de nappe"},"risqueCotier":{"present":false,"libelle":"Risques côtiers (submersion marine, tsunami)"},"seisme":{"present":true,"libelle":"Séisme"},"mouvementTerrain":{"present":false,"libelle":"Mouvements de terrain"},"reculTraitCote":{"present":false,"libelle":"Recul du trait de côte"},"retraitGonflementArgile":{"present":false,"libelle":"Retrait gonflement des argiles"},"avalanche":{"present":false,"libelle":"Avalanche"},"feuForet":{"present":false,"libelle":"Feu de forêt"},"eruptionVolcanique":{"present":false,"libelle":"Volcan"},"cyclone":{"present":false,"libelle":"Vent violent"},"radon":{"present":true,"libelle":"Radon"}},"risquesTechnologiques":{"icpe":{"present":false,"libelle":"Installations industrielles classées (ICPE)"},"nucleaire":{"present":false,"libelle":"Nucléaire"},"canalisationsMatieresDangereuses":{"present":false,"libelle":"Canalisations de transport de matières dangereuses"},"pollutionSols":{"present":true,"libelle":"Pollution des sols"},"ruptureBarrage":{"present":false,"libelle":"Rupture de barrage"},"risqueMinier":{"present":false,"libelle":"Risques miniers"}}}%    

            On obtient les mêmes résultats que sur https://georisques.gouv.fr/mes-risques/connaitre-les-risques-pres-de-chez-moi/rapport2?typeForm=adresse&city=Paris&codeInsee=75108&lon=2.314693&lat=48.878839&adresse=97+Boulevard+Malesherbes+75008+Paris        