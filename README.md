# ***REMOVED*** Arbetsprov

## Uppgiten:
Programmet ska:
* Skicka meddelande till en mottagare (till exempel identifierad med epostadress, telefonnummer, användarnamn eller liknande)
* Hämta nya (sedan förra hämtningen) meddelanden till mottagare
* Ta bort ett eller flera meddelanden för en mottagare
* Hämta tidsordnade meddelanden till en mottagare enligt start och stopp index

## Starta monogodb databasen
Installera och starta mongodb. Jag har version v3.6.2 av mongodb. Testerna kräver en databas igång, en förbättring är att ersätta databasen med mockad version, kanske mongomock.

## Starta applikationen
```bash
pip install pipenv
pipenv install
mv env.example .env `#Editera env.example, kolla att database url passar`
pipenv shell
```

## Kör testerna
```bash
nosetests
```

## Start the applikationen
`flask run`

## Exemple requests
### Skicka meddelande
```Bash
curl -H "Content-Type: application/json" -X POST -d '{"message":"God day example_user!"}' http://localhost:5000/messages/example_user
```
### Hämta en eller flera meddelanden
```Bash
curl 'http://localhost:5000/messages/example_user/<id>'
curl 'http://localhost:5000/messages/example_user/<id1>,<id2> ...'
```
### Radera en eller flera meddelanden
```Bash
curl -X DELETE 'http://localhost:5000/messages/example_user/<id>'
curl -X DELETE 'http://localhost:5000/messages/example_user/<id1>,<id2>...'
```
### Hämta olästa meddelanden
```Bash
curl 'http://localhost:5000/messages/example_user/unread'
```
### Hämta meddelanden mellan start och/eller stop tidpunkt
```Bash
curl 'http://localhost:5000/messages/example_user?start=2018-02-28T22:01:31&stop=2018-03-01T20:22:07'
curl 'http://localhost:5000/messages/example_user?start=2018-02-28T22:01:31'
curl 'http://localhost:5000/messages/example_user?stop=2018-03-01T20:22:07'
```