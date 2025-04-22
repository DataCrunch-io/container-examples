# Hello World! Container

Here is an example of a simple container compatible with DataCrunch serverless containers.

Build:

```bash
docker build -t $YOUR_REGISTRY/hello-world:v1 .
```

Run container locally to test it:
```bash
docker run -d -p 8989:8989 $YOUR_REGISTRY/hello-world:v1
```

To run a request against the container, run 
```bash
curl localhost:8989/hello-world
```

Depending on whether you have a GPU available this  will give you the following output:
```json
{"message":"Hello world, I can run on cpu|gpu!"}
```

To make the container available to DataCrunch Containers, it needs to be pushed to a Docker registry:
```bash
docker push $YOUR_REGISTRY/hello-world:v1
```

