import toml


def chat_setting_reform(player_setting):
    setting = {}
    for chat_task, chat_setting in player_setting.items():
        if chat_setting["chat_time"] not in setting:
            setting[chat_setting["chat_time"]] = {}
        setting[chat_setting["chat_time"]][chat_task] = chat_setting["dependence"]
    return setting


class ConfigLoader:
    def __init__(self, config_path: str):
        self._reload(config_path)

    def _reload(self, config_path: str):
        self.config = toml.load(config_path)
        self.controllable_players = self.config["controllable"]["controllable_players"]
        self.players = self.config["players"]
        self.players_script = self.config["script"]
        self.init_conversation = self.config["init_conversation"]
        self.chat_setting = {
            player: chat_setting_reform(player_setting)
            for player, player_setting in self.config["chat_setting"].items()
        }


if __name__ == "__main__":
    config = ConfigLoader("config/scenario_config.toml")
    print(123)
