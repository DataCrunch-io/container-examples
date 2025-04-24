# Health-check and lifecycle management

This example container demonstrates several lifecycle-management aspects:

* fine-grained control over the maximum number of concurrent requests each container replica can serve
* health-check endpoint that is aware of requests being served
* `SIGTERM` handling for graceful shutdown.

Please see [this documentation article](https://docs.datacrunch.io/containers/scaling) for additional discussion.