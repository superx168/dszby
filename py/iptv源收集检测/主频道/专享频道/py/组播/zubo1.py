from zubo import multicast_province
config_files = ["py/iptv源收集检测/主频道/专享频道/py/组播/ip/广东电信_config.txt", 
                "py/iptv源收集检测/主频道/专享频道/py/组播/ip/广东联通_config.txt", 
                "py/iptv源收集检测/主频道/专享频道/py/组播/ip/广西电信_config.txt", 
                "py/iptv源收集检测/主频道/专享频道/py/组播/ip/湖南电信_config.txt", 
                "py/iptv源收集检测/主频道/专享频道/py/组播/ip/湖北电信_config.txt",
                "py/iptv源收集检测/主频道/专享频道/py/组播/ip/福建电信_config.txt", 
                "py/iptv源收集检测/主频道/专享频道/py/组播/ip/山东电信_config.txt", 
                "py/iptv源收集检测/主频道/专享频道/py/组播/ip/山西联通_config.txt", 
                "py/iptv源收集检测/主频道/专享频道/py/组播/ip/河南电信_config.txt", 
                "py/iptv源收集检测/主频道/专享频道/py/组播/ip/河北联通_config.txt", 
                "py/iptv源收集检测/主频道/专享频道/py/组播/ip/北京联通_config.txt", 
                "py/iptv源收集检测/主频道/专享频道/py/组播/ip/天津联通_config.txt"
               ]
for config_file in config_files:
    multicast_province(config_file)
print(f"组播地址获取完成")
