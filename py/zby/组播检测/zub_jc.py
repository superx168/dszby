import os
import re
import time
import requests
import threading
from queue import Queue
from threading import Thread
from datetime import datetime
from datetime import timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from opencc import OpenCC
###
# 定义txt文件的URL列表
urls = [
       'https://ghproxy.cc/https://raw.githubusercontent.com/mlzlzj/iptv/refs/heads/main/iptv_list.txt',  #假m3u
       'https://ghproxy.cc/https://raw.githubusercontent.com/gaotianliuyun/gao/master/list.txt',   #暂时保留
        #'https://ghproxy.cc/https://raw.githubusercontent.com/ddhola/file/d7afb504b1ba4fef31813e1166cb892215a9c063/0609test',#港澳台、国外为主
       #'https://ghproxy.cc/https://raw.githubusercontent.com/frxz751113/IPTVzb1/main/%E7%BB%BC%E5%90%88%E6%BA%90.txt',
       # #'https://raw.githubusercontent.com/ssili126/tv/main/itvlist.txt',
       # 'https://ghproxy.cc/https://raw.githubusercontent.com/Supprise0901/TVBox_live/main/live.txt',
       # 'https://ghproxy.cc/https://raw.githubusercontent.com/gaotianliuyun/gao/master/list.txt',
       # 'https://gitlab.com/p2v5/wangtv/-/raw/main/lunbo.txt',
       # 'https://ghproxy.cc/https://raw.githubusercontent.com/vbskycn/iptv/master/tv/iptv4.txt',
       # 'https://ghproxy.cc/https://raw.githubusercontent.com/junge3333/juds6/main/yszb1.txt',
       #'https://ghproxy.cc/https://raw.githubusercontent.com/kimwang1978/collect-tv-txt/main/others_output.txt'
      ''

]
# 合并文件的函数
def merge_txt_files(urls, output_filename='py/zby/组播检测/汇总.txt'):
    try:
        with open(output_filename, 'w', encoding='utf-8') as outfile:
            for url in urls:
                try:
                    response = requests.get(url)
                    response.raise_for_status()  # 确保请求成功
                    # 尝试将响应内容解码为UTF-8，如果失败则尝试其他编码
                    try:
                        content = response.content.decode('utf-8')
                    except UnicodeDecodeError:
                        content = response.content.decode('gbk')  # 尝试GBK编码
                    outfile.write(content + '\n')
                except requests.RequestException as e:
                    print(f'Error downloading {url}: {e}')
    except IOError as e:
        print(f'Error writing to file: {e}')

# 调用函数
merge_txt_files(urls)

#简体转繁体
# 创建一个OpenCC对象,指定转换的规则为繁体字转简体字
converter = OpenCC('t2s.json')#繁转简
#converter = OpenCC('s2t.json')#简转繁
# 打开txt文件
with open('py/zby/组播检测/汇总.txt', 'r', encoding='utf-8') as file:
    traditional_text = file.read()
# 进行繁体字转简体字的转换
simplified_text = converter.convert(traditional_text)
# 将转换后的简体字写入txt文件
with open('py/zby/组播检测/汇总.txt', 'w', encoding='utf-8') as file:
    file.write(simplified_text)

with open('py/zby/组播检测/汇总.txt', 'r', encoding="utf-8") as file:
    # 读取所有行并存储到列表中
    lines = file.readlines()
#定义替换规则的字典对频道名替换
replacements = {
    	"CCTV-1高清测试": "",
    	"CCTV-2高清测试": "",
    	"CCTV-7高清测试": "",
    	"CCTV-10高清测试": "",
    	"中央": "CCTV",
    	"高清""": "",
    	"HD": "",
    	"标清": "",
    	"amc": "AMC",
    	"CCTV1综合": "CCTV1",
    	"CCTV2财经": "CCTV2",
    	"CCTV3综艺": "CCTV3",
    	"国际": "",
    	"5体育": "5",
    	"6电影": "6",
    	"军农": "",
    	"8影视": "8",
    	"9纪录": "9",
    	"0科教": "0",
    	"2社会与法": "2",
    	"3新闻": "3",
    	"4少儿": "4",
    	"5音乐": "5",
    	"咪咕": "",
    	"超清": "",
    	"频道": "",
    	"CCTV-": "CCTV",
    	"CCTV_": "CCTV",
    	"CCTV风云剧场": "风云剧场",
    	"CCTV第一剧场": "第一剧场",
    	"CCTV怀旧剧场": "怀旧剧场",
    	"熊猫影院": "熊猫电影",
    	"熊猫爱生活": "熊猫生活",
    	"爱宠宠物": "宠物生活",
    	"[ipv6]": "",
    	"专区": "",
    	"卫视超": "卫视",
    	"CCTV风云剧场": "风云剧场",
    	"CCTV第一剧场": "第一剧场",
    	"CCTV怀旧剧场": "怀旧剧场",
    	"IPTV": "",
    	"PLUS": "+",
    	"＋": "+",
    	"(": "",
    	")": "",
    	"CAV": "",
    	"美洲": "",
    	"北美": "",
    	"12M": "",
    	"高清测试CCTV-1": "",
    	"高清测试CCTV-2": "",
    	"高清测试CCTV-7": "",
    	"高清测试CCTV-10": "",
    	"LD": "",
    	"HEVC20M": "",
    	"S,": ",",
    	"测试": "",
    	"CCTW": "CCTV",
    	"试看": "",
    	"测试": "",
    	" ": "",
    	"测试cctv": "CCTV",
    	"CCTV1综合": "CCTV1",
    	"CCTV2财经": "CCTV2",
    	"CCTV3综艺": "CCTV3",
    	"CCTV4国际": "CCTV4",
    	"CCTV4中文国际": "CCTV4",
    	"CCTV4欧洲": "CCTV4",
    	"CCTV5体育": "CCTV5",
    	"CCTV5+体育": "CCTV5+",
    	"CCTV6电影": "CCTV6",
    	"CCTV7军事": "CCTV7",
    	"CCTV7军农": "CCTV7",
    	"CCTV7农业": "CCTV7",
    	"CCTV7国防军事": "CCTV7",
    	"CCTV8电视剧": "CCTV8",
    	"CCTV8影视": "CCTV8",
    	"CCTV8纪录": "CCTV9",
    	"CCTV9记录": "CCTV9",
    	"CCTV9纪录": "CCTV9",
    	"CCTV10科教": "CCTV10",
    	"CCTV11戏曲": "CCTV11",
    	"CCTV12社会与法": "CCTV12",
    	"CCTV13新闻": "CCTV13",
    	"CCTV新闻": "CCTV13",
    	"CCTV14少儿": "CCTV14",
    	"央视14少儿": "CCTV14",
    	"CCTV少儿超": "CCTV14",
    	"CCTV15音乐": "CCTV15",
    	"CCTV音乐": "CCTV15",
    	"CCTV16奥林匹克": "CCTV16",
    	"CCTV17农业农村": "CCTV17",
    	"CCTV17军农": "CCTV17",
    	"CCTV17农业": "CCTV17",
    	"CCTV5+体育赛视": "CCTV5+",
    	"CCTV5+赛视": "CCTV5+",
    	"CCTV5+体育赛事": "CCTV5+",
    	"CCTV5+赛事": "CCTV5+",
    	"CCTV5+体育": "CCTV5+",
    	"CCTV5赛事": "CCTV5+",
    	"凤凰中文台": "凤凰中文",
    	"凤凰资讯台": "凤凰资讯",
    	"(CCTV4K测试）": "CCTV4K",
    	"上海东方卫视": "上海卫视",
    	"东方卫视": "上海卫视",
    	"内蒙卫视": "内蒙古卫视",
    	"福建东南卫视": "东南卫视",
    	"广东南方卫视": "南方卫视",
    	"湖南金鹰卡通": "金鹰卡通",
    	"炫动卡通": "哈哈炫动",
    	"卡酷卡通": "卡酷少儿",
    	"卡酷动画": "卡酷少儿",
    	"BRTVKAKU少儿": "卡酷少儿",
    	"优曼卡通": "优漫卡通",
    	"优曼卡通": "优漫卡通",
    	"嘉佳卡通": "佳嘉卡通",
    	"世界地理": "地理世界",
    	"CCTV世界地理": "地理世界",
    	"BTV北京卫视": "北京卫视",
    	"BTV冬奥纪实": "冬奥纪实",
    	"东奥纪实": "冬奥纪实",
    	"卫视台": "卫视",
    	"湖南电视台": "湖南卫视",
    	"少儿科教": "少儿",
    	"影视剧": "影视",
    	"电视剧": "影视",
    	"CCTV1CCTV1": "CCTV1",
    	"CCTV2CCTV2": "CCTV2",
    	"CCTV7CCTV7": "CCTV7",
    	"CCTV10CCTV10": "CCTV10"
}
with open('py/zby/组播检测/汇总.txt', 'w', encoding='utf-8') as new_file:
    for line in lines:
        # 去除行尾的换行符
        line = line.rstrip('\n')
        # 分割行，获取逗号前的字符串
        parts = line.split(',', 1)
        if len(parts) > 0:
            # 替换逗号前的字符串
            before_comma = parts[0]
            for old, new in replacements.items():
                before_comma = before_comma.replace(old, new)
            # 将替换后的逗号前部分和逗号后部分重新组合成一行，并写入新文件
            new_line = f'{before_comma},{parts[1]}\n' if len(parts) > 1 else f'{before_comma}\n'
            new_file.write(new_line)


# 打开文本文件进行读取
def read_and_process_file(input_filename, output_filename, encodings=['utf-8', 'gbk']):
    for encoding in encodings:
        try:
            with open(input_filename, 'r', encoding=encoding) as file:
                lines = file.readlines()
                break
        except UnicodeDecodeError:
            continue
    else:
        raise ValueError(f"Cannot decode file '{input_filename}' with any of the provided encodings")

    with open(output_filename, 'w', encoding='utf-8') as outfile:
        for line in lines:
            if '$' in line:
                processed_line = line.split('$')[0].rstrip('\n')
                outfile.write(processed_line + '\n')
            else:
                outfile.write(line)

# 调用函数
read_and_process_file('py/zby/组播检测/汇总.txt', 'py/zby/组播检测/汇总1.txt')  # 修改输出文件名以避免覆盖原始文件

###################################################################去重#####################################
def remove_duplicates(input_file, output_file):
    # 用于存储已经遇到的URL和包含genre的行
    seen_urls = set()
    seen_lines_with_genre = set()
    # 用于存储最终输出的行
    output_lines = []
    # 打开输入文件并读取所有行
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        print("去重前的行数：", len(lines))
        # 遍历每一行
        for line in lines:
            # 使用正则表达式查找URL和包含genre的行,默认最后一行
            urls = re.findall(r'[https]?[http]?[rtsp]?[rtmp]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
            genre_line = re.search(r'\bgenre\b', line, re.IGNORECASE) is not None
            # 如果找到URL并且该URL尚未被记录
            if urls and urls[0] not in seen_urls:
                seen_urls.add(urls[0])
                output_lines.append(line)
            # 如果找到包含genre的行，无论是否已被记录，都写入新文件
            if genre_line:
                output_lines.append(line)
    # 将结果写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(output_lines)
    print("去重后的行数：", len(output_lines))
# 使用方法
remove_duplicates('py/zby/组播检测/汇总1.txt', 'py/zby/组播检测/1.txt')
##########################
with open('py/zby/组播检测/1.txt', 'r', encoding='utf-8') as file:
	# 从整理好的文本中按类别进行特定关键词提取
	keywords = ['udp','rtp','hls','tsfile']  # 需要提取的关键字列表
	pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字
# pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制
with open('py/zby/组播检测/1.txt', 'r', encoding='utf-8') as file, open('py/zby/组播检测/2.txt', 'w', encoding='utf-8') as a:  #####定义临时文件名
	a.write('\n')  #####写入临时文件名
	for line in file:
		if 'genre' in line:
			if re.search(pattern, line):  # 如果行中有任意关键字
				a.write(line)  # 将该

# 开始对组播源频道列表进行下载速度检测
# 定义一个全局队列，用于存储需要测速的频道信息
speed_test_queue = Queue()

# 用于存储测速结果的列表
speed_results = []


# 读取iptv_list.txt文件中的所有频道，并将它们添加到队列中
def load_channels_to_speed_test():
    with open('py/zby/组播检测/2.txt', 'r', encoding='utf-8') as file:
        for line in file:
            channel_info = line.strip().split(',')
            if len(channel_info) >= 2:  # 假设至少有名称和URL
                name, url = channel_info[:2]  # 只取名称和URL
                speed_test_queue.put((name, url))


# 执行下载速度测试
def download_speed_test():
    while not speed_test_queue.empty():
        channel = speed_test_queue.get()
        name, url = channel
        download_time = 5  # 设置下载时间为 5 秒
        chunk_size = 1024  # 设置下载数据块大小为 1024 字节

        try:
            start_time = time.time()
            response = requests.get(url, stream=True, timeout=download_time)
            response.raise_for_status()
            size = 0
            for chunk in response.iter_content(chunk_size=chunk_size):
                size += len(chunk)
                if time.time() - start_time >= download_time:
                    break
            download_time = time.time() - start_time
            download_rate = round(size / download_time / 1024 / 1024, 2)
        except requests.RequestException as e:
            print(f"请求异常: {e}")
            download_rate = 0

        print(f"{name},{url}, {download_rate} MB/s")
        speed_test_queue.task_done()
        speed_results.append((download_rate, name, url))


# 创建并启动线程
def start_speed_test_threads(num_threads):
    threads = []
    for _ in range(num_threads):
        thread = Thread(target=download_speed_test)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()


load_channels_to_speed_test()
start_speed_test_threads(10)  # 测试下载速度线程数
speed_results.sort(reverse=True)

# 写入分类排序后的频道信息
with open("py/zby/组播检测/speed.txt", 'w', encoding='utf-8') as file:
    for result in speed_results:
        download_rate, channel_name, channel_url = result
        if download_rate >= 0.01:  # 只写入下载速度大于或等于 0.2 MB/s 的频道
            file.write(f"{channel_name},{channel_url},{download_rate}\n")

# 对经过下载速度检测后的所有组播频道列表进行分组排序
# 从测速后的文件中读取频道列表
with open('py/zby/组播检测/speed.txt', 'r', encoding='utf-8') as file:
    channels = []
    for line in file:
        line = line.strip()
        if line:
            parts = line.split(',')
            if len(parts) == 3:
                name, url, speed = parts
                channels.append((name, url, speed))


def natural_key(string):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', string)]


def group_and_sort_channels(channels):
    groups = {
        '央视频道,#genre#': [],
        '卫视频道,#genre#': [],
        '安徽频道,#genre#': [],      
        '湖南频道,#genre#': [],
        '其他频道,#genre#': []
    }

    for name, url, speed in channels:
        if 'cctv' in name.lower():
            groups['央视频道,#genre#'].append((name, url, speed))
        elif '卫视' in name or '凤凰' in name or '翡翠' in name or 'CHC' in name:
            groups['卫视频道,#genre#'].append((name, url, speed))
        elif ('安徽' in name or '海豚' in name or '金鹰' in name or '纪实' in name or '合肥' in name or '肥东' in name
              or '肥西' in name or '长丰' in name or '滁州' in name or '全椒' in name or '来安' in name or '定远' in name
              or '凤阳' in name or '明光' in name or '芜湖' in name or '湾沚' in name or '繁昌' in name or '无为' in name
              or '南陵' in name or '马鞍山' in name or '安庆' in name or '潜山' in name or '桐城' in name or '太湖' in name
              or '黄山' in name or '徽州' in name or '太平' in name or '歙县' in name or '休宁' in name or '祁门' in name
              or '黟县' in name or '宣城' in name or '广德' in name or '郎溪' in name or '旌德' in name or '宁国' in name
              or '绩溪' in name or '池州' in name or '石台' in name or '东至' in name or '铜陵' in name or '义安' in name
              or '寿县' in name or '淮北' in name or '濉溪' in name or '宿州' in name or '萧县' in name or '泗县' in name
              or '蚌埠' in name or '五河' in name or '固镇' in name or '阜阳' in name or '颍上' in name or '界首' in name
              or '临泉' in name or '阜南' in name or '亳州' in name or '利辛' in name or '涡阳' in name or '蒙城' in name
              or '枞阳' in name or '六安' in name or '霍山' in name or '霍邱' in name or '金寨' in name or '淮南' in name):
            groups['安徽频道,#genre#'].append((name, url, speed))          
        elif ('湖南' in name or '金鹰' in name or '长沙' in name or '娄底' in name or '岳阳' in name or '张家界' in name
              or '常德' in name or '怀化' in name or '新化' in name or '株洲' in name or '桂东' in name or '武冈' in name
              or '永州' in name or '津市' in name or '浏阳' in name or '湘潭' in name or '湘西' in name or '溆浦' in name
              or '益阳' in name or '衡阳' in name or '道县' in name or '邵阳' in name or '郴州' in name or '双峰' in name
              or '东安' in name or '中方' in name or '会同' in name or '双牌' in name or '城步' in name or '宁乡' in name
              or '宁远' in name or '岳麓' in name or '新田' in name or '桃源' in name or '江华' in name or '江永' in name
              or '汨罗' in name or '洪江' in name or '涟源' in name or '湘江' in name or '祁阳' in name or '芷江' in name
              or '蓝山' in name or '辰溪' in name or '通道' in name or '靖州' in name or '麻阳' in name):
            groups['湖南频道,#genre#'].append((name, url, speed))
        else:
            groups['其他频道,#genre#'].append((name, url, speed))

        # 对每组进行排序
        for group in groups.values():
            group.sort(key=lambda x: (natural_key(x[0]), -float(x[2]) if x[2] is not None else float('-inf')))

    # 筛选相同名称的频道，只保存10个
    filtered_groups = {}
    overflow_groups = {}

    for group_name, channel_list in groups.items():
        seen_names = {}
        filtered_list = []
        overflow_list = []

        for channel in channel_list:
            name = channel[0]
            if name not in seen_names:
                seen_names[name] = 0

            if seen_names[name] < 10:
                filtered_list.append(channel)
                seen_names[name] += 1
            else:
                overflow_list.append(channel)

        filtered_groups[group_name] = filtered_list
        overflow_groups[group_name] = overflow_list

    #  获取当前时间
    now = datetime.now()
    update_time_line = f"更新时间,#genre#\n{now.strftime('%Y-%m-%d %H:%M:%S')},url\n"
    with open('py/zby/组播检测/iptv_list.txt', 'w', encoding='utf-8') as file:
        file.write(update_time_line)
        total_channels = 0  # 用于统计频道总数
        for group_name, channel_list in filtered_groups.items():
            file.write(f"{group_name}:\n")
            print(f"{group_name}:")  # 打印分组名称
            for name, url, speed in channel_list:
                if speed >= 0.5:  # 只写入下载速度大于或等于 0.3 MB/s 的频道
                  file.write(f"{name},{url}\n")
                print(f"  {name},{url},{speed}")  # 打印频道信息
                total_channels += 1  # 统计写入文件内的频道总数
            file.write("\n")
            print()  # 打印空行分隔组

    # # 保存频道数量超过10个的频道列表到新文件
    # with open('Filtered_iptv.txt', 'w', encoding='utf-8') as file:
    #     for group_name, channel_list in overflow_groups.items():
    #         if channel_list:  # 只写入非空组
    #             file.write(f"{group_name}\n")
    #             for name, url, speed in channel_list:
    #                 file.write(f"{name},{url}\n")
    #             file.write("\n")  # 打印空行分隔组
    print(f"\n经过测速分类排序后的频道列表数量为: {total_channels} 个，已全部写入iptv_list.txt文件中。")
    return groups

grouped_channels = group_and_sort_channels(channels)

# os.remove("湖南_组播.txt")
# os.remove("speed.txt")
# os.remove("ip.txt")

#  获取远程直播源文件
# url = "http://aktv.top/live.txt"
# r = requests.get(url)
# open('AKTV.txt', 'wb').write(r.content)

# 合并所有的txt文件
file_contents = []
file_paths = ["py/zby/组播检测/iptv_list.txt"]  # 替换为实际的文件路径列表
for file_path in file_paths:
    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.read()
        file_contents.append(content)

# 写入合并后的txt文件
with open("py/zby/组播检测/iptv_list.txt", "w", encoding="utf-8") as output:
    output.write('\n'.join(file_contents))
