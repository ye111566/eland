from endstone.plugin import Plugin
from endstone.command import Command, CommandSender
from endstone import ColorFormat
from endstone.form import ActionForm
from endstone.command import CommandSenderWrapper
import os
import json
from endstone.event import event_handler, PlayerInteractEvent
# 获取脚本运行的当前目录
current_dir = os.getcwd()

# 指定menu文件夹的路径
menu_dir = os.path.join(current_dir, "plugins", "menu")
#player_name=sender.name
class Ye111566Menu(Plugin):
    api_version = "0.5"
    global player_namea
    global opencount
    player_namea=""
    opencount=0
    def on_enable(self) -> None:
        self.server.scheduler.run_task(self, self.send_time, delay=0, period=2)

        # 确保menu文件夹存在
        os.makedirs(menu_dir, exist_ok=True)
        self.register_events(self)
        # 检查menu.json是否存在，若不存在则创建默认的menu.json
        menu_file_path = os.path.join(menu_dir, "menu.json")
        if not os.path.exists(menu_file_path):
            default_menu_data = {
                "按钮显示文本1": {
                    "text": "点按钮后回复的消息文本1",
                    "cmd": "msg @s hi",
                    "mode": "player"
                },
                "按钮显示文本2": {
                    "text": "点按钮后回复的消息文本2",
                    "cmd": "title @a title hi",
                    "mode": "server"
                },
                "按钮显示文本3": {
                    "text": "点按钮后回复的消息文本3",
                    "cmd": "title @a title hi $sender.name$",
                    "mode": "server"
                },
                "打开menu.json": {
                    "text": "打开成功",
                    "cmd": "menu menu.json",
                    "mode": "player"
                }
            }
            with open(menu_file_path, 'w', encoding='utf-8') as f:
                json.dump(default_menu_data, f, ensure_ascii=False, indent=4)
            self.logger.info(f"已创建默认的 menu.json 文件于: {menu_file_path}")

        self.logger.info(f"{ColorFormat.YELLOW}菜单目录: {menu_dir}")
        self.logger.warning("来自endstone0.5.3的bug!!!!!!!!!!!!!!!!!")
        self.logger.warning("如果在mode为player执行的命令是打开其他菜单")
        self.logger.warning("如果没用并且报错，请打开其源代码")
        self.logger.warning("把sender.send_form改成self.server.get_player(sender.name).send_form(form)")
    @event_handler
    def PlayerInteractEvent(self, event: PlayerInteractEvent):
        global opencount
        global player_namea
        player_namea=event.player.name
        #self.server.logger.info(event.player.name)
        player_name=event.player.name
        if " " in player_name:
            player_name=f'"{player_name}"'
        if self.server.dispatch_command(CommandSenderWrapper(self.server.command_sender), "title @a[name="+player_name+",hasitem=[{item=compass,location=slot.weapon.mainhand}]] actionbar a)"):
            opencount=3
    def send_time(self) -> None:
        global opencount
        global player_namea
        opencount=opencount-1
        if opencount==1:
            self.server.get_player(player_namea).perform_command("menu")
    commands = {
        "menu": {
            "description": "菜单",
            "usages": ["/menu [msg: message]"],
            "permissions": ["my_plugin.command.menu"],
            "aliases": ["cd", "caidan"]
        }
    }

    permissions = {
        "my_plugin.command.menu": {
            "description": "§b§l§o菜单",
            "default": True,
        }
    }

    def load_menu(self, menu_file: str):
        # 拼接menu.json路径
        menu_file_path = os.path.join(menu_dir, menu_file)
        
        # 检查文件是否存在
        if not os.path.exists(menu_file_path):
            return None

        # 读取menu.json
        with open(menu_file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:
        if command.name == "menu":
            # 如果用户提供了一个菜单文件名，则加载它，否则加载默认的menu.json
            if len(args) == 0 or args[0] == "":
                menu_file = "menu.json"
            else:
                menu_file = args[0]

            menu = self.load_menu(menu_file)

            if menu is None:
                sender.send_message(f"找不到菜单文件: {menu_file}")
                return True

            # 创建表单
            form = ActionForm(
                title="§l§b选择一个操作",
                content="§l§o§5请选择你想执行的操作"
            )

            # 动态添加按钮并设置回调
            for button_text, button_data in menu.items():
                def create_callback(button_text=button_text, command=button_data["cmd"], mode=button_data["mode"]):
                    def on_click(sender):
                        # 每次执行指令前重新读取menu.json
                        with open(os.path.join(menu_dir, menu_file), 'r', encoding='utf-8') as f:
                            updated_menu = json.load(f)

                        # 检查sender.name是否包含空格，如果有，则添加双引号
                        sender_name = sender.name
                        if ' ' in sender_name:
                            sender_name = f'"{sender_name}"'

                        # 替换$sender.name$为实际的玩家名称（可能带双引号）
                        cmd = updated_menu[button_text]["cmd"].replace("$sender.name$", sender_name)

                        # 执行当前点击的按钮对应的指令
                        sender.send_message(updated_menu[button_text]["text"])
                        if updated_menu[button_text]["mode"] == "player":
                            sender.perform_command(cmd)
                        elif updated_menu[button_text]["mode"] == "server":
                            

                            self.server.dispatch_command(CommandSenderWrapper(self.server.command_sender), cmd)
                    return on_click
                if button_data.get("icon") is not None:
                    form.add_button(button_text,icon=button_data["icon"],on_click=create_callback(button_text, button_data["cmd"], button_data["mode"]))
                if button_data.get("icon") is None:
                    form.add_button(button_text,on_click=create_callback(button_text, button_data["cmd"], button_data["mode"]))
            self.server.get_player(sender.name).send_form(form)
            # 发送表单
        return True
