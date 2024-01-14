from typing import Dict

import gradio as gr

from controllable_player import ControllablePlayer


class UIManager(object):
    def __init__(self, player_dict: Dict, scenario_config):
        self.player_dict = player_dict
        self.scenario_config = scenario_config
        self.player_zh_name_map = {}
        self.module_dict = {}
        self.handle = self.init_ui()

    def init_ui(self):
        with gr.Blocks() as ui:
            for player, player_handle in self.player_dict.items():
                self.module_dict[player] = {}
                self.player_zh_name_map[player_handle.zh_name] = player_handle
                with gr.Tab(player_handle.zh_name):
                    gr.Markdown("### 历史对话信息")
                    player_history_text = gr.Textbox(label=f"输入指令历史", lines=6, value=player_handle.history_input)
                    self.module_dict[player]["input"] = player_history_text
                    rival_history_text = gr.Textbox(
                        label=f"{player_handle.zh_name}返回的结果", lines=6, value=player_handle.history_response
                    )
                    self.module_dict[player]["output"] = rival_history_text
                    # 对于可以控制的单位，增加一个输入框和输入按钮
                    if isinstance(player_handle, ControllablePlayer):
                        new_input_text = gr.Textbox(label=f"{player_handle.zh_name}的新输入", lines=2)
                        self.module_dict[player]["new_input"] = player_history_text
                        exec_btn = gr.Button(value=f"执行{player_handle.zh_name}输入")
                        exec_btn.click(fn=self.chat, inputs=[new_input_text, exec_btn], outputs=[])
            refresh_btn = gr.Button(value="刷新结果")
            refresh_btn.click(fn=self.refresh_data, inputs=[], outputs=self.get_module_list())
        return ui

    def get_module_list(self):
        module_list = []
        for player in self.module_dict:
            module_list.append(self.module_dict[player]["input"])
            module_list.append(self.module_dict[player]["output"])
        return module_list

    def chat(self, input_, player_info):
        player_zh_name = player_info.replace("执行", "").replace("输入", "")
        controllable_player = self.player_zh_name_map[player_zh_name]
        controllable_player.play(input_)
        return [controllable_player.history_input, controllable_player.history_response]

    def refresh_data(self):
        result = []
        for _player, player_handle in self.player_dict.items():
            result.append(player_handle.history_input)
            result.append(player_handle.history_response)
        return result

    def launch(self, share=True):
        self.handle.launch(share=share)
