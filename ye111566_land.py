from endstone.plugin import Plugin
from endstone.command import Command, CommandSender ,CommandSenderWrapper
from endstone import ColorFormat 
from endstone.form import ActionForm
import os
import json
import uuid
import math
from datetime import datetime
from endstone.event import event_handler, BlockBreakEvent, BlockPlaceEvent, PlayerInteractEvent
from endstone.form import ActionForm, ModalForm, Dropdown, TextInput
from endstone import ColorFormat

def transfer_land(land_file_path, user_from, user_to, land_name):
    """
    将 land_name 从 user_from 转移给 user_to。
    
    参数:
    land_file_path: 领地数据的文件路径
    user_from: 转出用户
    user_to: 转入用户
    land_name: 要转移的领地名称
    """
    # 读取 JSON 文件
    with open(land_file_path, 'r', encoding='utf-8') as f:
        land_data = json.load(f)
    
    # 检查源用户是否拥有该领地
    if user_from not in land_data:
        print(f"用户 {user_from} 不存在.")
        return
    
    # 查找源用户是否有该领地
    user_from_land = None
    for land_info in land_data[user_from]:
        if land_name in land_info:
            user_from_land = land_info[land_name]
            break
    
    if not user_from_land:
        print(f"用户 {user_from} 没有 {land_name} 领地.")
        return
    
    # 如果目标用户没有，则初始化目标用户数据
    if user_to not in land_data:
        land_data[user_to] = []
    
    # 将领地数据添加到目标用户
    land_data[user_to].append({land_name: user_from_land})
    
    # 从源用户删除该领地
    land_data[user_from] = [land for land in land_data[user_from] if land_name not in land]
    
    # 保存更新后的数据回 JSON 文件
    with open(land_file_path, 'w', encoding='utf-8') as f:
        json.dump(land_data, f, ensure_ascii=False, indent=4)
    
    print(f"领地 {land_name} 已成功从 {user_from} 转移给 {user_to}.")


# 定义检测长方体是否重合的函数
def no_intersection_between_cuboids(a, b, c, d, e, f, g, h, i, j, k, l):
    if max(a, d) < min(g, j) or max(g, j) < min(a, d):
        return True
    if max(b, e) < min(h, k) or max(h, k) < min(b, e):
        return True
    if max(c, f) < min(i, l) or max(i, l) < min(c, f):
        return True
    return False
class Land:
    def __init__(self, land:dict):
        self.name=list(land.keys())[0]
        land_info=list(land.values())[0]
        self.info=list(land.values())[0]
        self.posa=list(map(int, list(land.values())[0]["posa"].split(', ')))
        self.posb=list(map(int, list(land.values())[0]["posa"].split(', ')))
        self.dim=list(land.values())[0]["dim"]
        if list(land.values())[0]["dim"]=="Overworld":
            self.dim_index=0
        if list(land.values())[0]["dim"]=="Nether":
            self.dim_index=1
        if list(land.values())[0]["dim"]=="TheEnd":
            self.dim_index=2
        self.anti_right_click_block=land_info["anti_right_click_block"]
        self.arcb=land_info["anti_right_click_block"]
        self.member=land_info["member"]
        self.tppos=[land_info["tpposx"],land_info["tpposy"],land_info["tpposz"]]
        
        containterget=list(land.values())[0]["permission"][0]["containter"]
        containter_bool=containterget.lower()=="true"
        self.containter=containter_bool
        
        buildget=list(land.values())[0]["permission"][1]["build"]
        build_bool=buildget.lower()=="true"
        self.build=build_bool
        
        mineget=list(land.values())[0]["permission"][2]["mine"]
        mine_bool=mineget.lower()=="true"
        self.mine=mine_bool
        
        tpget=list(land.values())[0]["permission"][3]["tp"]
        tp_bool=tpget.lower()=="true"
        self.tp=tp_bool
        land_json_path = os.path.join(os.getcwd(), "plugins", "land", "land.json")
        self.fire=land_info["fire"]
        self.mobgriefing=land_info["mobgriefing"]
        self.explode=land_info["explode"]
        # 检查 land.json 文件是否存在
        if not os.path.exists(land_json_path):
            print("领地文件不存在，无法检查领地权限！")
            return
        # 读取 land.json 文件
        with open(land_json_path, 'r', encoding='utf-8') as f:
            land_data = json.load(f)
        for owner, lands in land_data.items():
            for oneland in lands:
                if land==oneland:
                    self.owner=owner
class Ye111566Land(Plugin):
    api_version = "0.5"
    from endstone.block import Block
    def landdata_to_Land(self,land:dict):
        return Land(land)
    
    def Block_to_landname(self, block:Block):
        land_json_path = os.path.join(os.getcwd(), "plugins", "land", "land.json")
        # 检查 land.json 文件是否存在
        if not os.path.exists(land_json_path):
            print("领地文件不存在，无法检查领地权限！")
            return
        # 读取 land.json 文件
        with open(land_json_path, 'r', encoding='utf-8') as f:
            land_data = json.load(f)
        block_x = math.floor(block.location.x)
        block_y = math.floor(block.location.y)
        block_z = math.floor(block.location.z)
        block_dimension = block.location.dimension.name
        for owner, lands in land_data.items():
            for land in lands:
                for land_name, land_info in land.items():
                    posa = list(map(int, land_info["posa"].split(', ')))
                    posb = list(map(int, land_info["posb"].split(', ')))
                    dim = land_info["dim"]
                    if dim == block_dimension:
                        if (min(posa[0], posb[0]) <= block_x <= max(posa[0], posb[0]) and
                            min(posa[1], posb[1]) <= block_y <= max(posa[1], posb[1]) and
                            min(posa[2], posb[2]) <= block_z <= max(posa[2], posb[2])):
                                return land_name
                    else:
                        return None
                    
    from endstone import Player
    def Player_to_landname(self,player:Player) -> None:
        land_json_path = os.path.join(os.getcwd(), "plugins", "land", "land.json")
        if not os.path.exists(land_json_path):
            self.logger.info("领地文件不存在，无法检查领地信息！")
            return
        with open(land_json_path, 'r', encoding='utf-8') as f:
            land_data = json.load(f)
        oneplayer = player
        player_x = math.floor(oneplayer.location.x)
        player_y = math.floor(oneplayer.location.y)
        player_z = math.floor(oneplayer.location.z)
        player_dim = oneplayer.location.dimension.name
        for owner, lands in land_data.items():
            for land in lands:
                for land_name, land_info in land.items():
                    posa = list(map(int, land_info["posa"].split(', ')))
                    posb = list(map(int, land_info["posb"].split(', ')))
                    land_dim = land_info["dim"]
                    #print(f"{player_dim},{player_x},{player_y},{player_z},{land_name},{str(posa)},{str(posb)},{land_dim}")
                    if player_dim == land_dim:
                        if (min(posa[0], posb[0]) <= player_x <= max(posa[0], posb[0]) and
                            min(posa[1], posb[1]) <= player_y <= max(posa[1], posb[1]) and
                            min(posa[2], posb[2]) <= player_z <= max(posa[2], posb[2])):
                            return land_name

    def landname_to_landdata(self, name:str):
        land_json_path = os.path.join(os.getcwd(), "plugins", "land", "land.json")
        # 检查 land.json 文件是否存在
        if not os.path.exists(land_json_path):
            print("领地文件不存在，无法检查领地权限！")
            return
        # 读取 land.json 文件
        with open(land_json_path, 'r', encoding='utf-8') as f:
            land_data = json.load(f)
        for owner, lands in land_data.items():
            for land in lands:
                for land_name, land_info in land.items():
                    if name==land_name:
                        return land
    def landname_to_Land(self,name:str):
        landdata=self.landname_to_landdata(name)
        return self.landdata_to_Land(landdata)
##umaru写这里!
    def fire(self):
        land_json_path = os.path.join(os.getcwd(), "plugins", "land", "land.json")
        # 检查 land.json 文件是否存在
        if not os.path.exists(land_json_path):
            print("领地文件不存在，无法检查领地权限！")
            return
        # 读取 land.json 文件
        with open(land_json_path, 'r', encoding='utf-8') as f:
            land_data = json.load(f)
            for owner, lands in land_data.items():
                for land in lands:
                    for land_name, land_info in land.items():
                        self.landname_to_Land(land_name).fire#fire权限开关
##umaru写这里!
    def explode(self):
        land_json_path = os.path.join(os.getcwd(), "plugins", "land", "land.json")
        # 检查 land.json 文件是否存在
        if not os.path.exists(land_json_path):
            print("领地文件不存在，无法检查领地权限！")
            return
        # 读取 land.json 文件
        with open(land_json_path, 'r', encoding='utf-8') as f:
            land_data = json.load(f)
            for owner, lands in land_data.items():
                for land in lands:
                    for land_name, land_info in land.items():
                        self.landname_to_Land(land_name).explode#explode权限开关
                        
##umaru写这里!
    def mobgriefing(self):
        land_json_path = os.path.join(os.getcwd(), "plugins", "land", "land.json")
        # 检查 land.json 文件是否存在
        if not os.path.exists(land_json_path):
            print("领地文件不存在，无法检查领地权限！")
            return
        # 读取 land.json 文件
        with open(land_json_path, 'r', encoding='utf-8') as f:
            land_data = json.load(f)
            for owner, lands in land_data.items():
                for land in lands:
                    for land_name, land_info in land.items():
                        self.landname_to_Land(land_name).mobgriefing#mobgriefing权限开关
    # 事件监听器：玩家交互事件
    @event_handler
    def PlayerInteractEvent(self, event: PlayerInteractEvent):
        land_json_path = os.path.join(os.getcwd(), "plugins", "land", "land.json")
        
        # 检查 land.json 文件是否存在
        if not os.path.exists(land_json_path):
            event.player.send_message("领地文件不存在，无法检查领地权限！")
            return

        # 读取 land.json 文件
        with open(land_json_path, 'r', encoding='utf-8') as f:
            land_data = json.load(f)

        player_name = event.player.name
        block_x = math.floor(event.block.location.x)
        block_y = math.floor(event.block.location.y)
        block_z = math.floor(event.block.location.z)
        block_dimension = event.block.location.dimension.name
        #self.server.logger.info(f"block_xyz:{block_x} {block_y} {block_z} ,dim:{block_dimension}")

        # 遍历所有领地
        for owner, lands in land_data.items():
            for land in lands:
                for land_name, land_info in land.items():
                    posa = list(map(int, land_info["posa"].split(', ')))
                    posb = list(map(int, land_info["posb"].split(', ')))
                    dim = land_info["dim"]
                    #self.server.logger.info(f"{land_name}的信息:{posa[0]} {posa[1]} {posa[2]}到{posb[0]} {posb[1]} {posb[2]},维度{dim}")
                    
                    # 只检查与当前方块同维度的领地
                    if dim == block_dimension:
                        # 确定方块是否在该领地范围内
                        if (min(posa[0], posb[0]) <= block_x <= max(posa[0], posb[0]) and
                            min(posa[1], posb[1]) <= block_y <= max(posa[1], posb[1]) and
                            min(posa[2], posb[2]) <= block_z <= max(posa[2], posb[2])):
                            if land_info["permission"][0]["containter"] == "false" and player_name != owner and player_name not in land_info["member"]:
                                event.player.send_message(f"你不能在玩家 {owner} 的领地中进行任何右键")
                                event.cancelled = True
                                return
                            elif land_info["permission"][0]["containter"] == "true" and len(land_info.get("anti_right_click_block")) !=0 and player_name != owner and player_name not in land_info["member"]:
                                if event.block.type in land_info["anti_right_click_block"]:
                                    event.player.send_message(f"你不能在玩家 {owner} 的领地中右键操作{event.block.type}")
                                    event.cancelled = True
                                return


    # 事件监听器：方块放置事件
    @event_handler
    def BlockPlaceEvent(self, event: BlockPlaceEvent):
        land_json_path = os.path.join(os.getcwd(), "plugins", "land", "land.json")
        
        # 检查 land.json 文件是否存在
        if not os.path.exists(land_json_path):
            event.player.send_message("领地文件不存在，无法检查领地权限！")
            return

        # 读取 land.json 文件
        with open(land_json_path, 'r', encoding='utf-8') as f:
            land_data = json.load(f)

        player_name = event.player.name
        block_x = math.floor(event.block.location.x)
        block_y = math.floor(event.block.location.y)
        block_z = math.floor(event.block.location.z)
        block_dimension = event.block.location.dimension.name
        #self.server.logger.info(f"block_xyz:{block_x} {block_y} {block_z} ,dim:{block_dimension}")

        # 遍历所有领地
        for owner, lands in land_data.items():
            for land in lands:
                for land_name, land_info in land.items():
                    posa = list(map(int, land_info["posa"].split(', ')))
                    posb = list(map(int, land_info["posb"].split(', ')))
                    dim = land_info["dim"]
                    #self.server.logger.info(f"{land_name}的信息:{posa[0]} {posa[1]} {posa[2]}到{posb[0]} {posb[1]} {posb[2]},维度{dim}")
                    
                    # 只检查与当前方块同维度的领地
                    if dim == block_dimension:
                        # 确定方块是否在该领地范围内
                        if (min(posa[0], posb[0]) <= block_x <= max(posa[0], posb[0]) and
                            min(posa[1], posb[1]) <= block_y <= max(posa[1], posb[1]) and
                            min(posa[2], posb[2]) <= block_z <= max(posa[2], posb[2])):
                            
                            # 检查权限：如果 build 权限为 false 且玩家不是领主或成员
                            if land_info["permission"][1]["build"] == "false" and player_name != owner and player_name not in land_info["member"]:
                                event.player.send_message(f"你不能在玩家 {owner} 的领地中放置方块！")
                                event.cancelled = True
                                return    


    # 事件监听器：方块破坏事件
    @event_handler
    def BlockBreakEvent(self, event: BlockBreakEvent):
        land_json_path = os.path.join(os.getcwd(), "plugins", "land", "land.json")
        
        # 检查 land.json 文件是否存在
        if not os.path.exists(land_json_path):
            event.player.send_message("领地文件不存在，无法检查领地权限！")
            return

        # 读取 land.json 文件
        with open(land_json_path, 'r', encoding='utf-8') as f:
            land_data = json.load(f)

        player_name = event.player.name
        block_x = math.floor(event.block.location.x)
        block_y = math.floor(event.block.location.y)
        block_z = math.floor(event.block.location.z)
        block_dimension = event.block.location.dimension.name
        #self.server.logger.info(f"block_xyz:{block_x} {block_y} {block_z} ,dim:{block_dimension}")

        # 遍历所有领地
        for owner, lands in land_data.items():
            for land in lands:
                for land_name, land_info in land.items():
                    posa = list(map(int, land_info["posa"].split(', ')))
                    posb = list(map(int, land_info["posb"].split(', ')))
                    dim = land_info["dim"]
                    #self.server.logger.info(f"{land_name}的信息:{posa[0]} {posa[1]} {posa[2]}到{posb[0]} {posb[1]} {posb[2]},维度{dim}")
                    
                    # 只检查与当前方块同维度的领地
                    if dim == block_dimension:
                        # 确定方块是否在该领地范围内
                        if (min(posa[0], posb[0]) <= block_x <= max(posa[0], posb[0]) and
                            min(posa[1], posb[1]) <= block_y <= max(posa[1], posb[1]) and
                            min(posa[2], posb[2]) <= block_z <= max(posa[2], posb[2])):
                            
                            # 检查权限：如果 mine 权限为 false 且玩家不是领主或成员
                            if land_info["permission"][2]["mine"] == "false" and player_name != owner and player_name not in land_info["member"]:
                                event.player.send_message(f"你不能破坏玩家 {owner} 的领地中的方块！")
                                event.cancelled = True
                                return


    def on_enable(self) -> None:
        import os
        import json
        self.register_events(self)
        current_dir = os.getcwd()
        self.land_dir = os.path.join(current_dir, "plugins", "land")
        self.money_dir = os.path.join(current_dir, "plugins", "money")
        self.land_file = os.path.join(self.land_dir, "land.json")
        self.config_file = os.path.join(self.land_dir, "config.json")
        self.money_file = os.path.join(self.money_dir, "money.json")

        # 如果 land.json 不存在，创建空的文件
        if not os.path.exists(self.land_file):
            os.makedirs(self.land_dir, exist_ok=True)
            with open(self.land_file, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=4)
        
        # 如果 config.json 不存在，创建默认配置
        if not os.path.exists(self.config_file):
            with open(self.config_file, 'w', encoding='utf-8') as f:
                # 默认值为 {"price": 1, "money": "json"}
                json.dump({"price": 1, "money": "json"}, f, ensure_ascii=False, indent=4)
        
        # 读取配置文件
        with open(self.config_file, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        
        # 读取地块单价和 money 类型（json 或 economyapi）
        self.price_per_block = config_data.get("price", 1)
        self.money_type = config_data.get("money", "json")  # 默认为 json

        # 日志信息
        self.logger.info(f"{ColorFormat.YELLOW}领地插件已启用！配置文件位于: {self.land_file}")
        self.logger.info(f"{ColorFormat.YELLOW}领地价格配置文件位于: {self.config_file}")
        self.logger.info(f"{ColorFormat.YELLOW}玩家金钱文件位于: {self.money_file}")

        # 周期性任务
        self.server.scheduler.run_task(self, self.landinfo, delay=0, period=20)
        import os
        import json

        # 获取领地文件的路径
        land_file_path = os.path.join(os.getcwd(), "plugins", "land", "land.json")

        # 读取 JSON 文件
        with open(land_file_path, 'r', encoding='utf-8') as f:
            land_data = json.load(f)

        # 遍历所有用户的领地数据，并确保每个领地都包含 "anti_right_click_block"
        for user_data in land_data.values():
            for land_info in user_data:
                for land_name, details in land_info.items():
                    # 如果没有 anti_right_click_block 键，设置为一个空列表
                    details.setdefault("anti_right_click_block", [])
                    details.setdefault("fire", False)
                    details.setdefault("explode", False)
                    details.setdefault("mobgriefing", False)
        # 将修改后的数据写回到 JSON 文件
        with open(land_file_path, 'w', encoding='utf-8') as f:
            json.dump(land_data, f, ensure_ascii=False, indent=4)

        print("领地数据已更新，'anti_right_click_block' fire explode mobgriefing 已初始化。")



    def landinfo(self) -> None:
        land_json_path = os.path.join(os.getcwd(), "plugins", "land", "land.json")

        # 检查 land.json 文件是否存在
        if not os.path.exists(land_json_path):
            self.logger.info("领地文件不存在，无法检查领地信息！")
            return

        with open(land_json_path, 'r', encoding='utf-8') as f:
            land_data = json.load(f)

        # 遍历所有在线玩家
        for oneplayer in self.server.online_players:
            player_x = math.floor(oneplayer.location.x)
            player_y = math.floor(oneplayer.location.y)
            player_z = math.floor(oneplayer.location.z)
            player_dim = oneplayer.location.dimension.name

            # 默认提示信息（表示未在领地中）
            found_land = False

            for owner, lands in land_data.items():
                for land in lands:
                    for land_name, land_info in land.items():
                        posa = list(map(int, land_info["posa"].split(', ')))
                        posb = list(map(int, land_info["posb"].split(', ')))
                        land_dim = land_info["dim"]

                        if player_dim == land_dim:
                            # 判断玩家是否在领地范围内
                            if (min(posa[0], posb[0]) <= player_x <= max(posa[0], posb[0]) and
                                min(posa[1], posb[1]) <= player_y <= max(posa[1], posb[1]) and
                                min(posa[2], posb[2]) <= player_z <= max(posa[2], posb[2])):
                                
                                # 设置找到领地的标志
                                found_land = True

                                player_name = oneplayer.name
                                message = f'§l§b你现在在§1§e{owner}§b的领地§e{land_name}§b上'.replace(" ","")
                                self.server.get_player(player_name).send_tip(message)
                                #cmdreturn = self.server.dispatch_command(CommandSenderWrapper(self.server.command_sender), 
                                #                                        f'title {player_name} actionbar {message}')
                                #if not cmdreturn:
                                #    self.server.dispatch_command(CommandSenderWrapper(self.server.command_sender), 
                                #                                f'title {player_name} actionbar §l§b你现在在一个领地上')
                                break  # 找到领地后不再遍历，继续下一个玩家
                    if found_land:
                        break
                if found_land:
                    break


    commands = {
        "land": {
            "description": "领地",
            "usages": ["/land [msg: message] [msg: message] [msg: message] [msg: message] [msg: message] [msg: message] [msg: message]"],
            "permissions": ["my_plugin.command.land"],
            "aliases": ["lingdi"]
        }
    }

    permissions = {
        "my_plugin.command.land": {
            "description": "§b§l§o领地",
            "default": True,
        }
    }


    def get_all_land_names(self):
        if os.path.exists(self.land_file):
            with open(self.land_file, 'r', encoding='utf-8') as f:
                land_data = json.load(f)

            all_land_names = []

            # 遍历所有玩家的领地
            for player, lands in land_data.items():
                for land in lands:
                    # 提取领地的名字，假设每个领地都是字典，键为领地名称
                    land_name = list(land.keys())[0]
                    all_land_names.append(land_name)

            return all_land_names
        else:
            print("找不到 land.json 文件")
            return []

    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:
        if command.name == "land":
            if args[0]=="transfer":
                if len(args)==3:
                    land_file_path = os.path.join(os.getcwd(), "plugins", "land", "land.json")
                    transfer_land(land_file_path, sender.name, args[2], args[1])
                    sender.send_message(f"执行{args[1]}过户给{args[2]}")
                else:
                    sender.send_error_message("用法: /land transfer <land_name> <to_player>")
            # 1. 成员管理
            if args[0] == "member":
                if len(args) >= 3:
                    land_name = args[1]
                    operation = args[2].lower()
                    target_player = args[3].replace('"', '')  # 去掉引号

                    if os.path.exists(self.land_file):
                        with open(self.land_file, 'r', encoding='utf-8') as f:
                            land_data = json.load(f)

                        player_name = sender.name

                        if player_name in land_data:
                            for land in land_data[player_name]:
                                if land_name in land:
                                    if operation == "add":
                                        if target_player not in land[land_name]["member"]:
                                            land[land_name]["member"].append(target_player)
                                            sender.send_message(f"成功将 {target_player} 添加为领地 {land_name} 的成员")
                                    elif operation == "del":
                                        if target_player in land[land_name]["member"]:
                                            land[land_name]["member"].remove(target_player)
                                            sender.send_message(f"成功将 {target_player} 从领地 {land_name} 的成员中移除")
                                    else:
                                        sender.send_message("无效的操作，使用 add 或 del")
                                    with open(self.land_file, 'w', encoding='utf-8') as f:
                                        json.dump(land_data, f, ensure_ascii=False, indent=4)
                                    return True
                            sender.send_message(f"没有找到名为 {land_name} 的领地或你没有权限")
                        else:
                            sender.send_message("你没有任何领地")
                    else:
                        sender.send_message("找不到 land.json 文件")
                elif len(args) == 3 and args[2] == "list":
                    # 列出领地的所有成员
                    land_name = args[1]
                    if os.path.exists(self.land_file):
                        with open(self.land_file, 'r', encoding='utf-8') as f:
                            land_data = json.load(f)

                        for owner, lands in land_data.items():
                            for land in lands:
                                if land_name in land:
                                    members = land[land_name]["member"]
                                    sender.send_message(f"领地 {land_name} 的成员列表: {', '.join(members)}")
                                    return True
                        sender.send_message(f"没有找到名为 {land_name} 的领地")
                    else:
                        sender.send_message("找不到 land.json 文件")
                else:
                    sender.send_message("用法: /land member name add|del playername")
            # 1.5. block管理
            if args[0] == "anti_right_click_block" or args[0] == "arcb":
                if len(args) >= 3:
                    land_name = args[1]
                    operation = args[2].lower()
                    target_player = args[3].replace('"', '')  # 去掉引号

                    if os.path.exists(self.land_file):
                        with open(self.land_file, 'r', encoding='utf-8') as f:
                            land_data = json.load(f)

                        player_name = sender.name

                        if player_name in land_data:
                            for land in land_data[player_name]:
                                if land_name in land:
                                    if operation == "add":
                                        if target_player not in land[land_name]["anti_right_click_block"]:
                                            land[land_name]["anti_right_click_block"].append(target_player)
                                            sender.send_message(f"成功将 {target_player} 添加为领地 {land_name} 的anti_right_click_block")
                                    elif operation == "del":
                                        if target_player in land[land_name]["anti_right_click_block"]:
                                            land[land_name]["anti_right_click_block"].remove(target_player)
                                            sender.send_message(f"成功将 {target_player} 从领地 {land_name} 的anti_right_click_block中移除")
                                    else:
                                        sender.send_message("无效的操作，使用 add 或 del")
                                    with open(self.land_file, 'w', encoding='utf-8') as f:
                                        json.dump(land_data, f, ensure_ascii=False, indent=4)
                                    return True
                            sender.send_message(f"没有找到名为 {land_name} 的领地或你没有权限")
                        else:
                            sender.send_message("你没有任何领地")
                    else:
                        sender.send_message("找不到 land.json 文件")
                elif len(args) == 3 and args[2] == "list":
                    # 列出领地的所有成员
                    land_name = args[1]
                    if os.path.exists(self.land_file):
                        with open(self.land_file, 'r', encoding='utf-8') as f:
                            land_data = json.load(f)

                        for owner, lands in land_data.items():
                            for land in lands:
                                if land_name in land:
                                    members = land[land_name]["anti_right_click_block"]
                                    sender.send_message(f"领地 {land_name} 的anti_right_click_block列表: {', '.join(members)}")
                                    return True
                        sender.send_message(f"没有找到名为 {land_name} 的领地")
                    else:
                        sender.send_message("找不到 land.json 文件")
                else:
                    sender.send_message("用法: /land anti_right_click_block name add|del playername")


            # 2. 领地购买
            elif args[0] == "buy":
                if len(args) >= 7:
                    try:
                        buy_posa_x = int(args[1])
                        buy_posa_y = int(args[2])
                        buy_posa_z = int(args[3])
                        buy_posb_x = int(args[4])
                        buy_posb_y = int(args[5])
                        buy_posb_z = int(args[6])

                        dx = abs(buy_posa_x - buy_posb_x) + 1
                        dy = abs(buy_posa_y - buy_posb_y) + 1
                        dz = abs(buy_posa_z - buy_posb_z) + 1

                        total_blocks = dx * dy * dz

                        if os.path.exists(self.config_file):
                            with open(self.config_file, 'r', encoding='utf-8') as f:
                                config_data = json.load(f)
                            price_per_block = config_data.get("price", 1)
                            money_type = config_data.get("money", "json")  # 获取 money 类型，默认为 json
                        else:
                            sender.send_message("找不到 config.json 文件，使用默认单价 1")
                            price_per_block = 1
                            money_type = "json"  # 默认值为 json

                        total_price = total_blocks * price_per_block

                        player_name = sender.name
                        
                        if money_type == "json":
                            if os.path.exists(self.money_file):
                                with open(self.money_file, 'r', encoding='utf-8') as f:
                                    money_data = json.load(f)

                                player_money = money_data.get(player_name, 0)

                                if player_money < total_price:
                                    if " " in player_name:
                                        player_name=f'"{player_name}"'
                                    sender.send_message(f"余额不足！你需要 {total_price} 单位货币，但只有 {player_money} 单位货币")
                                    return True

                                if os.path.exists(self.land_file):
                                    with open(self.land_file, 'r', encoding='utf-8') as f:
                                        land_data = json.load(f)

                                    for owner, lands in land_data.items():
                                        for land in lands:
                                            for land_name, land_info in land.items():
                                                posa_str = land_info.get("posa")
                                                posb_str = land_info.get("posb")
                                                posa_x, posa_y, posa_z = map(int, posa_str.split(", "))
                                                posb_x, posb_y, posb_z = map(int, posb_str.split(", "))

                                                if not no_intersection_between_cuboids(buy_posa_x, buy_posa_y, buy_posa_z,
                                                                                    buy_posb_x, buy_posb_y, buy_posb_z,
                                                                                    posa_x, posa_y, posa_z,
                                                                                    posb_x, posb_y, posb_z):
                                                    if land_info.get("dim") == self.server.get_player(sender.name).location.dimension.name:
                                                        sender.send_message(f"购买失败，领地与玩家 {owner} 的领地 {land_name} 重叠！")
                                                        return True

                                money_data[player_name] = player_money - total_price
                                with open(self.money_file, 'w', encoding='utf-8') as f:
                                    json.dump(money_data, f, ensure_ascii=False, indent=4)

                        elif money_type == "economyapi":
                            if not self.server.dispatch_command(CommandSenderWrapper(self.server.command_sender), f'economy reduce {player_name} {total_price}'):
                                sender.send_message(f"余额不足！你需要 {total_price} 单位货币")
                                return True

                        if os.path.exists(self.land_file):
                            with open(self.land_file, 'r', encoding='utf-8') as f:
                                land_data = json.load(f)

                            for owner, lands in land_data.items():
                                for land in lands:
                                    for land_name, land_info in land.items():
                                        posa_str = land_info.get("posa")
                                        posb_str = land_info.get("posb")
                                        posa_x, posa_y, posa_z = map(int, posa_str.split(", "))
                                        posb_x, posb_y, posb_z = map(int, posb_str.split(", "))
                                        
                                        if not no_intersection_between_cuboids(buy_posa_x, buy_posa_y, buy_posa_z,
                                                                            buy_posb_x, buy_posb_y, buy_posb_z,
                                                                            posa_x, posa_y, posa_z,
                                                                            posb_x, posb_y, posb_z):
                                            if land_info.get("dim") == self.server.get_player(sender.name).location.dimension.name:
                                                sender.send_message(f"购买失败，领地与玩家 {owner} 的领地 {land_name} 重叠！")
                                                return True

                        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
                        land_name = current_time

                        new_land = {
                            land_name: {
                                "posa": f"{buy_posa_x}, {buy_posa_y}, {buy_posa_z}",
                                "posb": f"{buy_posb_x}, {buy_posb_y}, {buy_posb_z}",
                                "dim": f"{self.server.get_player(sender.name).location.dimension.name}",
                                "member": [],
                                "tpposx": f"{buy_posa_x}",
                                "tpposy": f"{buy_posa_y}",
                                "tpposz": f"{buy_posa_z}",
                                "anti_right_click_block":[],
                                "permission": [
                                    {"containter": "false"},
                                    {"build": "false"},
                                    {"mine": "false"},
                                    {"tp": "false"},
                                ]
                            }
                        }

                        if player_name in land_data:
                            land_data[player_name].append(new_land)
                        else:
                            land_data[player_name] = [new_land]

                        with open(self.land_file, 'w', encoding='utf-8') as f:
                            json.dump(land_data, f, ensure_ascii=False, indent=4)

                        sender.send_message(f"购买领地成功！领地价格为: {total_price} 单位货币")

                    except ValueError:
                        sender.send_message("坐标必须为整数！")
                else:
                    sender.send_message("用法: /land buy posa_x posa_y posa_z posb_x posb_y posb_z")

            # 3. 重命名领地
            elif args[0] == "rename":
                if len(args) >= 3:
                    old_name = args[1]
                    new_name = args[2]
                    if new_name in self.get_all_land_names():
                        sender.send_error_message("此新名字已经存在")
                    if new_name not in self.get_all_land_names():
                        if os.path.exists(self.land_file):
                            with open(self.land_file, 'r', encoding='utf-8') as f:
                                land_data = json.load(f)

                            player_name = sender.name

                            if player_name in land_data:
                                for land in land_data[player_name]:
                                    if old_name in land:
                                        land[new_name] = land.pop(old_name)
                                        sender.send_message(f"领地已重命名为 {new_name}")
                                        
                                        with open(self.land_file, 'w', encoding='utf-8') as f:
                                            json.dump(land_data, f, ensure_ascii=False, indent=4)
                                        return True
                            sender.send_message(f"没有找到名为 {old_name} 的领地或你没有权限")
                        else:
                            sender.send_message("找不到 land.json 文件")
                else:
                    sender.send_message("用法: /land rename old_name new_name")









            
            # 4. 删除领地
            elif args[0] == "del":
                if len(args) >= 2:
                    del_name = args[1]

                    if os.path.exists(self.land_file) and os.path.exists(self.config_file):
                        with open(self.land_file, 'r', encoding='utf-8') as f:
                            land_data = json.load(f)

                        if os.path.exists(self.config_file):
                            with open(self.config_file, 'r', encoding='utf-8') as f:
                                config_data = json.load(f)
                            price_per_block = config_data.get("price", 1)
                            money_type = config_data.get("money", "json")  # 获取 money 类型，默认为 json
                        else:
                            sender.send_message("找不到 config.json 文件，使用默认单价 1")
                            price_per_block = 1
                            money_type = "json"

                        player_name = sender.name

                        if player_name in land_data:
                            for land in land_data[player_name]:
                                if del_name in land:
                                    posa = list(map(int, land[del_name]["posa"].split(", ")))
                                    posb = list(map(int, land[del_name]["posb"].split(", ")))
                                    dx = abs(posa[0] - posb[0]) + 1
                                    dy = abs(posa[1] - posb[1]) + 1
                                    dz = abs(posa[2] - posb[2]) + 1
                                    total_blocks = dx * dy * dz

                                    refund_amount = total_blocks * price_per_block

                                    if money_type == "json":
                                        # 使用 JSON 文件进行退款操作
                                        if os.path.exists(self.money_file):
                                            with open(self.money_file, 'r', encoding='utf-8') as f:
                                                money_data = json.load(f)

                                            player_money = money_data.get(player_name, 0)
                                            money_data[player_name] = player_money + refund_amount

                                            with open(self.money_file, 'w', encoding='utf-8') as f:
                                                json.dump(money_data, f, ensure_ascii=False, indent=4)
                                        else:
                                            sender.send_message("找不到 money.json 文件")
                                            return True

                                    elif money_type == "economyapi":
                                        if " " in player_name:
                                            player_name=f'"{player_name}"'
                                        # 使用 economyapi 进行退款操作
                                        if not self.server.dispatch_command(CommandSenderWrapper(self.server.command_sender), f'economy add {player_name} {refund_amount}'):
                                            sender.send_message("退款失败，请联系管理员")
                                            return True

                                    # 移除领地
                                    land_data[player_name].remove(land)
                                    if not land_data[player_name]:
                                        del land_data[player_name]

                                    with open(self.land_file, 'w', encoding='utf-8') as f:
                                        json.dump(land_data, f, ensure_ascii=False, indent=4)

                                    sender.send_message(f"成功删除领地 {del_name}，已退款 {refund_amount} 单位货币")
                                    return True

                        sender.send_message(f"没有找到名为 {del_name} 的领地或你没有权限删除")
                    else:
                        sender.send_message("找不到 land.json 文件")
                else:
                    sender.send_message("用法: /land del land_name")















            # 5. 查看领地信息
            elif args[0] == "info":
                if os.path.exists(self.land_file):
                    with open(self.land_file, 'r', encoding='utf-8') as f:
                        land_data = json.load(f)

                    player_name = sender.name

                    if player_name in land_data:
                        sender.send_message(f"玩家 {player_name} 的所有领地信息:")
                        for land in land_data[player_name]:
                            for land_name, land_info in land.items():
                                sender.send_message(f"领地名: {land_name}")
                                sender.send_message(f"坐标范围: {land_info['posa']} 到 {land_info['posb']}")
                                sender.send_message(f"维度: {land_info['dim']}")
                                sender.send_message(f"权限: {land_info['permission']}")
                                sender.send_message(f"成员: {land_info['member']}")
                                sender.send_message(f"禁止右键的方块: {land_info['anti_right_click_block']}")
                    else:
                        sender.send_message(f"玩家 {player_name} 没有领地。")
                else:
                    sender.send_message("找不到 land.json 文件")
            # 6. 传送到领地
            elif args[0] == "tp":
                if len(args) >= 2:
                    land_name = args[1]

                    if os.path.exists(self.land_file):
                        with open(self.land_file, 'r', encoding='utf-8') as f:
                            land_data = json.load(f)

                        player_name = sender.name

                        for owner, lands in land_data.items():
                            for land in lands:
                                if land_name in land:
                                    land_info = land[land_name]

                                    # 获取传送坐标
                                    tpposx = int(land_info.get("tpposx", land_info["posa"].split(", ")[0]))
                                    tpposy = int(land_info.get("tpposy", land_info["posa"].split(", ")[1]))
                                    tpposz = int(land_info.get("tpposz", land_info["posa"].split(", ")[2]))
                                    dim=land_info["dim"]
                                    match dim:
                                        case "TheEnd":
                                            dim="the_end"

                                    if owner == player_name:
                                        sender_name = f'"{player_name}"' if ' ' in player_name else player_name
                                        self.server.dispatch_command(CommandSenderWrapper(self.server.command_sender), f"execute in {dim} run tp {sender_name} {tpposx} {tpposy} {tpposz}")
                                        sender.send_message(f"已传送至领地 {land_name}")
                                        return True

                                    if land_info["permission"][3]["tp"] == "true":
                                        sender_name = f'"{player_name}"' if ' ' in player_name else player_name
                                        self.server.dispatch_command(CommandSenderWrapper(self.server.command_sender), f"execute in {dim} run tp {sender_name} {tpposx} {tpposy} {tpposz}")
                                        sender.send_message(f"已传送至领地 {land_name}")
                                        return True
                                    else:
                                        sender.send_message(f"你没有权限传送到该领地 {land_name}")
                                        return True

                        sender.send_message(f"没有找到名为 {land_name} 的领地")
                    else:
                        sender.send_message("找不到 land.json 文件")
                else:
                    sender.send_message("用法: /land tp land_name")

            # 7. 设置领地传送点
            elif args[0] == "tpset":
                if len(args) >= 5:
                    land_name = args[1]
                    tpposx = int(args[2])
                    tpposy = int(args[3])
                    tpposz = int(args[4])

                    if os.path.exists(self.land_file):
                        with open(self.land_file, 'r', encoding='utf-8') as f:
                            land_data = json.load(f)

                        player_name = sender.name

                        if player_name in land_data:
                            for land in land_data[player_name]:
                                if land_name in land:
                                    # 只能领地主人设置传送点
                                    land_info = land[land_name]
                                    land_info["tpposx"] = tpposx
                                    land_info["tpposy"] = tpposy
                                    land_info["tpposz"] = tpposz

                                    with open(self.land_file, 'w', encoding='utf-8') as f:
                                        json.dump(land_data, f, ensure_ascii=False, indent=4)

                                    sender.send_message(f"成功设置领地 {land_name} 的传送点为 ({tpposx}, {tpposy}, {tpposz})")
                                    return True

                            sender.send_message(f"没有找到名为 {land_name} 的领地或你没有权限")
                        else:
                            sender.send_message("你没有任何领地")
                    else:
                        sender.send_message("找不到 land.json 文件")
                else:
                    sender.send_message("用法: /land tpset land_name tpposx tpposy tpposz")
            # 8. 管理领地权限
            elif args[0] == "manage":
                if len(args) >= 4:
                    land_name = args[1]
                    permission_type = args[2].lower()  # 例如 containter, build, mine, tp
                    permission_value = args[3].lower()  # true or false

                    # 检查权限类型是否合法
                    valid_permissions = ["containter", "build", "mine", "tp"]
                    if permission_type not in valid_permissions:
                        if permission_type in["fire","mobgriefing","explode"]:
                            if os.path.exists(self.land_file):
                                with open(self.land_file, 'r', encoding='utf-8') as f:
                                    land_data = json.load(f)

                                player_name = sender.name

                                if player_name in land_data:
                                    for land in land_data[player_name]:
                                        if land_name in land:
                                            # 只能领地主人设置传送点
                                            land_info = land[land_name]
                                            if permission_value =="true":
                                                permission_value_bool=True
                                            if permission_value =="false":
                                                permission_value_bool=False
                                            land_info[permission_type] = permission_value_bool

                                            with open(self.land_file, 'w', encoding='utf-8') as f:
                                                json.dump(land_data, f, ensure_ascii=False, indent=4)

                                            sender.send_message(f"成功")
                                            return True

                                    sender.send_message(f"没有找到名为 {land_name} 的领地或你没有权限")
                                else:
                                    sender.send_message("你没有任何领地")
                            else:
                                sender.send_message("找不到 land.json 文件")

                            

                    if permission_value not in ["true", "false"]:
                        sender.send_message("权限值必须为 'true' 或 'false'")
                        return True

                    # 打开并检查 land.json 文件
                    if os.path.exists(self.land_file):
                        with open(self.land_file, 'r', encoding='utf-8') as f:
                            land_data = json.load(f)

                        player_name = sender.name

                        # 只能领地主人修改权限
                        if player_name in land_data:
                            for land in land_data[player_name]:
                                if land_name in land:
                                    land_info = land[land_name]
                                    
                                    # 根据权限类型修改对应的权限值
                                    permission_index = valid_permissions.index(permission_type)
                                    land_info["permission"][permission_index][permission_type] = permission_value
                                    
                                    # 更新 land.json 文件
                                    with open(self.land_file, 'w', encoding='utf-8') as f:
                                        json.dump(land_data, f, ensure_ascii=False, indent=4)

                                    sender.send_message(f"成功将领地 {land_name} 的权限 {permission_type} 设置为 {permission_value}")
                                    return True

                            sender.send_message(f"没有找到名为 {land_name} 的领地或你没有权限")
                        else:
                            sender.send_message("你没有任何领地")
                    else:
                        sender.send_message("找不到 land.json 文件")
                else:
                    sender.send_message("用法: /land manage land_name containter|build|mine|tp true|false")            
            elif args[0] == "help":
                sender.send_message("/land member <land_name> add|del <playername(有空格玩家名加引号)> - 添加或删除领地成员")##
                sender.send_message("/land buy <posa_x> <posa_y> <posa_z> <posb_x> <posb_y> <posb_z> - 购买领地")#
                sender.send_message("/land rename <old_name> <new_name> - 重命名领地")##
                sender.send_message("/land del <land_name> - 删除领地并退款")##
                sender.send_message("/land info - 查看自己的领地信息")#
                sender.send_message("/land tp <land_name> - 传送到指定领地（可以传送到开启tp权限的其他领地哦）")#
                sender.send_message("/land tpset <land_name> <tpposx> <tpposy> <tpposz> - 设置领地传送点(默认为创建时候的posa)")##
                sender.send_message("/land manage <land_name> containter|build|mine|tp true|false - 管理领地权限")##
                sender.send_message("/land help - 查看此帮助信息")#
                sender.send_message("/land anti_right_click_block <land_name> add|del <minecraft:blockid>")#
            elif args[0] == "gui" or args[0] == "":
                player = self.server.get_player(sender.name)
                player.perform_command("landgui")
            else:
                sender.send_message("/land help-查看领地帮助信息")
        return True
