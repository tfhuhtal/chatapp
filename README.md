# chatapp
This is a repository for my awesome chat app!

Sovelluksen nettisivu: https://chatapp3000.fly.dev
Tämän hetkinen tilanne sovelluksessa:
- voi luoda uuden käyttäjätunnuksen
- voi kirjautua sivustolle
- näkee sovelluksen etusivulta omat keskustelut
- voi luoda uuden keskustelun
- voi liittyä keskusteluun
- voi kirjautua ulos

Tuotannossa voi testata sovellusta näillä ohjeilla:
1. kloonaa repo omaan haluamaasi kansioosi
2. poista db.py ohjelmasta kohta ".replace("://", "ql://", 1)"
3. aseta omat luo oma .env kansio ja sinne omat secret_key ja database_url muuttujat
4. pip install requirements.txt
5. venv ja psql päälle ja luo schema.sql mukaiset taulut
6. flask run


Tässä on keskustelusovellukseni jossa on seuraavat ominaisuudet kurssisivuilta:
- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
- Käyttäjä näkee sovelluksen etusivulla listan omista ryhmistä sekä jokaisen ryhmän viestien määrän ja viimeksi lähetetyn viestin ajankohdan.
- Käyttäjä voi luoda alueelle uuden ryhmän antamalla ryhmän nimen.
- Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ryhmään.
- Käyttäjä voi muokata luomansa ryhmän nimeä sekä lähettämänsä viestin sisältöä. Käyttäjä voi myös poistaa ryhmän tai viestin.
- Käyttäjä voi etsiä kaikki viestit, joiden osana on annettu sana.
- Ylläpitäjä voi lisätä ja poistaa keskustelualueita.
- Ylläpitäjä voi luoda salaisen alueen ja määrittää, keillä käyttäjillä on pääsy alueelle.
