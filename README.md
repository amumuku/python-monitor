# python-monitor 环境安装及运行
# 1-监控 安装环境
```
pip install -r requirements.txt
```

# 2-后台运行主币监控环境
```
nohup python python-monitor-maintoken-balance.py > monitor-maintoken.log 2>&1 &
```
# 3-后台运行代币监控环境
```
nohup python python-monitor-othertokens-balance.py  > monitor-othertokens.log 2>&1 &
```
