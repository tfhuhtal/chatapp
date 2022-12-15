# chatapp
This is a repository for my awesome chat app!

Sovelluksen nettisivu: https://chatapp3000.fly.dev
Tässä on keskustelusovellukseni jossa on seuraavat ominaisuudet:
- voi luoda uuden käyttäjätunnuksen
- voi kirjautua sivustolle
- näkee sovelluksen etusivulta omat keskustelut ja kuinka monta osallistujaa keskustelussa on
- voi luoda uuden keskustelun
- voi liittyä keskusteluun mikäli keskustelu on julkinen
- voi lähettää viestin keskusteluun
- voi kirjautua ulos
- voi poistaa käyttäjiä keskusteluista, mikäli on ylläpitäjä
- käyttäjä voi itse poistua huoneesta
- voi muokata huoneen nimeä
- Käyttäjä voi etsiä kaikki viestit, joiden osana on annettu sana.
- muokata lähettämäänsä viestiä
- huoneen ylläpitäjä voi muokata keskustelun tilaa julkiseksi tai yksityiseksi

Tuotannossa voi testata sovellusta näillä ohjeilla:
1. kloonaa repo omaan haluamaasi kansioosi
2. poista db.py ohjelmasta kohta ".replace("://", "ql://", 1)"
3. luo oma .env tiedosto ja sinne omat secret_key ja database_url muuttujat
4. pip install requirements.txt
5. venv ja psql päälle ja luo schema.sql mukaiset taulut
6. flask run