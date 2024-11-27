import os
import json
import math
from endstone.plugin import Plugin
from endstone.command import Command, CommandSender
from endstone.form import ModalForm, TextInput,Dropdown
from endstone import Player, ColorFormat


class Ye111566Landgui(Plugin):
    api_version = "0.5"

    def on_enable(self) -> None:
        self.pos_file = os.path.join(os.getcwd(), "plugins", "landgui", "pos.json")
        os.makedirs(os.path.dirname(self.pos_file), exist_ok=True)

        # 初始化文件
        if not os.path.exists(self.pos_file):
            with open(self.pos_file, 'w', encoding='utf-8') as f:
                json.dump({}, f)

        self.logger.info("Ye111566Landgui 插件已启用")

    commands = {
        "landgui": {
            "description": "领地菜单",
            "usages": ["/landgui [msg: message]"],
            "permissions": ["ye111566_landgui.command.landgui"],
            "aliases": ["lingdi"]
        }
    }

    permissions = {
        "ye111566_landgui.command.landgui": {
            "description": "§b§l§o领地菜单",
            "default": True,
        }
    }

    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:
        player = self.server.get_player(sender.name)
        
        if command.name == "landgui":
            if len(args) == 1:
                if args[0] == "posa":
                    self.set_pos(sender, "posa")
                elif args[0] == "posb":
                    self.set_pos(sender, "posb")
                elif args[0] == "member":
                    self.show_member_management_form(sender)
                elif args[0] == "buy":
                    self.show_buy_form(sender)
                elif args[0] == "rename":
                    self.show_rename_form(sender)
                elif args[0] == "del":
                    self.show_del_form(sender)
                elif args[0] == "tp":
                    self.show_tp_form(sender)
                elif args[0] == "tpset":
                    self.show_tpset_form(sender)
                elif args[0] == "manage":
                    self.show_manage_form(sender)
                elif args[0] == "home":
                    self.show_home_form(sender)
                elif args[0] == "transfer":
                    self.show_transfer_form(sender)
                elif args[0] == "arcb":
                    self.show_arcb_form(sender)
                elif args[0] == "":
                    player.perform_command("menu landgui.json")
                else:
                    player.send_message("无效的子命令")
            else:
                player.send_message("请指定 landgui 子命令！")
        return True


    def show_arcb_form(self, sender: CommandSender):
        player = self.server.get_player(sender.name)

        # 读取 land.json 文件
        land_file = os.path.join(os.getcwd(), "plugins", "land", "land.json")
        if not os.path.exists(land_file):
            player.send_message("找不到 land.json 文件")
            return
        
        with open(land_file, 'r', encoding='utf-8') as f:
            land_data = json.load(f)

        # 获取该玩家的领地列表
        player_name = sender.name
        if player_name not in land_data:
            player.send_message(f"玩家 {player_name} 没有领地")
            return

        land_options = [list(land.keys())[0] for land in land_data[player_name]]  # 玩家拥有的领地名称列表

        # 创建 ModalForm 菜单
        form = ModalForm(
            title="编辑右键方块黑名单",
            controls=[
                Dropdown(label="选择领地", options=land_options),      # 下拉选择领地
                Dropdown(label="选择操作", options=["添加", "删除"]),       # 下拉选择操作
                TextInput(label="方块id", placeholder="请输入方块id")  # 输入玩家名字
            ],
            submit_button="提交",
            on_submit=self.handle_arcb_submit
        )
        
        # 显示表单
        player.send_form(form)

    # 处理arcb表单提交
    def handle_arcb_submit(self, player: Player, json_str: str) -> None:
        data = json.loads(json_str)

        land_options = [list(land.keys())[0] for land in self.load_land_data(player.name)]  # 再次获取领地名称
        operation_options = ["add", "del"]

        land_name_index = int(data[0])  # 领地选项的索引
        operation_index = int(data[1])  # 操作选项的索引
        blockname = data[2].strip()  # 方块名字
        if "minecraft:" not in blockname:
            blockname="minecraft:"+blockname
        # 根据索引获取相应的值
        land_name = land_options[land_name_index]
        operation = operation_options[operation_index]

        # 构建并执行命令
        command = f'/land arcb {land_name} {operation} {blockname}'
        player.send_message(f"执行指令：{command}")
        player.perform_command(command)
    def show_transfer_form(self, sender: CommandSender):
        player = self.server.get_player(sender.name)

        # 读取 land.json 文件
        land_file = os.path.join(os.getcwd(), "plugins", "land", "land.json")
        if not os.path.exists(land_file):
            player.send_message("找不到 land.json 文件")
            return
        
        with open(land_file, 'r', encoding='utf-8') as f:
            land_data = json.load(f)

        # 获取该玩家的领地列表
        player_name = sender.name
        if player_name not in land_data:
            player.send_message(f"玩家 {player_name} 没有领地")
            return

        land_options = [list(land.keys())[0] for land in land_data[player_name]]  # 玩家拥有的领地名称列表

        # 创建 ModalForm 菜单
        form = ModalForm(
            title="过户领地",
            controls=[
                Dropdown(label="选择领地", options=land_options),      # 下拉选择领地
                TextInput(label="过户的玩家", placeholder="请输入过户的玩家")   # 输入新名字
            ],
            submit_button="过户",
            on_submit=self.handle_transfer_submit
        )
        
        # 显示表单
        player.send_form(form)

    # 处理过户表单提交
    def handle_transfer_submit(self, player: Player, json_str: str) -> None:
        data = json.loads(json_str)

        land_options = [list(land.keys())[0] for land in self.load_land_data(player.name)]  # 再次获取领地名称

        land_name_index = int(data[0])  # 领地选项的索引
        new_land_owner = data[1].strip()  # 新领地主人
        if " " in new_land_owner:
            new_land_owner=f'"{new_land_owner}"'
        if not new_land_owner:
            player.send_message("过户的对象不能为空！")
            return

        # 根据索引获取原来的领地名称
        land_name = land_options[land_name_index]

        # 构建并执行命令
        command = f'/land transfer {land_name} {new_land_owner}'
        player.send_message(f"执行指令：{command}")
        player.perform_command(command)



    # 显示 home 表单，选择领地后执行传送命令
    def show_home_form(self, player):
        # 获取玩家的领地列表
        player_lands = self.load_land_data(player.name)
        if not player_lands:
            player.send_message("你没有任何领地。")
            return

        # 从玩家的领地数据中提取领地名字
        land_names = [list(land.keys())[0] for land in player_lands]

        # 处理提交后的操作
        def handle_home_submit(player, json_str: str):
            data = json.loads(json_str)
            selected_land_index = int(data[0])  # 获取选中的领地
            land_name = land_names[selected_land_index]  # 从land_names中提取选中的领地名字

            # 执行 /land tp 指令
            tp_command = f"/land tp {land_name}"
            player.send_message(f"执行指令: {tp_command}")
            player.perform_command(tp_command)

        # 显示表单，只有一个下拉框供玩家选择领地
        self.server.get_player(player.name).send_form(
            ModalForm(
                title="传送到领地",
                controls=[
                    Dropdown(label="选择领地", options=land_names)
                ],
                submit_button="传送",
                on_submit=handle_home_submit
            )
        )








    def show_del_form(self, player):
        # 加载玩家领地数据
        player_lands = self.load_land_data(player.name)

        if not player_lands:
            player.send_message("你没有任何领地可以删除")
            return
        
        # 领地名称列表
        land_names = [list(land.keys())[0] for land in player_lands]

        def handle_del_submit(player, json_str: str):
            data = json.loads(json_str)
            selected_land_index = int(data[0])
            selected_land_name = land_names[selected_land_index]

            del_command = f"/land del {selected_land_name}"
            player.send_message(f"执行指令: {del_command}")
            player.perform_command(del_command)

        self.server.get_player(player.name).send_form(
            ModalForm(
                title="删除领地",
                controls=[
                    Dropdown(label="选择领地", options=land_names)
                ],
                submit_button="删除",
                on_submit=handle_del_submit
            )
        )

    def show_tp_form(self, player):
        def handle_tp_submit(player, json_str: str):
            data = json.loads(json_str)
            land_name = str(data[0]).strip()

            if not land_name:
                player.send_message("领地名称不能为空！")
                return

            tp_command = f"/land tp {land_name}"
            player.send_message(f"执行指令: {tp_command}")
            player.perform_command(tp_command)

        self.server.get_player(player.name).send_form(
            ModalForm(
                title="传送到领地",
                controls=[
                    TextInput(label="传送到的领地名称", placeholder="输入领地名称")
                ],
                submit_button="传送",
                on_submit=handle_tp_submit
            )
        )



    # 显示 tpset 表单，使用 pos.json 中的 posa 坐标作为占位符
    def show_tpset_form(self, player):
        # 从 pos.json 加载玩家坐标数据
        pos_data = self.load_pos_data_tpset(player.name)
        
        if not pos_data or len(pos_data) < 1:
            player.send_message("你还没有设置任何传送点。")
            return
        
        posa = pos_data[0]  # 获取 posa 坐标
        # 使用posa的x, y, z作为占位符
        placeholder_x = f"§7{posa['x']}"
        placeholder_y = f"§7{posa['y']}"
        placeholder_z = f"§7{posa['z']}"

        def handle_tpset_submit(player, json_str: str):
            data = json.loads(json_str)
            selected_land_index = int(data[0])  # 获取选中的领地
            x = data[1] if data[1] else posa['x']  # 如果输入为空，则使用占位符中的posa
            y = data[2] if data[2] else posa['y']
            z = data[3] if data[3] else posa['z']

            land_name = land_names[selected_land_index]
            tpset_command = f"/land tpset {land_name} {x} {y} {z}"
            player.send_message(f"执行指令: {tpset_command}")
            player.perform_command(tpset_command)

        # 获取玩家的领地列表
        player_lands = self.load_land_data(player.name)
        land_names = [list(land.keys())[0] for land in player_lands]

        # 显示表单，使用posa的x, y, z作为默认值
        self.server.get_player(player.name).send_form(
            ModalForm(
                title="设置传送点",
                controls=[
                    Dropdown(label="选择领地", options=land_names),
                    TextInput(label="X 坐标", placeholder=placeholder_x),
                    TextInput(label="Y 坐标", placeholder=placeholder_y),
                    TextInput(label="Z 坐标", placeholder=placeholder_z)
                ],
                submit_button="设置传送点",
                on_submit=handle_tpset_submit
            )
        )




    def show_manage_form(self, player):
        # 加载玩家领地数据
        player_lands = self.load_land_data(player.name)

        if not player_lands:
            player.send_message("你没有任何领地可以管理")
            return
        
        # 领地名称列表
        land_names = [list(land.keys())[0] for land in player_lands]
        
        permission_types = ["containter", "build", "mine", "tp"]
        boolean_options = ["true", "false"]

        def handle_manage_submit(player, json_str: str):
            data = json.loads(json_str)
            selected_land_index = int(data[0])
            selected_permission_index = int(data[1])
            selected_value_index = int(data[2])

            selected_land_name = land_names[selected_land_index]
            permission_type = permission_types[selected_permission_index]
            boolean_value = boolean_options[selected_value_index]

            manage_command = f"/land manage {selected_land_name} {permission_type} {boolean_value}"
            player.send_message(f"执行指令: {manage_command}")
            player.perform_command(manage_command)
        
        self.server.get_player(player.name).send_form(
            ModalForm(
                title="管理领地权限",
                controls=[
                    Dropdown(label="选择领地", options=land_names),
                    Dropdown(label="选择权限", options=['领地内右键方块','领地内放置','领地内挖掘','公开领地传送']),
                    Dropdown(label="设置值", options=['开启','关闭'])
                ],
                submit_button="设置",
                on_submit=handle_manage_submit
            )
        )







    # 显示重命名领地表单
    def show_rename_form(self, sender: CommandSender):
        player = self.server.get_player(sender.name)

        # 读取 land.json 文件
        land_file = os.path.join(os.getcwd(), "plugins", "land", "land.json")
        if not os.path.exists(land_file):
            player.send_message("找不到 land.json 文件")
            return
        
        with open(land_file, 'r', encoding='utf-8') as f:
            land_data = json.load(f)

        # 获取该玩家的领地列表
        player_name = sender.name
        if player_name not in land_data:
            player.send_message(f"玩家 {player_name} 没有领地")
            return

        land_options = [list(land.keys())[0] for land in land_data[player_name]]  # 玩家拥有的领地名称列表

        # 创建 ModalForm 菜单
        form = ModalForm(
            title="重命名领地",
            controls=[
                Dropdown(label="选择领地", options=land_options),      # 下拉选择领地
                TextInput(label="新领地名字", placeholder="请输入新名字")   # 输入新名字
            ],
            submit_button="提交",
            on_submit=self.handle_rename_submit
        )
        
        # 显示表单
        player.send_form(form)

    # 处理重命名表单提交
    def handle_rename_submit(self, player: Player, json_str: str) -> None:
        data = json.loads(json_str)

        land_options = [list(land.keys())[0] for land in self.load_land_data(player.name)]  # 再次获取领地名称

        land_name_index = int(data[0])  # 领地选项的索引
        new_land_name = data[1].strip()  # 新领地名字

        if not new_land_name:
            player.send_message("领地新名字不能为空！")
            return

        # 根据索引获取原来的领地名称
        land_name = land_options[land_name_index]

        # 构建并执行命令
        command = f'/land rename {land_name} {new_land_name}'
        player.send_message(f"执行指令：{command}")
        player.perform_command(command)



    # 设置 posa 或 posb 功能
    def set_pos(self, sender: CommandSender, pos_type: str):
        player = self.server.get_player(sender.name)
        pos_data = self.load_pos_data()

        # 获取玩家当前坐标和维度
        location = player.location
        player_name = sender.name

        if player_name not in pos_data:
            pos_data[player_name] = [{"x": None, "y": None, "z": None, "dim": None},  # Posa 数据
                                     {"x": None, "y": None, "z": None}]  # Posb 数据

        # 更新相应的 posa 或 posb 数据
        if pos_type == "posa":
            pos_data[player_name][0] = {
                "x": math.floor(location.x),
                "y": math.floor(location.y),
                "z": math.floor(location.z),
                "dim": location.dimension.name
            }
            player.send_message(f"PosA 已保存为: x={location.x}, y={location.y}, z={location.z}, dim={location.dimension.name}")
        elif pos_type == "posb":
            pos_data[player_name][1] = {
                "x": math.floor(location.x),
                "y": math.floor(location.y),
                "z": math.floor(location.z)
            }
            player.send_message(f"PosB 已保存为: x={location.x}, y={location.y}, z={location.z}")

        # 保存数据
        self.save_pos_data(pos_data)

    # 保存位置数据
    def save_pos_data(self, pos_data):
        with open(self.pos_file, 'w', encoding='utf-8') as f:
            json.dump(pos_data, f, ensure_ascii=False, indent=4)

    # 加载位置数据
    def load_pos_data(self):
        with open(self.pos_file, 'r', encoding='utf-8') as f:
            return json.load(f)


    def load_pos_data_tpset(self, player_name: str):
        pos_file = os.path.join(os.getcwd(), "plugins", "landgui", "pos.json")
        if not os.path.exists(pos_file):
            return None

        with open(pos_file, 'r', encoding='utf-8') as f:
            pos_data = json.load(f)

        return pos_data.get(player_name)


    # 显示购买领地表单
    def show_buy_form(self, sender: CommandSender):
        player = self.server.get_player(sender.name)
        pos_data = self.load_pos_data()
        player_name = player.name

        # 如果该玩家没有保存的 pos 信息，提醒玩家先保存 posa 和 posb
        if player_name not in pos_data or not pos_data[player_name][0]["x"] or not pos_data[player_name][1]["x"]:
            player.send_message("请先设置 PosA 和 PosB 再进行购买！")
            return

        posa = pos_data[player_name][0]
        posb = pos_data[player_name][1]
        def handle_buy_submit(player: Player, json_str: str) -> None:
            data = json.loads(json_str)

            # 获取玩家输入的值，如果没有输入则使用占位符中的默认值
            posa_x = data[0].strip() or posa['x']
            posa_y = data[1].strip() or posa['y']
            posa_z = data[2].strip() or posa['z']
            posb_x = data[3].strip() or posb['x']
            posb_y = data[4].strip() or posb['y']
            posb_z = data[5].strip() or posb['z']

            # 构建并执行指令
            command = f'/land buy {posa_x} {posa_y} {posa_z} {posb_x} {posb_y} {posb_z}'
            player.send_message(f"执行指令：{command}")
            player.perform_command(command)
        # 构建表单
        form = ModalForm(
            title="购买领地",
            controls=[
                TextInput(label="PosA X", placeholder=f"§7{posa['x']}"),
                TextInput(label="PosA Y", placeholder=f"§7{posa['y']}"),
                TextInput(label="PosA Z", placeholder=f"§7{posa['z']}"),
                TextInput(label="PosB X", placeholder=f"§7{posb['x']}"),
                TextInput(label="PosB Y", placeholder=f"§7{posb['y']}"),
                TextInput(label="PosB Z", placeholder=f"§7{posb['z']}")
            ],
            submit_button="提交",
            on_submit=handle_buy_submit
        )

        # 显示表单
        player.send_form(form)

        # 处理购买领地表单提交


    # 显示成员管理表单
    def show_member_management_form(self, sender: CommandSender):
        player = self.server.get_player(sender.name)

        # 读取 land.json 文件
        land_file = os.path.join(os.getcwd(), "plugins", "land", "land.json")
        if not os.path.exists(land_file):
            player.send_message("找不到 land.json 文件")
            return
        
        with open(land_file, 'r', encoding='utf-8') as f:
            land_data = json.load(f)

        # 获取该玩家的领地列表
        player_name = sender.name
        if player_name not in land_data:
            player.send_message(f"玩家 {player_name} 没有领地")
            return

        land_options = [list(land.keys())[0] for land in land_data[player_name]]  # 玩家拥有的领地名称列表

        # 创建 ModalForm 菜单
        form = ModalForm(
            title="管理领地成员",
            controls=[
                Dropdown(label="选择领地", options=land_options),      # 下拉选择领地
                Dropdown(label="操作", options=["add", "del"]),       # 下拉选择操作
                TextInput(label="玩家名字", placeholder="请输入玩家名字")  # 输入玩家名字
            ],
            submit_button="提交",
            on_submit=self.handle_member_submit
        )
        
        # 显示表单
        player.send_form(form)

    # 处理成员表单提交
    def handle_member_submit(self, player: Player, json_str: str) -> None:
        data = json.loads(json_str)

        land_options = [list(land.keys())[0] for land in self.load_land_data(player.name)]  # 再次获取领地名称
        operation_options = ["add", "del"]

        land_name_index = int(data[0])  # 领地选项的索引
        operation_index = int(data[1])  # 操作选项的索引
        playername = data[2].strip()  # 玩家名字

        # 根据索引获取相应的值
        land_name = land_options[land_name_index]
        operation = operation_options[operation_index]

        # 构建并执行命令
        command = f'/land member {land_name} {operation} {playername}'
        player.send_message(f"执行指令：{command}")
        player.perform_command(command)

    def load_land_data(self, player_name: str = None):
        land_file = os.path.join(os.getcwd(), "plugins", "land", "land.json")
        if not os.path.exists(land_file):
            return {}

        with open(land_file, 'r', encoding='utf-8') as f:
            land_data = json.load(f)

        # 如果传入了 player_name，则只返回该玩家的领地，否则返回整个数据
        if player_name:
            return land_data.get(player_name, [])
        return land_data


