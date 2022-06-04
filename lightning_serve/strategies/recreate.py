from lightning import LightningWork
from lightning.structures import List
from lightning_serve.strategies.base import Strategy


class RecreateStrategy(Strategy):

    def run(self, serve_works: List[LightningWork]):
        if len(serve_works) < 2:
            return {w.url: 1.0 for w in serve_works}

        latest_serve_work = serve_works[-1]
        # Stop before the new service is up and running.
        for serve_work in serve_works[:-1]:
            serve_work.stop()

        if latest_serve_work.url != "":
            return {latest_serve_work.url: 1.0}
        else:
            return {}