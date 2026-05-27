import csv
import json
from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parent
PAGES = ROOT / "pages"
IMG_DIR = ROOT / "question_images"
OUT_JSON = ROOT / "hainan_2024_geography_exam_question_bank.json"
OUT_CSV = ROOT / "hainan_2024_geography_exam_question_bank.csv"
OUT_MD = ROOT / "hainan_2024_geography_exam_question_bank.md"


FIGURES = [
    ("figure_01", 1, (100, 360, 680, 920), "中国的省级行政区域示意图", [1, 2]),
    ("figure_02", 1, (95, 1345, 540, 1585), "干栏式木楼景观图", [3, 4]),
    ("table_01", 1, (85, 1925, 770, 2405), "不同年份中国城镇人口与农村人口比重", [5, 6]),
    ("figure_03", 2, (1060, 440, 1605, 940), "中国主要气象灾害的分布", [7, 8]),
    ("figure_04", 2, (1250, 960, 1615, 1370), "地球自转运动方向示意图", [9]),
    ("figure_05", 2, (110, 1690, 1585, 2070), "碳达峰、碳中和及长江流域局部区域示意图", [10, 11]),
    ("figure_06", 3, (90, 255, 860, 565), "我国南方某茶叶优势产区等高线地形图", [12, 13]),
    ("figure_07", 3, (95, 920, 940, 1255), "世界人口增长示意图", [14, 15]),
    ("figure_08", 3, (815, 1565, 1605, 2110), "亚洲局部区域示意图", [16, 17]),
    ("figure_09", 4, (1265, 190, 1610, 700), "我国部分海域示意图", [18, 19]),
    ("figure_10", 4, (1225, 1660, 1580, 1995), "北冰洋科考途经区域示意图", [23, 24]),
    ("figure_11", 5, (1135, 110, 1610, 570), "中国环渤海经济圈位置示意图", [26, 27]),
    ("figure_12", 5, (90, 700, 1150, 1210), "日本和巴西简图", [28, 29]),
    ("table_02", 5, (85, 1780, 1235, 2225), "香港进出口商品的地区构成", [30, 31]),
    ("figure_13", 6, (170, 115, 1110, 625), "粤港澳大湾区示意图", [30, 31]),
    ("figure_14", 6, (135, 1290, 1085, 1780), "中国南极科考站分布图和南极地区气候资料", [32, 33]),
    ("figure_15", 7, (95, 190, 1580, 515), "某区域海陆分布示意图和甲、乙两地气候资料", [34, 35]),
    ("figure_16", 7, (80, 1310, 1580, 1810), "二十四节气示意图和海南7月平均气温及环岛旅游公路分布示意图", [36]),
    ("figure_17", 8, (900, 130, 1625, 700), "中国三大育种基地分布和水土资源比重示意图", [37]),
    ("figure_18", 8, (735, 1165, 1630, 1615), "渝新欧班列主要线路示意图", [38]),
]


def image_path(name: str) -> str:
    return f"question_images/{name}.png"


QUESTIONS = [
    {
        "id": "HN2024-GEO-001",
        "number": 1,
        "type": "single_choice",
        "score": 2,
        "source_page": 1,
        "group_prompt": "戏曲是中华优秀传统文化的亮丽名片，京剧、豫剧、秦腔、川剧、琼剧等百花争艳，各具地方特色。读图为“中国的省级行政区域示意图”，完成1-2题。",
        "stem": "琼剧是海南省的代表剧种，主要流行于图中的",
        "options": {"A": "甲地", "B": "乙地", "C": "丙地", "D": "丁地"},
        "answer": "",
        "images": [image_path("figure_01")],
    },
    {
        "id": "HN2024-GEO-002",
        "number": 2,
        "type": "single_choice",
        "score": 2,
        "source_page": 1,
        "group_prompt": "戏曲是中华优秀传统文化的亮丽名片，京剧、豫剧、秦腔、川剧、琼剧等百花争艳，各具地方特色。读图为“中国的省级行政区域示意图”，完成1-2题。",
        "stem": "我国传统文化地域差异显著的主要原因是",
        "options": {"A": "地处高纬", "B": "疆域辽阔", "C": "位于热带", "D": "海域宽广"},
        "answer": "",
        "images": [image_path("figure_01")],
    },
    {
        "id": "HN2024-GEO-003",
        "number": 3,
        "type": "single_choice",
        "score": 2,
        "source_page": 1,
        "group_prompt": "干栏式木楼是我国西南少数民族地区的传统民居，木楼底层架空，下层堆放杂物，上层住人。读图为干栏式木楼景观图，完成3-4题。",
        "stem": "干栏式木楼反映当地的气候特征是",
        "options": {"A": "干旱", "B": "寒冷", "C": "湿热", "D": "干热"},
        "answer": "",
        "images": [image_path("figure_02")],
    },
    {
        "id": "HN2024-GEO-004",
        "number": 4,
        "type": "single_choice",
        "score": 2,
        "source_page": 1,
        "group_prompt": "干栏式木楼是我国西南少数民族地区的传统民居，木楼底层架空，下层堆放杂物，上层住人。读图为干栏式木楼景观图，完成3-4题。",
        "stem": "下列少数民族集中分布在该地区的是",
        "options": {"A": "傣族", "B": "维吾尔族", "C": "朝鲜族", "D": "蒙古族"},
        "answer": "",
        "images": [image_path("figure_02")],
    },
    {
        "id": "HN2024-GEO-005",
        "number": 5,
        "type": "single_choice",
        "score": 2,
        "source_page": 1,
        "group_prompt": "读表，完成5-6题。",
        "stem": "据表可知，我国",
        "options": {"A": "农村人口比重越来越大", "B": "1970年城镇人口比农村人口多", "C": "城镇人口比重不断增大", "D": "2023年农村人口比城镇人口多"},
        "answer": "",
        "images": [image_path("table_01")],
    },
    {
        "id": "HN2024-GEO-006",
        "number": 6,
        "type": "single_choice",
        "score": 2,
        "source_page": 2,
        "group_prompt": "读表，完成5-6题。",
        "stem": "我国城乡人口比重发生变化的首要原因是",
        "options": {"A": "农村基础设施完善", "B": "农村耕地面积扩大", "C": "城市空气质量优良", "D": "我国经济快速发展"},
        "answer": "",
        "images": [image_path("table_01")],
    },
    {
        "id": "HN2024-GEO-007",
        "number": 7,
        "type": "single_choice",
        "score": 2,
        "source_page": 2,
        "group_prompt": "5月12日是全国防灾减灾日，2024年的主题是“人人讲安全、个个会应急——着力提升基础防灾避险能力”。读图为“中国主要气象灾害的分布”，完成7-8题。",
        "stem": "我国洪涝灾害多发区主要分布在",
        "options": {"A": "西北地区", "B": "东北地区", "C": "东南地区", "D": "青藏地区"},
        "answer": "",
        "images": [image_path("figure_03")],
    },
    {
        "id": "HN2024-GEO-008",
        "number": 8,
        "type": "single_choice",
        "score": 2,
        "source_page": 2,
        "group_prompt": "5月12日是全国防灾减灾日，2024年的主题是“人人讲安全、个个会应急——着力提升基础防灾避险能力”。读图为“中国主要气象灾害的分布”，完成7-8题。",
        "stem": "中学生需要掌握自然灾害安全防护的基本技能。下列自然灾害应对方法合理的是",
        "options": {"A": "地震发生时应迅速乘坐电梯逃生", "B": "遇到洪水时应及时跑到低洼地带", "C": "刮台风时应躲在大型广告牌下避风", "D": "遇泥石流应向垂直于其流向的山坡上跑"},
        "answer": "",
        "images": [image_path("figure_03")],
    },
    {
        "id": "HN2024-GEO-009",
        "number": 9,
        "type": "single_choice",
        "score": 2,
        "source_page": 2,
        "group_prompt": "下图是同学们为演示地球自转运动设想的四种方向，完成9题。",
        "stem": "下图是同学们为演示地球自转运动设想的四种方向，正确的是",
        "options": {"A": "甲", "B": "乙", "C": "丙", "D": "丁"},
        "answer": "",
        "images": [image_path("figure_04")],
    },
    {
        "id": "HN2024-GEO-010",
        "number": 10,
        "type": "single_choice",
        "score": 2,
        "source_page": 2,
        "group_prompt": "长江干流的乌东德、白鹤滩、溪洛渡、向家坝、三峡和葛洲坝等六座梯级水电站，共同构成目前世界上最大清洁能源走廊，对我国在2030年前实现碳达峰、2060年前实现碳中和具有重要意义。读图为碳达峰、碳中和及长江流域局部区域示意图，完成10-11题。",
        "stem": "长江干流建成清洁能源走廊，对实现碳达峰、碳中和的积极作用是",
        "options": {"A": "保护淡水资源", "B": "防止水土流失", "C": "降低火电比重", "D": "防止洪涝灾害"},
        "answer": "",
        "images": [image_path("figure_05")],
    },
    {
        "id": "HN2024-GEO-011",
        "number": 11,
        "type": "single_choice",
        "score": 2,
        "source_page": 2,
        "group_prompt": "长江干流的乌东德、白鹤滩、溪洛渡、向家坝、三峡和葛洲坝等六座梯级水电站，共同构成目前世界上最大清洁能源走廊，对我国在2030年前实现碳达峰、2060年前实现碳中和具有重要意义。读图为碳达峰、碳中和及长江流域局部区域示意图，完成10-11题。",
        "stem": "长江干流上游建设水电站的优势条件是",
        "options": {"A": "江阔水深", "B": "植被茂密", "C": "水流平缓", "D": "落差很大"},
        "answer": "",
        "images": [image_path("figure_05")],
    },
    {
        "id": "HN2024-GEO-012",
        "number": 12,
        "type": "single_choice",
        "score": 2,
        "source_page": 3,
        "group_prompt": "中国种茶历史悠久，茶文化底蕴深厚。茶树适宜生长在温度20-25℃，年降水量1500mm以上，排水条件较好的坡地。图为我国南方某茶叶优势产区等高线地形图。结合图文材料，完成12-13题。",
        "stem": "该茶树种植区的地理环境特征为",
        "options": {"A": "位于高纬地区", "B": "属于半干旱地区", "C": "气候温暖湿润", "D": "荒漠草原为主"},
        "answer": "",
        "images": [image_path("figure_06")],
    },
    {
        "id": "HN2024-GEO-013",
        "number": 13,
        "type": "single_choice",
        "score": 2,
        "source_page": 3,
        "group_prompt": "中国种茶历史悠久，茶文化底蕴深厚。茶树适宜生长在温度20-25℃，年降水量1500mm以上，排水条件较好的坡地。图为我国南方某茶叶优势产区等高线地形图。结合图文材料，完成12-13题。",
        "stem": "图示区域茶园选址最优的是",
        "options": {"A": "甲", "B": "乙", "C": "丙", "D": "丁"},
        "answer": "",
        "images": [image_path("figure_06")],
    },
    {
        "id": "HN2024-GEO-014",
        "number": 14,
        "type": "single_choice",
        "score": 2,
        "source_page": 3,
        "group_prompt": "读图为“世界人口增长示意图”，完成14-15题。",
        "stem": "世界人口达到80亿的年份是",
        "options": {"A": "1987年", "B": "1999年", "C": "2011年", "D": "2022年"},
        "answer": "",
        "images": [image_path("figure_07")],
    },
    {
        "id": "HN2024-GEO-015",
        "number": 15,
        "type": "single_choice",
        "score": 2,
        "source_page": 3,
        "group_prompt": "读图为“世界人口增长示意图”，完成14-15题。",
        "stem": "图示时间段世界人口增长特点是",
        "options": {"A": "持续增长", "B": "保持不变", "C": "匀速增长", "D": "减速增长"},
        "answer": "",
        "images": [image_path("figure_07")],
    },
    {
        "id": "HN2024-GEO-016",
        "number": 16,
        "type": "single_choice",
        "score": 2,
        "source_page": 3,
        "group_prompt": "在“一带一路”倡议下，中国与图示地区经贸往来频繁，合作共赢，共建人类命运共同体。读图为亚洲局部区域示意图，完成16-17题。",
        "stem": "甲、乙、丙三个半岛的共同地理特征是",
        "options": {"A": "被赤道穿过", "B": "濒临印度洋", "C": "季风气候显著", "D": "以高原为主"},
        "answer": "",
        "images": [image_path("figure_08")],
    },
    {
        "id": "HN2024-GEO-017",
        "number": 17,
        "type": "single_choice",
        "score": 2,
        "source_page": 3,
        "group_prompt": "在“一带一路”倡议下，中国与图示地区经贸往来频繁，合作共赢，共建人类命运共同体。读图为亚洲局部区域示意图，完成16-17题。",
        "stem": "关于中国与三地间的贸易往来说法正确的是",
        "options": {"A": "从甲地进口的商品主要是石油", "B": "从乙地进口的商品主要是乳畜产品", "C": "从丙地进口的商品主要是小麦", "D": "中国向三地出口的商品主要是铁矿"},
        "answer": "",
        "images": [image_path("figure_08")],
    },
    {
        "id": "HN2024-GEO-018",
        "number": 18,
        "type": "single_choice",
        "score": 2,
        "source_page": 4,
        "group_prompt": "深耕海洋经济，“向海图强”，加快建设“南海粮仓”，是海南省加快迈向海洋强省的重要工作。读图为“我国部分海域示意图”，完成18-19题。",
        "stem": "南海诸岛是中国领土的组成部分，是中国固有领土。关于我国黄岩岛表述正确的是",
        "options": {"A": "西沙群岛最大岛屿", "B": "属于中沙群岛", "C": "我国最南端的岛屿", "D": "位于南海西部"},
        "answer": "",
        "images": [image_path("figure_09")],
    },
    {
        "id": "HN2024-GEO-019",
        "number": 19,
        "type": "single_choice",
        "score": 2,
        "source_page": 4,
        "group_prompt": "深耕海洋经济，“向海图强”，加快建设“南海粮仓”，是海南省加快迈向海洋强省的重要工作。读图为“我国部分海域示意图”，完成18-19题。",
        "stem": "有利于打造“南海粮仓”，实现海洋可持续发展的是：①用电网捕鱼；②季节性休渔；③保护红树林；④采挖珊瑚礁。",
        "options": {"A": "①②", "B": "②③", "C": "①④", "D": "③④"},
        "answer": "",
        "images": [image_path("figure_09")],
    },
    {
        "id": "HN2024-GEO-020",
        "number": 20,
        "type": "single_choice",
        "score": 2,
        "source_page": 4,
        "group_prompt": "为了提高地理实践力，海南省某中学组织八年级学生开展“探访湿地”研学活动研究湿地功能。据此完成20-21题。",
        "stem": "开展本次研学活动的合理顺序是：①选用湿地公园电子地图；②规划湿地考察路线；③探究湿地生态环境效应；④提出湿地保护建议。",
        "options": {"A": "①-②-③-④", "B": "②-③-①-④", "C": "②-①-③-④", "D": "④-③-②-①"},
        "answer": "",
        "images": [],
    },
    {
        "id": "HN2024-GEO-021",
        "number": 21,
        "type": "single_choice",
        "score": 2,
        "source_page": 4,
        "group_prompt": "为了提高地理实践力，海南省某中学组织八年级学生开展“探访湿地”研学活动研究湿地功能。据此完成20-21题。",
        "stem": "湿地的生态环境效益主要表现在：①涵养水源；②保护耕地；③提高居民生活水平；④维护生物多样性。",
        "options": {"A": "①②", "B": "②③", "C": "①④", "D": "③④"},
        "answer": "",
        "images": [],
    },
    {
        "id": "HN2024-GEO-022",
        "number": 22,
        "type": "single_choice",
        "score": 2,
        "source_page": 4,
        "group_prompt": "",
        "stem": "我国能实现“神舟”问天、“嫦娥”揽月、“祝融”探火、“羲和”逐日、“蛟龙”入海、“北斗”组网，主要得益于",
        "options": {"A": "自然资源丰富", "B": "劳动力数量多", "C": "土地面积广大", "D": "高新技术发展"},
        "answer": "",
        "images": [],
    },
    {
        "id": "HN2024-GEO-023",
        "number": 23,
        "type": "single_choice",
        "score": 2,
        "source_page": 4,
        "group_prompt": "中国第13次北冰洋科学考察科研成果，为我国有效应对全球气候变化提供重要数据支撑。本次科考途经图为所示区域。据此完成23-25题。",
        "stem": "科考船途经的甲海峡是",
        "options": {"A": "白令海峡", "B": "马六甲海峡", "C": "台湾海峡", "D": "土耳其海峡"},
        "answer": "",
        "images": [image_path("figure_10")],
    },
    {
        "id": "HN2024-GEO-024",
        "number": 24,
        "type": "single_choice",
        "score": 2,
        "source_page": 4,
        "group_prompt": "中国第13次北冰洋科学考察科研成果，为我国有效应对全球气候变化提供重要数据支撑。本次科考途经图为所示区域。据此完成23-25题。",
        "stem": "甲海峡沟通的海洋是",
        "options": {"A": "北冰洋、大西洋", "B": "北冰洋、太平洋", "C": "大西洋、太平洋", "D": "印度洋、太平洋"},
        "answer": "",
        "images": [image_path("figure_10")],
    },
    {
        "id": "HN2024-GEO-025",
        "number": 25,
        "type": "single_choice",
        "score": 2,
        "source_page": 4,
        "group_prompt": "中国第13次北冰洋科学考察科研成果，为我国有效应对全球气候变化提供重要数据支撑。本次科考途经图为所示区域。据此完成23-25题。",
        "stem": "下列做法有利于减少二氧化碳排放，进而减缓全球变暖的有：①推广使用清洁能源；②用柴草做生活燃料；③大规模发展重工业；④乘坐公共交通出行。",
        "options": {"A": "①②", "B": "②③", "C": "①④", "D": "③④"},
        "answer": "",
        "images": [],
    },
    {
        "id": "HN2024-GEO-026",
        "number": 26,
        "type": "single_choice",
        "score": 2,
        "source_page": 5,
        "group_prompt": "“环渤海”经济圈带动我国北方地区经济迅速发展。读图为中国“环渤海”经济圈位置示意图，完成26-27题。",
        "stem": "沈阳所属的工业基地是",
        "options": {"A": "辽中南工业基地", "B": "长江三角洲工业基地", "C": "京津唐工业基地", "D": "珠江三角洲工业基地"},
        "answer": "",
        "images": [image_path("figure_11")],
    },
    {
        "id": "HN2024-GEO-027",
        "number": 27,
        "type": "single_choice",
        "score": 2,
        "source_page": 5,
        "group_prompt": "“环渤海”经济圈带动我国北方地区经济迅速发展。读图为中国“环渤海”经济圈位置示意图，完成26-27题。",
        "stem": "环渤海地区发展重工业的有利自然条件",
        "options": {"A": "矿产资源丰富", "B": "劳动力丰富", "C": "海路交通便利", "D": "市场广阔"},
        "answer": "",
        "images": [image_path("figure_11")],
    },
    {
        "id": "HN2024-GEO-028",
        "number": 28,
        "type": "single_choice",
        "score": 2,
        "source_page": 5,
        "group_prompt": "某地理学习小组对比学习日本和巴西，探究两国的地理特征。读图，完成28-29题。",
        "stem": "对比两国河流特征说法正确的是",
        "options": {"A": "含沙量均大", "B": "都有结冰期", "C": "巴西亚马孙河流域面积广", "D": "日本的河流多自南向北流"},
        "answer": "",
        "images": [image_path("figure_12")],
    },
    {
        "id": "HN2024-GEO-029",
        "number": 29,
        "type": "single_choice",
        "score": 2,
        "source_page": 5,
        "group_prompt": "某地理学习小组对比学习日本和巴西，探究两国的地理特征。读图，完成28-29题。",
        "stem": "关于两国地理特征表述正确的是",
        "options": {"A": "都位于热带，水热充足", "B": "两国的贸易往来以海运为主", "C": "两国矿产资源都很丰富", "D": "城市都集中分布在太平洋沿岸"},
        "answer": "",
        "images": [image_path("figure_12")],
    },
    {
        "id": "HN2024-GEO-030",
        "number": 30,
        "type": "single_choice",
        "score": 2,
        "source_page": 6,
        "group_prompt": "2023年12月，随着港珠澳大桥旅游正式向公众开放，祖国内地赴港、澳旅游的人持续增长。读表为香港出口商品的地区构成和图为粤港澳大湾区示意图，完成30-31题。",
        "stem": "关于港珠澳大桥表述正确的是：①联通了港澳和东南亚地区；②促进港澳地区旅游业发展；③连接香港、澳门、广州三地；④加强粤港澳大湾区内部联系。",
        "options": {"A": "①③", "B": "①④", "C": "②③", "D": "②④"},
        "answer": "",
        "images": [image_path("table_02"), image_path("figure_13")],
    },
    {
        "id": "HN2024-GEO-031",
        "number": 31,
        "type": "single_choice",
        "score": 2,
        "source_page": 6,
        "group_prompt": "2023年12月，随着港珠澳大桥旅游正式向公众开放，祖国内地赴港、澳旅游的人持续增长。读表为香港出口商品的地区构成和图为粤港澳大湾区示意图，完成30-31题。",
        "stem": "据表可知，香港2020年相较于2010年",
        "options": {"A": "和祖国内地经济联系更加紧密", "B": "出口到其他国家和地区商品比重上升", "C": "从祖国内地进口商品比重增大", "D": "从其他国家和地区进口商品比重下降"},
        "answer": "",
        "images": [image_path("table_02"), image_path("figure_13")],
    },
    {
        "id": "HN2024-GEO-032",
        "number": 32,
        "type": "single_choice",
        "score": 2,
        "source_page": 6,
        "group_prompt": "中国2023年11月开始为期5个多月的第40次南极科学考察，并于2024年2月建成我国第5个南极科考站——秦岭站。读图为中国南极科考站分布图和南极地区气候资料，完成32-33题。",
        "stem": "在此次南极地区考察、建站过程中，我国科考队员需要克服的困难主要有：①极夜；②酷寒；③烈风；④暴雨。",
        "options": {"A": "①②", "B": "②③", "C": "③④", "D": "①④"},
        "answer": "",
        "images": [image_path("figure_14")],
    },
    {
        "id": "HN2024-GEO-033",
        "number": 33,
        "type": "single_choice",
        "score": 2,
        "source_page": 6,
        "group_prompt": "中国2023年11月开始为期5个多月的第40次南极科学考察，并于2024年2月建成我国第5个南极科考站——秦岭站。读图为中国南极科考站分布图和南极地区气候资料，完成32-33题。",
        "stem": "若一架飞机从秦岭站向泰山站运送物资，沿最短航线飞行的方向为",
        "options": {"A": "一直向正西", "B": "先向东南再向东北", "C": "一直向西北", "D": "先向西南再向西北"},
        "answer": "",
        "images": [image_path("figure_14")],
    },
    {
        "id": "HN2024-GEO-034",
        "number": 34,
        "type": "single_choice",
        "score": 2,
        "source_page": 7,
        "group_prompt": "地理实践是学习地理的有效途径，某地理小组搜集到某区域海陆分布示意图和甲、乙两地气候资料（下图和表）。据此完成34-35题。",
        "stem": "甲、乙两地最可能位于",
        "options": {"A": "非洲", "B": "北美洲", "C": "南美洲", "D": "大洋洲"},
        "answer": "",
        "images": [image_path("figure_15")],
    },
    {
        "id": "HN2024-GEO-035",
        "number": 35,
        "type": "single_choice",
        "score": 2,
        "source_page": 7,
        "group_prompt": "地理实践是学习地理的有效途径，某地理小组搜集到某区域海陆分布示意图和甲、乙两地气候资料（下图和表）。据此完成34-35题。",
        "stem": "关于甲、乙两地的自然地理特征的叙述，正确的是",
        "options": {"A": "甲地年降水量集中在1月", "B": "乙地夏季温和湿润，冬季寒冷干燥", "C": "1月甲地盛行西北季风", "D": "7月乙地等温线较同纬度海洋偏北"},
        "answer": "",
        "images": [image_path("figure_15")],
    },
    {
        "id": "HN2024-GEO-036",
        "number": 36,
        "type": "non_choice",
        "score": 10,
        "source_page": 7,
        "group_prompt": "读图文材料，完成下列各题。",
        "stem": "材料一：二十四节气是中华优秀传统文化，是劳动人民智慧的结晶。\n材料二：海南环岛旅游公路2023年12月18日全线通车，线路全长988km，贯穿海口等12个滨海市县、31家A级景区，对促进海南自贸港建设具有重大意义。\n材料三：下图为“二十四节气示意图”和“海南7月平均气温及环岛旅游公路分布示意图”。\n（1）二十四节气变化的主要原因是地球的____运动，海南环岛旅游公路全线通车的日期最接近的节气是____，参加通车仪式的北方游客感受到当日海口白昼时长比其家乡____，造成两地当日昼长差异的主要影响因素是____。\n（2）7月海南岛降水丰富，是因为受富含水汽的____季风的影响，此时海南岛的平均气温分布特征为____，其主要原因是海南岛____。\n（3）据材料二说出影响海南岛旅游公路选线的主要因素是____。海南环岛旅游公路等交通设施逐步完善，对建设海南自由贸易港有哪些积极作用____？",
        "options": {},
        "answer": "",
        "images": [image_path("figure_16")],
    },
    {
        "id": "HN2024-GEO-037",
        "number": 37,
        "type": "non_choice",
        "score": 10,
        "source_page": 8,
        "group_prompt": "结合图文资料，完成下列各题。",
        "stem": "材料一：粮食安全是国家的物质保障。我国三大育种基地充分利用自然条件优势着力打造农作物“种业芯片”，其中甘肃省河西走廊是我国最大的玉米制种基地，“天干地不干”是其作为种子生产基地的独特自然条件。\n材料二：图为中国三大育种基地分布和四大地理区域水资源与耕地资源占全国比重示意图。\n（1）农谚“冬天麦盖三层被，来年枕着馒头睡”中描述的粮食作物是____，该作物主要产区位于我国四大地理区域中的____地区，该地区水土资源的配合特点是____。\n（2）我国三大育种基地中，热量条件最好的是____育种基地。甘肃育种基地成为我国最大的玉米制种基地的优势自然条件有哪些____？\n（3）耕地安全与种子安全同等重要，是粮食安全的重要保障。据图可知，我国耕地资源的空间分布特点为____，结合所学知识，说出保护耕地的有效措施____。",
        "options": {},
        "answer": "",
        "images": [image_path("figure_17")],
    },
    {
        "id": "HN2024-GEO-038",
        "number": 38,
        "type": "non_choice",
        "score": 10,
        "source_page": 8,
        "group_prompt": "读图文材料，完成下列各题。",
        "stem": "材料一：2024年5月，国家主席习近平应邀对欧洲的法国、塞尔维亚和匈牙利进行国事访问，与三国领导人达成多项共识，取得丰硕成果，中欧合作再出发。\n材料二：“渝新欧”班列线路东起我国重庆，西至德国杜伊斯堡，全长11000多千米，是共建“一带一路”合作的重要组成部分。经过十多年发展，中欧贸易量日益增大。\n材料三：图为“渝新欧”班列主要线路示意图。\n（1）中欧贸易量日益增大，其中“渝新欧”班列运回中国的农产品，以欧洲西部盛产的牛羊肉和乳产品为主，说明欧洲西部的____业发达，运用所学知识，说出该地区发展此类农业的有利条件是____。\n（2）沿着“渝新欧”班列主要线路从杜伊斯堡到阿拉山口的植被发生明显变化，依次是____，原因是____。\n（3）与海运相比，“渝新欧”班列在货物运输方面的优势是____。探究：“渝新欧”班列途经俄罗斯，该国的贝加尔湖结冰期较周边地区偏长，结冰开始的时间相对较晚，融冰时间更晚的原因____。",
        "options": {},
        "answer": "",
        "images": [image_path("figure_18")],
    },
]


def crop_figures() -> None:
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    for name, page, box, _, _ in FIGURES:
        source = Image.open(PAGES / f"page-{page:02d}.png").convert("RGB")
        crop = source.crop(box)
        crop = ImageOps.autocontrast(crop, cutoff=1)
        crop.save(IMG_DIR / f"{name}.png", optimize=True)


def write_json() -> None:
    payload = {
        "source": {
            "id": "hainan_2024_geography_exam",
            "title": "2024年海南省中考地理真题",
            "subject": "地理",
            "exam_time_minutes": None,
            "full_score": 100,
            "original_pdf": "2024年海南省中考地理真题（试题）.pdf",
            "notes": "本题库由PDF文字层与页面图人工校对生成；当前未提供答案卷，answer字段暂为空。",
        },
        "figures": [
            {
                "id": name,
                "title": title,
                "source_page": page,
                "file": image_path(name),
                "linked_question_numbers": linked,
            }
            for name, page, _, title, linked in FIGURES
        ],
        "questions": QUESTIONS,
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_csv() -> None:
    with OUT_CSV.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "id",
                "number",
                "type",
                "score",
                "source_page",
                "group_prompt",
                "stem",
                "option_a",
                "option_b",
                "option_c",
                "option_d",
                "answer",
                "images",
            ],
        )
        writer.writeheader()
        for question in QUESTIONS:
            options = question.get("options", {})
            writer.writerow(
                {
                    "id": question["id"],
                    "number": question["number"],
                    "type": question["type"],
                    "score": question["score"],
                    "source_page": question["source_page"],
                    "group_prompt": question["group_prompt"],
                    "stem": question["stem"],
                    "option_a": options.get("A", ""),
                    "option_b": options.get("B", ""),
                    "option_c": options.get("C", ""),
                    "option_d": options.get("D", ""),
                    "answer": question.get("answer", ""),
                    "images": ";".join(question.get("images", [])),
                }
            )


def write_markdown() -> None:
    lines = [
        "# 2024年海南省中考地理真题题库",
        "",
        "> 注：当前未提供答案卷，`answer` 字段暂为空；图片路径相对于本目录。",
        "",
    ]
    for question in QUESTIONS:
        lines.append(f"## {question['number']}. {question['stem']}")
        if question.get("group_prompt"):
            lines.append("")
            lines.append(f"材料/题组：{question['group_prompt']}")
        if question.get("options"):
            lines.append("")
            for key in ["A", "B", "C", "D"]:
                if key in question["options"]:
                    lines.append(f"- {key}. {question['options'][key]}")
        if question.get("images"):
            lines.append("")
            lines.append("关联图片：" + "，".join(question["images"]))
        lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    crop_figures()
    write_json()
    write_csv()
    write_markdown()
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_CSV}")
    print(f"wrote {OUT_MD}")
    print(f"cropped {len(FIGURES)} figures to {IMG_DIR}")


if __name__ == "__main__":
    main()
