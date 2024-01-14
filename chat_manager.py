import threading
import time

from controllable_player import ControllablePlayer
from player import Player


class ChatManager(threading.Thread):
    def __init__(self, player_dict):
        threading.Thread.__init__(self)
        self.player_dict = player_dict
        self.system_time = 1

    def run(self):
        """
        定时查询controllable的player是否有输入，如果有的话触发对话更新
        :return: None
        """
        while True:
            time.sleep(3)
            for player, player_handler in self.player_dict.items():
                if isinstance(player_handler, ControllablePlayer):
                    # 有新的输入需要处理
                    if not player_handler.response_ready:
                        rival_player_handler = self.player_dict[player_handler.rival_player]
                        steps_num = len(rival_player_handler.chat_setting)
                        for step_time in range(1, steps_num + 1):
                            self.update_player(rival_player_handler, self.system_time, step_time)
                            # 把此轮需要更新但未被联动更新的角色全部更新
                            self.update_all_working_players(step_time)
                            # 把和此轮对话无关的player的时间均同步到最新的时间,以保证对话之间的时间同步
                            self.update_all_players()
                            self.system_time += 1
                        player_handler.response(rival_player_handler.last_response, steps_num)
                        print(f"来自{player}的对话更新成功！")
            print(f"heart beat~ system time: {self.system_time}")

    def update_player(self, rival_player_handler, now_system_time, turn_time):
        if not rival_player_handler.has_been_update(now_system_time):
            # -1优先级最高
            task_turn_time = -1 if -1 in rival_player_handler.chat_setting else turn_time
            # todo目前同一时刻多个chat_setting按第一个处理
            task_name = list(rival_player_handler.chat_setting[task_turn_time].keys())[0]
            dependency_info = rival_player_handler.chat_setting[task_turn_time][task_name]
            input_str = []
            for dependency_player, content_time in dependency_info.items():
                # 相对时间
                abs_time = content_time - turn_time
                dependency_time = now_system_time + abs_time
                dependency_player_handler = self.player_dict[dependency_player]
                if not dependency_player_handler.has_been_update(dependency_time):
                    self.update_player(dependency_player_handler, now_system_time, turn_time)
                # 将依赖输入组合起来作为player的输入
                if isinstance(dependency_player_handler, Player):
                    dependency_str = dependency_player_handler.get_time_response(dependency_time)
                else:
                    dependency_str = dependency_player_handler.get_time_input(dependency_time)
                input_str.append(f"{dependency_player_handler.zh_name}: {dependency_str}")
            rival_player_handler.play("\n".join(input_str))

    def update_all_working_players(self, turn_time):
        for _player, player_handler in self.player_dict.items():
            if isinstance(player_handler, Player) and (
                turn_time in player_handler.chat_setting or -1 in player_handler.chat_setting
            ):
                # 有更新任务但未被联动更新的角色，进行更新
                self.update_player(player_handler, self.system_time, turn_time)

    def update_all_players(self):
        for _player, player_handler in self.player_dict.items():
            player_handler.sync_time = self.system_time
