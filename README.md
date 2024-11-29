# eland
a realm plugin for minecraft endstone bedrock dedicated server plugin loader

usage:
/land
to open the main menu
/landgui posa
/landgui posb
to set the posa and posb of an area to be landed

5.0.2版本
api已封装
使用方法：

self.server.plugin_manager.get_plugin('ye111566_land').landname_to_Land('主城') 可以把领地名字为主城的领地转为领地Land对象

self.server.plugin_manager.get_plugin('ye111566_land').landname_to_landdata('主城') 可以把领地名字为主城的领地转为此领地的字典

self.server.plugin_manager.get_plugin('ye111566_land').landdata_to_Land('主城') 可以把领地的字典转为领地Land对象

self.server.plugin_manager.get_plugin('ye111566_land').block_to_landname(endstone的Block对象)可以把方块对象转为此方块所在的领地的名字

Land对象有下列方法：

attr: name->str

返回领地的名字

attr: info->dict

返回领地的信息字典

attr: posa->list[int]

返回领地的posa 如[114,51,4]

attr: posb->list[int]

返回领地的posb 如[114,51,4]

attr: tppos->list[int]

返回领地的tppos 如[114,51,4]

attr: dim->str

返回领地的维度名字 有Overworld Nether TheEnd 三种(注意大小写)

attr:dim_index->int

返回领地的维度代码 主世界0 地狱1 末地2

attr:anti_right_click_block->list[str]

返回领地内禁止被右键的方块的id列表 如["minecraft:glow_frame","minecraft:grass_block"]

attr:arcb->list[str] (缩写版，同上)

返回领地内禁止被右键的方块的id列表 如["minecraft:glow_frame","minecraft:grass_block"]

attr:member->list[str]

返回领地的成员列表 如["田所浩二","宫本浩次"]

attr:containter->bool

返回是否开启右键权限

attr:mine->bool

返回是否开启挖掘权限

attr:build->bool

返回是否开启放置权限

attr:tp->bool

返回是否开启公共传送权限

attr:owner->str

返回领地的主人名字 如"HOMO1145141919810"
