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
    DATA_FOLDER = config.get('settings', 'data_folder')
    OUTPUT_FOLDER = config.get('settings', 'output_folder')
    ACCURACY = config.getint('settings', 'accuracy')
    EXPORT_FORMAT = config.get('settings', 'export_format')

    # 固定参数设置
    WGS84LONG = config.getfloat('settings', 'wgs84_long')
    WGS84SHORT = config.getfloat('settings', 'wgs84_short')
    E2 = (WGS84LONG**2 - WGS84SHORT**2) / WGS84LONG**2
    CGCS2000 = Proj(f'epsg:{config.getint("settings", "cgcs2000_epsg")}')
    WGS84 = Proj(f'epsg:{config.getint("settings", "wgs84_epsg")}')

    # 初始化
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

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

    # 保留小数点后几位
    def round_to_accuracy(number):
        number_str = str(number)
        if '.' in number_str:
            if len(number_str.split('.')[1]) < ACCURACY:
                number_str = number_str + '0' * (ACCURACY - len(number_str.split('.')[1]))
        else:
            number_str = number_str + '.' + '0' * ACCURACY
        return number_str

    # 读取DATA_FOLDER下所有的Excel和CSV文件
    data_files = [file for file in os.listdir(DATA_FOLDER) if file.endswith(('.xlsx', '.csv'))]
    total_files = len(data_files)
    print(f"总文件数: {total_files}")

    nan_count = 0
    files_with_nan = set()

    for file_name in data_files:
        input_file_path = os.path.join(DATA_FOLDER, file_name)
        if file_name.endswith('.xlsx'):
            data = pd.read_excel(input_file_path)
        elif file_name.endswith('.csv'):
            data = pd.read_csv(input_file_path)
        else:
            break
        print(f"正在处理文件: {file_name}, 数据总数: {data.shape[0]}")

        df = pd.DataFrame(columns=['Point Set'])
        rows = []

        for index, row in tqdm(data.iterrows(), total=data.shape[0], desc=f"转换中 (CGCS2000 转 WGS84) - {file_name}"):
            if pd.isna(row['X']) or pd.isna(row['Y']):
                nan_count += 1
                files_with_nan.add(file_name)
                continue
            lat, lon = cgcs2000_to_wgs84(row['X'], row['Y'])
            if OUTPUT_HEIGHT:
                rows.append({'Point Set': row['Point Set'], 'Latitude': float_to_dms(lat), 'Longitude': float_to_dms(lon), 'Height': str(row['Z'])})
            else:
                rows.append({'Point Set': row['Point Set'], 'Latitude': float_to_dms(lat), 'Longitude': float_to_dms(lon), 'Height': ''})

        df = pd.concat([df, pd.DataFrame(rows)], ignore_index=True)

        output_file_name = os.path.splitext(file_name)[0] + ' Converted Data.csv'
        if  OUTPUT_FORMAT == 'CSV':
            if EXPORT_FORMAT == '1':
                df.to_csv(os.path.join(OUTPUT_FOLDER, output_file_name), index=False)
            elif EXPORT_FORMAT == '2':
                df.to_csv(os.path.join(OUTPUT_FOLDER, output_file_name), encoding='GBK', index=False)
        elif OUTPUT_FORMAT == 'Excel':
            if EXPORT_FORMAT == '1':
                df.to_excel(os.path.join(OUTPUT_FOLDER, output_file_name), index=False)
            elif EXPORT_FORMAT == '2':
                df.to_excel(os.path.join(OUTPUT_FOLDER, output_file_name), encoding='GBK', index=False)

    print(f"总共跳过的NaN行数: {nan_count}")
    print(f"包含NaN数据的文件: {', '.join(files_with_nan)}")

except Exception as e:
    print(f"发生错误: {e}")

finally:
    input("按任意键退出...")