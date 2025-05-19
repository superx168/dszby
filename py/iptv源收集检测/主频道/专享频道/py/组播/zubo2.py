from zubo import multicast_province
config_files = ["py/iptv源收集检测/主频道/专享频道/py/组播/ip/江苏电信_config.txt", 
                "py/iptv源收集检测/主频道/专享频道/py/组播/ip/上海电信_config.txt", 
                "py/iptv源收集检测/主频道/专享频道/py/组播/ip/浙江电信_config.txt", 
                "py/iptv源收集检测/主频道/专享频道/py/组播/ip/江西电信_config.txt", 
                "py/iptv源收集检测/主频道/专享频道/py/组播/ip/安徽电信_config.txt", 
                "py/iptv源收集检测/主频道/专享频道/py/组播/ip/四川电信_config.txt", 
                "py/iptv源收集检测/主频道/专享频道/py/组播/ip/贵州电信_config.txt", 
                "py/iptv源收集检测/主频道/专享频道/py/组播/ip/重庆电信_config.txt", 
                "py/iptv源收集检测/主频道/专享频道/py/组播/ip/陕西电信_config.txt", 
                "py/iptv源收集检测/主频道/专享频道/py/组播/ip/宁夏电信_config.txt"]
for config_file in config_files:
    multicast_province(config_file)
print(f"组播地址获取完成")
