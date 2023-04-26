## 运行环境和运行方式
运行环境包含在 `env.yaml`文件中；整个程序的入口在`main.py`中， 其中可以使用`game_manager.setAgent(agent:Agent,name:str)`来为玩家指定不同的agent；
其中参数为：<br>
`agent`：传入的`Agent`对象；<br>
`name`：对应角色，可以是`"farmer_1","farmer_2","lord"`<br>
不同Agent对象的初始化方法：<br>
`NaiveAgent(None)  # 随机决策`<br>
`GreedyAgent(None)  # 贪婪决策`<br>
`MiniMaxAgent(player_name:str, depth[optional]:int)  # 搜索决策，需要 playername 指定角色，以及depth指定搜索深度`
