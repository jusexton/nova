import logging

from nova import Nova, config

logging.basicConfig(level=logging.INFO)

cfg = config.load()
cfg.extensions.append('gw2')
nova = Nova(cfg)
nova.run(cfg.token)
