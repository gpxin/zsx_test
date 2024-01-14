from scr.common import get_llm_response
from scr.observer import Observer
from scr.publisher import Publisher
from scr.system_clock import SystemClock


class Player(Publisher, Observer):
    def __init__(self, zh_name, role_script, chat_setting):
        super().__init__()
        self.zh_name = zh_name
        self.role_script = role_script
        self.chat_setting = chat_setting
        self.conversation_id = None
        self.response_history = {}
        self.input_history = {}
        self.sync_time = 0

    @property
    def history_response(self):
        response_list = [input_str for time_step, input_str in self.response_history.items()]
        return "\n".join(response_list)

    @property
    def history_input(self):
        input_list = [input_str for time_step, input_str in self.input_history.items()]
        return "\n".join(input_list)

    def play(self, following_plot):
        # 根据同步时间更新对话内容
        self.sync_time += 1
        if self.conversation_id is None:
            answer, self.conversation_id = get_llm_response(following_plot)
        else:
            answer, _ = get_llm_response(following_plot, self.conversation_id)
        self.input_history[self.sync_time] = following_plot
        self.response_history[self.sync_time] = answer
        return answer

    def notify(self, info):
        # 如果info是int代表的是系统时间更新
        if isinstance(info, SystemClock):
            self.sync_time = info.time
        # 如果更新的信息是
        elif isinstance(info, Player):
            pass


if __name__ == "__main__":
    print(123)
    player = Player()
