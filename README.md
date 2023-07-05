To run the application 

Create the shinylive app using

```
shiny create myapp
pip install shinylive
```

run the server at port 8080:

```
shinylive export myapp site && python3 -m http.server --directory site 8008 --bind 127.0.0.1
```