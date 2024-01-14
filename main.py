import os

from scr.common import PROJECT_PATH
from stage import Scenario

if __name__ == "__main__":
    scenario = Scenario(os.path.join(PROJECT_PATH, "config/scenario_config.toml"))
    scenario.start()
