# Open Street Map

## Server

### Install dependencies

```
npm install
```

### Run the server

```
./bin/www -i [id]
```

*The `id` corresponds to the server index in the configuration file `server.conf`.*

### Test

```
curl -i -H "Content-Type: application/json" -X POST -d '{"client":{"ID":5,"Position":{"lat":2,"lon":16}}}' http://localhost:8080
```
