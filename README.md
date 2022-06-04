# Lightning Serve

Lightning provides python based serving orchestration layer for serving any frameworks.

## API

The Lightning Serve library exposes 1 main class: `ServeFlow` and associated strategies such as `BlueGreenStrategy`.

```py
from lightning import LightningFlow, LightningApp
from lightning_serve import ServeFlow
from lightning_serve.strategies import BlueGreenStrategy
from datetime import datetime

class RootFlow(LightningFlow):

    def __init__(self):
        super().__init__()

        self.serve = ServeFlow(
            strategy=BlueGreenStrategy(),
            script_path="./scripts/serve.py",
        )

    def run(self):
        # Deploy a new server every time the provided input changed and shutdown the previous when the new one is ready.
        self.serve.run(random_kwargs=datetime.now().strftime("%m/%d/%Y, %H:%M"))

    def configure_layout(self):
        return {"name": "Serve", "content": self.serve.url + "/predict"}

app = LightningApp(RootFlow())
```

## Currently Support Strategy:

Inspired from [Kubernetes deployment strategies](https://github.com/ContainerSolutions/k8s-deployment-strategies)

[x] recreate: terminate the old version and release the new one
[x] ramped: release a new version on a rolling update fashion, one after the other
[x] blue/green: release a new version alongside the old version then switch traffic
[] canary: release a new version to a subset of users, then proceed to a full rollout
[x] a/b testing: release a new version to a subset of users in a precise way
    - [x] (HTTP headers)
    - [] cookie
    - [x] weight
[] shadow: release a new version alongside the old version. Incoming traffic is mirrored to the new version and doesn't impact the response.