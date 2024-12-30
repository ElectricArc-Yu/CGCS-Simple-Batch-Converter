import numpy as np
import pandas as pd
import math
import csv
from pyproj import Proj, transform
import warnings
import os
import configparser
from tqdm import tqdm

warnings.simplefilter(action='ignore', category=FutureWarning)

try:

    # 读取配置文件
    config = configparser.ConfigParser()
    with open('config.cfg', 'r', encoding='utf-8') as configfile:
        config.read_file(configfile)

    # 基本设置
    OUTPUT_HEIGHT = config.getboolean('settings', 'output_height')
    OUTPUT_FORMAT = config.get('settings', 'output_format')
    INPUT_FILE = config.get('settings', 'input_file')
    OUTPUT_FOLDER = config.get('settings', 'output_folder')
    ACCURACY = config.getint('settings', 'accuracy')

    # 固定参数设置
    WGS84LONG = config.getfloat('settings', 'wgs84_long')
    WGS84SHORT = config.getfloat('settings', 'wgs84_short')
    E2 = (WGS84LONG**2 - WGS84SHORT**2) / WGS84LONG**2
    CGCS2000 = Proj(f'epsg:{config.getint("settings", "cgcs2000_epsg")}')
    WGS84 = Proj(f'epsg:{config.getint("settings", "wgs84_epsg")}')

    # 初始化
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    # 读取数据
    #如果是csv文件，使用pd.read_csv
    #如果是excel文件，使用pd.read_excel
    if INPUT_FILE.endswith('.csv'):
        data = pd.read_csv(INPUT_FILE)
    elif INPUT_FILE.endswith('.xlsx'):
        data = pd.read_excel(INPUT_FILE)
    print("数据总数: " + str(data.shape[0]))

    # 通过Pyproj将CGCS2000坐标转化为经纬度坐标
    def cgcs2000_to_wgs84(x, y):
        lat, lon = transform(CGCS2000, WGS84, x, y)
        return lat, lon

    # 将float64转为度数格式
    def float_to_dms(origin):
        degree = int(origin)
        minute = int((origin - degree) * 60)
        second = round(((origin - degree) * 60 - minute) * 60, ACCURACY)
        second_str = round_to_accuracy(second)
        return f"{degree}°{minute}′{second_str}″"

    #保留小数点后几位
    def round_to_accuracy(number):
        number_str = str(number)
        if '.' in number_str:
            if len(number_str.split('.')[1]) < ACCURACY:
                number_str = number_str + '0' * (ACCURACY - len(number_str.split('.')[1]))
        else:
            number_str = number_str + '.' + '0' * ACCURACY
        return number_str

    df = pd.DataFrame(columns=['Point Set'])

    rows = []

    for index, row in tqdm(data.iterrows(), total=data.shape[0], desc="转换中 (CGCS2000 转 WGS84)"):
        lat, lon = cgcs2000_to_wgs84(row['X'], row['Y'])
        if OUTPUT_HEIGHT:
            rows.append({'Point Set': row['Point Set'], 'Latitude': float_to_dms(lat), 'Longitude': float_to_dms(lon), 'Height': str(row['Z'])})
        else:
            rows.append({'Point Set': row['Point Set'], 'Latitude': float_to_dms(lat), 'Longitude': float_to_dms(lon), 'Height': ''})

    df = pd.concat([df, pd.DataFrame(rows)], ignore_index=True)

    if OUTPUT_FORMAT == 'CSV':
        output_file_name = os.path.splitext(os.path.basename(INPUT_FILE))[0] + ' Converted Data.csv'
        df.to_csv(os.path.join(OUTPUT_FOLDER, output_file_name), index=False)
    elif OUTPUT_FORMAT == 'Excel':
        output_file_name = os.path.splitext(os.path.basename(INPUT_FILE))[0] + ' Converted Data.xlsx'
        df.to_csv(os.path.join(OUTPUT_FOLDER, output_file_name), index=False)
    else:
        print('输出格式错误')

except Exception as e:
    print(f"发生错误: {e}")

finally:
    input("按任意键退出...")