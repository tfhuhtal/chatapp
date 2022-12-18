# chatapp

Sovelluksen nettisivu: https://chatapp3000.fly.dev

##Ominaisuudet

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

##Testaus

Tuotannossa voi testata sovellusta näillä ohjeilla:
1. Kloonaa repo `git clone git@github.com:tfhuhtal/chatapp.git`
2. Poista `db.py`-moduulista 5. rivin kohta `.replace("://", "ql://", 1)`.
3. Luo oma `.env`, jonne luo omat ympäristömuuttujat `SECRET_KEY=` ja `DATABASE_URL=`.
4. Aja terminaalissa `pip install requirements.txt`. 
5. Aja terminaalissa `source venv/bin/activate` sekä luo terminaalissa PostgreSQL-tietokannan taulut `psql < schema.sql`.
6. Lopuksi aja terminaalissa `flask run`.