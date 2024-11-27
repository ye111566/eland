from endstone.plugin import Plugin
from endstone.command import Command, CommandSender ,CommandSenderWrapper
from endstone.event import event_handler, PlayerJoinEvent,PlayerCommandEvent
from endstone import ColorFormat
import os
import json
from endstone.actor import Actor
from endstone import Player

# 获取脚本运行的当前目录
current_dir = os.getcwd()
"""global selector
selector="""""
class Ye111566Jsonmoneys(Plugin):
    api_version = "0.5"
    def on_enable(self) -> None:
        pass
    """    self.register_events(self)
    @event_handler
    def on_player_command(self, event: PlayerCommandEvent):
        command=event.command
        if "jsonmoneys" in command:
            import re
            # 使用正则表达式提取选择器标签部分
            match = re.search(r'jsonmoneys\s+\S+\s+(.+?)\s+\d+$', command)
            if match:
                global selector
                selector=match.group(1)"""
        

    commands = {
        "jsonmoneys": {
            "description": "json经济系统选择器模式",
            "usages": ["/jsonmoneys (set|add|reduce)[name: EnumType] [tag:str] [int:int]"],
            "permissions": ["ye111566_jsonmoneys.command.jsonmoneys"],
            "aliases": ["jms","moneys"]
        }
    }

    permissions = {
        "ye111566_jsonmoneys.command.jsonmoneys": {
            "description": "§b§l§ojson经济系统选择器模式",
            "default": "op",
        }
    }
    def tag_to_Player(self,tag:str) -> Player:
        for oneplayer in self.server.online_players:
            if oneplayer.remove_scoreboard_tag(tag):
                return oneplayer
    def on_command(self, sender: CommandSender, command: Command, args) -> bool:
        if command.name == "jsonmoneys":
            tag_Player=self.tag_to_Player(args[1])
            """global selector
            self.server.dispatch_command(self.server.command_sender,f"tag {selector} add jsonmoneys_{args[0]}_{args[2]}")
            msg=f"{selector}:jsonmoneys_{args[0]}_{args[2]}，转化后此选择器的名字是"
            selector_Player=self.tag_to_Player(f"jsonmoneys_{args[0]}_{args[2]}")"""
            runcmd=self.server.dispatch_command(self.server.command_sender,f"jsonmoney {args[0]} {tag_Player.name} {args[2]}")
            if " " in tag_Player.name:
                tag_player_name=f'"{tag_Player.name}"'
            else:
                tag_player_name=tag_Player.name
            sender.send_message(f"§l§e执行指令§bjsonmoney {args[0]} {tag_player_name} {args[2]}§e,指令结果§b{runcmd}")
            
            
        return runcmd
    
