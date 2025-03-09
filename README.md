# eland
a realm plugin for minecraft endstone bedrock dedicated server plugin loader
下载去release


https://github.com/ye111566/eland/releases


usage:
/land
to open the main menu
/landgui posa
/landgui posb
to set the posa and posb of an area to be landed

5.0.2版本
api已封装
使用方法：
self.server.plugin_manager.get_plugin('ye111566_land').pos_to_landname(x,y,z,dimname)可以输入坐标返回属于这个坐标的领地名字
self.server.plugin_manager.get_plugin('ye111566_land').landname_to_Land('主城') 可以把领地名字为主城的领地转为领地Land对象

self.server.plugin_manager.get_plugin('ye111566_land').landname_to_landdata('主城') 可以把领地名字为主城的领地转为此领地的字典

self.server.plugin_manager.get_plugin('ye111566_land').landdata_to_Land('主城') 可以把领地的字典转为领地Land对象

self.server.plugin_manager.get_plugin('ye111566_land').Block_to_landname(endstone的Block对象)可以把方块对象转为此方块所在的领地的名字

self.server.plugin_manager.get_plugin('ye111566_land').Player_to_landname(endstone的Player对象)可以把玩家对象转为此玩家所在的领地的名字
Land对象有下列方法：
attr:father->str
返回领地的父领地
attr：son->list[str]
返回领地的子领地名字列表

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

attr:fire->bool
返回是否允许火焰

attr:explode
返回是否允许爆炸

attr:mobgriefing
返回是否允许生物破坏
meth:get_type()->str
返回领地的类型
有三种:
"father" 表示父领地
"normal" 表示没有子领地的普通领地
"son" 表示子领地
meth:get_owner()->str
比如a是一个Land对象
a.get_owner()得到的就是这个Land对象的主人名字
返回领地的主人名字 
如"HOMO1145141919810"


