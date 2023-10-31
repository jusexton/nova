# Nova

Self-host open source discord bot with a focus on providing quality core discord management tools along with
configurable features from endless domains.

## Getting Started

The easiest way to get started is using `docker-compose`.

```yaml
version: '3'
services:
  nova:
    image: nova:latest
    container_name: nova_bot
    restart: always
    volumes:
      - type: bind
        source: <source to config file here>
        target: /app/config.txt
```

```toml
[nova]
token = "123"

[nova.extensions]
"gw2" = {}
"poll" = {}
```

## Core and Extensions

- [Core](docs/core.md)
- [Guild Wars 2](docs/gw2.md)

