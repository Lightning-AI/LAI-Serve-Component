from lightning import LightningFlow, LightningApp
from lightning_serve import ServeFlow
from datetime import datetime

class RootFlow(LightningFlow):

    def __init__(self):
        super().__init__()

        self.serve = ServeFlow(
            strategy="ramped",
            script_path="./scripts/serve.py",
        )

    def run(self):
        # Deploy a new server every time the provided input changes
        # and shutdown the previous server once the new one is ready.
        self.serve.run(random_kwargs=datetime.now().strftime("%m/%d/%Y, %H:%M"))

    def configure_layout(self):
        return {"name": "Serve", "content": self.serve.proxy.url + "/predict"}

app = LightningApp(RootFlow(), debug=True)