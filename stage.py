from chat_manager import ChatManager
from scr.common import make_start_conversation
from config_loader import ConfigLoader
from controllable_player import ControllablePlayer
from scr.display import UIManager
from player import Player


class Scenario:
    def __init__(self, config_path):
        self.player_dict = {}
        self.conversation_history = {}
        self.scenario_config = ConfigLoader(config_path)
        self.ui_manager = None
        self.director = ChatManager(self.player_dict)
        self.scenario_init()

    def scenario_init(self):
        for player in self.scenario_config.init_conversation:
            player_script = self.scenario_config.players_script[player]
            player_zh_name = self.scenario_config.players[player]
            if player not in self.player_dict:
                # 主演是玩家控制的
                if player in self.scenario_config.controllable_players:
                    rival_player = self.scenario_config.controllable_players[player]
                    self.player_dict[player] = ControllablePlayer(player_zh_name, player_script, rival_player)
                else:
                    self.player_dict[player] = Player(
                        player_zh_name, player_script, self.scenario_config.chat_setting[player]
                    )
            if player in self.scenario_config.init_conversation:
                # 初始化对手演员，对手演员一定不是ControllablePlayer，因为ControllablePlayer来自用户输入
                for rival in self.scenario_config.init_conversation[player]:
                    rival_zh_name = self.scenario_config.players[rival]
                    # 对手演员只会被一个ControllablePlayer初始化一次
                    if rival in self.player_dict:
                        raise ValueError(f"对手演员{rival}已经被初始化过！")
                    self.player_dict[rival] = Player(
                        rival_zh_name,
                        self.scenario_config.players_script[rival],
                        self.scenario_config.chat_setting[rival],
                    )
                    # 使用角色设定prompt初始化对话
                    init_prompt = make_start_conversation(
                        self.player_dict[player].role_script, self.player_dict[rival].role_script
                    )
                    # 触发rival的回复
                    self.player_dict[rival].play(init_prompt)
        self.ui_manager = UIManager(self.player_dict, self.scenario_config)

    def start(self):
        self.director.start()
        self.ui_manager.launch()
