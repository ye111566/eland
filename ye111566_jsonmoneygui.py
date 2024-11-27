from endstone.plugin import Plugin
from endstone.command import Command, CommandSender ,CommandSenderWrapper
from endstone.event import event_handler, PlayerJoinEvent,PlayerCommandEvent
from endstone import ColorFormat
import os
import json
from endstone.actor import Actor
from endstone import Player
import sys
from endstone.form import ModalForm, TextInput,Dropdown,Label,ActionForm
# 获取脚本运行的当前目录
current_dir = os.getcwd()
class Ye111566Jsonmoneygui(Plugin):
    api_version = "0.5"
    def check_version(self):
        return sys.version_info < (3, 10)
    def on_enable(self) -> None:
        if self.check_version():
            self.logger.error(f"python版本过低！请使用python3.10以上版本！")       
    commands = {
        "jsonmoneygui": {
            "description": "json经济系统菜单模式",
            "usages": ["/jsonmoneygui (set|add|reduce|top|query|pay|gui)[name: EnumType]"],
            "permissions": ["ye111566_jsonmoneygui.command.jsonmoneygui"],
            "aliases": ["jmgui","moneygui"]
        }
    }

    permissions = {
        "ye111566_jsonmoneygui.command.jsonmoneygui": {
            "description": "§b§l§ojson经济系统gui模式",
            "default": True,
        }
    }
    """def tag_to_Player(self,tag:str) -> Player:
        for oneplayer in self.server.online_players:
            if oneplayer.remove_scoreboard_tag(tag):
                return oneplayer"""
    def on_command(self, sender: CommandSender, command: Command, args) -> bool:
        if command.name == "jsonmoneygui":
            if not args:
                canshu="gui"
            if args:
                canshu=args[0]
            match canshu:
                case "set":
                    if sender.is_op:
                        self.logger.info(canshu)
                        self.show_set_form(sender)
                    else:
                        sender.send_error_message("你没有权限使用此功能")
                case "add":
                    if sender.is_op:
                        self.logger.info(canshu)
                        self.show_add_form(sender)
                    else:
                        sender.send_error_message("你没有权限使用此功能")
                case "reduce":
                    if sender.is_op:
                        self.logger.info(canshu)
                        self.show_reduce_form(sender)
                    else:
                        sender.send_error_message("你没有权限使用此功能")
                case "top":
                    self.show_top_form(sender)
                case "query":
                    self.show_query_form(sender)
                case "pay":
                    self.logger.info(canshu)
                    self.show_pay_form(sender)
                case "gui":
                    self.logger.info(canshu)
                    self.show_gui(sender)
        return True
    def show_gui(self,player:CommandSender):
        def set_click(sender):
            sender.perform_command("jsonmoneygui set")
        def add_click(sender):
            sender.perform_command("jsonmoneygui add")
        def reduce_click(sender):
            sender.perform_command("jsonmoneygui reduce")
        def pay_click(sender):
            sender.perform_command("jsonmoneygui pay")
        def query_click(sender):
            sender.perform_command("jsonmoneygui query")
        def top_click(sender):
            sender.perform_command("jsonmoneygui top")
        form = ActionForm(
            title="§l§b选择一个操作",
            content="§l§e请选择你想执行的操作"
        )
        form.add_button("§l§e设置金钱(管理员)",on_click=set_click)
        form.add_button("§l§a增加金钱(管理员)",on_click=add_click)
        form.add_button("§l§c减少金钱(管理员)",on_click=reduce_click)
        form.add_button("§l§e转账给在线玩家",on_click=pay_click)
        form.add_button("§l§e查询金钱",on_click=query_click)
        form.add_button("§l§e排行榜",on_click=top_click)
        self.server.get_player(player.name).send_form(form)
    def show_set_form(self, player):
        # 处理提交后的操作
        playerlist=[oneplayer.name for oneplayer in self.server.online_players]
        def handle_set_submit(player, json_str: str):
            data = json.loads(json_str)
            select_player_name = playerlist[int(data[0])]
            if " " in select_player_name:
                select_player_name=f'"{select_player_name}"'
            player.send_message(f"money set {select_player_name} {data[1]}")
            player.perform_command(f"money set {select_player_name} {data[1]}")
        # 显示表单，只有一个下拉框供玩家选择领地
        self.server.get_player(player.name).send_form(
            ModalForm(
                title="设置金钱",
                controls=[
                    Dropdown(label="选择玩家", options=playerlist),
                    TextInput(label="设置的钱数", placeholder="请输入设置的钱数")
                ],
                submit_button="设置",
                on_submit=handle_set_submit
            )
        )
    def show_add_form(self, player):
        # 处理提交后的操作
        playerlist=[oneplayer.name for oneplayer in self.server.online_players]
        def handle_add_submit(player, json_str: str):
            data = json.loads(json_str)
            select_player_name = playerlist[int(data[0])]
            if " " in select_player_name:
                select_player_name=f'"{select_player_name}"'
            player.send_message(f"money add {select_player_name} {data[1]}")
            player.perform_command(f"money add {select_player_name} {data[1]}")
        # 显示表单，只有一个下拉框供玩家选择领地
        self.server.get_player(player.name).send_form(
            ModalForm(
                title="增加金钱",
                controls=[
                    Dropdown(label="选择玩家", options=playerlist),
                    TextInput(label="增加的钱数", placeholder="请输入增加的钱数")
                ],
                submit_button="增加",
                on_submit=handle_add_submit
            )
        )
    def show_reduce_form(self, player):
        # 处理提交后的操作
        playerlist=[oneplayer.name for oneplayer in self.server.online_players]
        def handle_reduce_submit(player, json_str: str):
            data = json.loads(json_str)
            select_player_name = playerlist[int(data[0])]
            if " " in select_player_name:
                select_player_name=f'"{select_player_name}"'
            player.send_message(f"money reduce {select_player_name} {data[1]}")
            player.perform_command(f"money reduce {select_player_name} {data[1]}")
        # 显示表单，只有一个下拉框供玩家选择领地
        self.server.get_player(player.name).send_form(
            ModalForm(
                title="减少金钱",
                controls=[
                    Dropdown(label="选择玩家", options=playerlist),
                    TextInput(label="减少的钱数", placeholder="请输入减少的钱数")
                ],
                submit_button="减少",
                on_submit=handle_reduce_submit
            )
        )
    def show_pay_form(self, player):
        # 处理提交后的操作
        playerlist=[oneplayer.name for oneplayer in self.server.online_players]
        def handle_pay_submit(player, json_str: str):
            data = json.loads(json_str)
            select_player_name = playerlist[int(data[0])]
            if " " in select_player_name:
                select_player_name=f'"{select_player_name}"'
            player.send_message(f"money pay {select_player_name} {data[1]}")
            player.perform_command(f"money pay {select_player_name} {data[1]}")
        # 显示表单，只有一个下拉框供玩家选择领地
        self.server.get_player(player.name).send_form(
            ModalForm(
                title="转账给在线玩家",
                controls=[
                    Dropdown(label="选择在线玩家作为收款方", options=playerlist),
                    TextInput(label="转账的钱数", placeholder="请输入转账的钱数")
                ],
                submit_button="转账",
                on_submit=handle_pay_submit
            )
        )
    def show_top_form(self, player):
        # 处理提交后的操作
        def handle_top_submit(player, json_str: str):
            data = json.loads(json_str)
            player.send_message(f"money top page {data[0]}")
            player.perform_command(f"money top page {data[0]}")
        # 显示表单，只有一个下拉框供玩家选择领地
        self.server.get_player(player.name).send_form(
            ModalForm(
                title="查询指定页码排行榜",
                controls=[
                    TextInput(label="页码", placeholder="请输入页码")
                ],
                submit_button="查询",
                on_submit=handle_top_submit
            )
        )
    def show_query_form(self, player):
        # 处理提交后的操作
        def handle_query_submit(player, json_str: str):
            data = json.loads(json_str)
            player.send_message(f"money query {data[1]}")
            player.perform_command(f"money query {data[1]}")
        # 显示表单，只有一个下拉框供玩家选择领地
        self.server.get_player(player.name).send_form(
            ModalForm(
                title="查询金钱",
                controls=[
                    Label("§l§e@a全部在线人，@s是自己\n也可以输入名字查询指定\n输入为空是查询自己"),
                    TextInput(label="选择器或名字", placeholder="输入选择器或名字")
                ],
                submit_button="查询",
                on_submit=handle_query_submit
            )
        )