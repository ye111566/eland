from endstone.plugin import Plugin
from endstone.command import Command, CommandSender
from endstone.event import event_handler, PlayerJoinEvent
from endstone import ColorFormat
import os
import json

# 获取脚本运行的当前目录
current_dir = os.getcwd()

class Ye111566Jsonmoney(Plugin):
    api_version = "0.5"
    def get_balance(self, player_name: str) -> int:
        money_file = os.path.join(os.getcwd(), "plugins", "money", "money.json")
        
        if not os.path.exists(money_file):
            return None  # 如果文件不存在，返回 None 表示无余额信息

        with open(money_file, 'r', encoding='utf-8') as f:
            money_data = json.load(f)
        
        return money_data.get(player_name, None)  # 从字典中获取玩家的余额

    def on_enable(self) -> None:
        # 设置 money.json 文件路径
        self.money_file = os.path.join(current_dir, "plugins", "money","money.json")
        self.register_events(self)
        # 检查 money.json 文件是否存在，如果不存在则创建一个空的 JSON 文件
        if not os.path.exists(self.money_file):
            os.makedirs(os.path.join(current_dir, "plugins"), exist_ok=True)
            with open(self.money_file, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=4)

        self.logger.info(f"{ColorFormat.YELLOW}JsonMoney 插件已启用！配置文件位于: {self.money_file}")
    @event_handler
    def on_player_join(self, event: PlayerJoinEvent):
        event.player.send_message(f"§l§b您的当前钱包余额:§e{self.get_balance(event.player.name)}")
    commands = {
        "jsonmoney": {
            "description": "json经济系统",
            "usages": ["/jsonmoney (set|add|reduce|pay|query|top)[name: EnumType] [player_or_page:player] [int:int]"],
            "permissions": ["ye111566_jsonmoney.command.jsonmoney"],
            "aliases": ["jm","money"]
        }
    }

    permissions = {
        "ye111566_jsonmoney.command.jsonmoney": {
            "description": "§b§l§ojson经济系统",
            "default": True,
        }
    }

    def load_money_data(self):
        # 加载 money.json 文件
        if os.path.exists(self.money_file):
            with open(self.money_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def save_money_data(self, data):
        # 保存 money.json 文件
        with open(self.money_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:
        if command.name == "jsonmoney":
            money_data = self.load_money_data()
            player_name = sender.name
            action = args[0]
            if action == "query":
                if len(args)==1:
                    player=self.server.get_player(sender.name)
                    player.send_message(f"§l§b您的当前钱包余额:{self.get_balance(player.name)}")
                if len(args)==2 and args[1]=="@a":
                    sender.send_message(f"§l§e当前所有玩家的经济数据如下:")
                    for oneplayer in self.server.online_players:
                        sender.send_message(f"§l§e{oneplayer.name}§l§b:§l§a{self.get_balance(oneplayer.name)}")
                if len(args)==2 and args[1]=="@s":
                    player=self.server.get_player(sender.name)
                    player.send_message(f"§l§b您的当前钱包余额:{self.get_balance(player.name)}")
                if len(args)==2 and args[1]!="@a" and args[1]!="@s":
                    sender.send_message(f"{args[1]}的金钱数量为{self.get_balance(args[1])}")
            if action !="query" and int(args[2])>=0:
                if action == "add" and len(args) == 3 and sender.is_op ==False:
                    sender.send_error_message("你无权使用此指令")
                if action == "reduce" and len(args) == 3 and sender.is_op ==False:
                    sender.send_error_message("你无权使用此指令")
                if action == "set" and len(args) == 3 and sender.is_op ==False:
                    sender.send_error_message("你无权使用此指令")
                if action == "add" and len(args) == 3 and sender.is_op ==True:
                    # 添加金额
                    target_player = args[1]
                    amount = int(args[2])

                    if target_player not in money_data:
                        money_data[target_player] = 0

                    money_data[target_player] += amount
                    self.save_money_data(money_data)
                    sender.send_message(f"{ColorFormat.GREEN}成功给 {target_player} 增加了 {amount} 单位货币！")
                    self.server.get_player(target_player).send_message(f"§l§b经济变动: 你§a获得§b了 §e{amount} §b单位货币！剩余金钱:§e{self.get_balance(target_player)}")
                    
                if action == "reduce" and len(args) == 3 and sender.is_op ==True:
                    # 扣除金额，首先检查金额是否足够
                    target_player = args[1]
                    amount = int(args[2])

                    if target_player not in money_data or money_data[target_player] < amount:
                        self.server.get_player(target_player).send_error_message("余额不足")
                        sender.send_message(f"{ColorFormat.RED}{target_player} 的余额不足，无法扣除 {amount} 单位货币！剩余金钱:{self.get_balance(target_player)}")
                        self.server.get_player(target_player).send_message(f"§l§c你的余额不足，无法被扣除 §e{amount}§c 单位货币！§b剩余金钱:§e{self.get_balance(target_player)}")
                        return False
                    else:
                        money_data[target_player] -= amount
                        self.save_money_data(money_data)
                        self.server.get_player(target_player).send_message(f"§l§b经济变动: 你被§c扣除§b了 §e{amount}§b 单位货币！剩余金钱:§e{self.get_balance(target_player)}")#########
                        sender.send_message(f"{ColorFormat.GREEN}成功从 {target_player} 扣除了 {amount} 单位货币！")
                        
                if action == "pay" and len(args) == 3:
                    # 支付金额
                    receiver = args[1]
                    amount = int(args[2])

                    if player_name not in money_data or money_data[player_name] < amount:
                        sender.send_message(f"§l§c你的余额不足，无法转账 §e{amount}§c 单位货币给 §e{receiver}§c！§b剩余金钱:§e{self.get_balance(sender.name)}")
                        return False

                    if receiver not in money_data:
                        money_data[receiver] = 0

                    # 扣除付款者的金额，增加接收者的金额
                    money_data[player_name] -= amount
                    self.save_money_data(money_data)
                    sender.send_message(f"§l§b你§a成功§b支付了 §e{amount}§b 单位货币给 §e{receiver}§b！剩余金钱:§e{self.get_balance(sender.name)}")
                    money_data[receiver] += amount
                    self.save_money_data(money_data)
                    self.server.get_player(receiver).send_message(f"§l§e{sender.name}§a转账§b了§e {amount}§b 单位货币给§a你§b！剩余金钱:§e{self.get_balance(receiver)}")
                if action == "set" and len(args) == 3 and sender.is_op ==True:
                    # 设置某个玩家的金额
                    target_player = args[1]
                    amount = int(args[2])

                    # 如果玩家不存在于 money_data，直接设置
                    money_data[target_player] = amount
                    self.save_money_data(money_data)

                    sender.send_message(f"{ColorFormat.GREEN}成功将 {target_player} 的余额设置为 {amount} 单位货币！")
                    self.server.get_player(target_player).send_message(f"经济变动，你的金钱被设置为{amount}")
                if args[0]== "top" and args[1] == "page":
                    #sender.send_message("开始计算")
                    # 获取页码并确保为整数
                    page = int(args[2])
                    #sender.send_message(str(page))
                    if page <= 0:
                        sender.send_message(f"{ColorFormat.RED}页码必须为正整数！")
                        
                    
                    # 每页显示10条数据
                    per_page = 10

                    # 读取 money.json 文件
                    money_data = self.load_money_data()
                    #sender.send_message("开始排序")
                    # 对玩家按照余额从高到低排序，返回 (玩家名字, 余额) 元组列表
                    sorted_money = sorted(money_data.items(), key=lambda x: x[1], reverse=True)
                    #sender.send_message("完成排序")
                    # 计算总页数
                    total_pages = (len(sorted_money) + per_page - 1) // per_page
                    #sender.send_message(f"总页数为{total_pages}")
                    # 如果页码超过总页数，返回错误信息
                    if page > total_pages:
                        sender.send_message(f"{ColorFormat.RED}超过最大页数！最大页数为 {total_pages}。")
                        

                    # 计算开始和结束索引
                    start_index = (page - 1) * per_page
                    end_index = min(start_index + per_page, len(sorted_money))
                    #sender.send_message(f"{start_index},{end_index}")
                    # 发送页码信息
                    sender.send_message(f"{ColorFormat.YELLOW}排行榜 - 第 {page} 页 / 共 {total_pages} 页")

                    # 输出玩家排名、名字和余额
                    for i, (player_name, balance) in enumerate(sorted_money[start_index:end_index], start=start_index + 1):
                        sender.send_message(f"{ColorFormat.GREEN}#{i}: {player_name} - {balance} 单位货币")
            if action !="query" and int(args[2])<0:
                sender.send_error_message("无效的数值！")
        return True
