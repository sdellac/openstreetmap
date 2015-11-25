# Open Street Map

## Server

### Install dependencies

```
npm install
```

### Run the server

```
node server.js -i [id]
```

*The `id` corresponds to the server index in the configuration file `server.conf`.*

### Pour tester

```
curl -i -H "Content-Type: application/json" -X POST -d '{"client":{"id":5,"position":{"lat":2,"lon":16}}}' http://localhost:8080
```
