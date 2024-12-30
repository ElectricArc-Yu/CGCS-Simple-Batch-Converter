# CGCS Simple Batch Converter

A simple batch converter for CGCS data. This script will convert all CGCS data in a directory to a specified format.

将CGCS2000坐标系数据批量转换为WGS84坐标系数据的脚本。

## Usage

Download the latest release from the following link:

下载最新版本的脚本：
```
https://github.com/ElectricArc-Yu/CGCS-Simple-Batch-Converter/releases
```

Only the `CoordinateTransformer.zip` file is needed for use basic function.

使用功能只需下载CoordinateTransformer.zip文件即可。

Extract the zip file and run the 'CoordinateTransformer.exe` file.

解压缩zip文件并运行`CoordinateTransformer.exe`文件。

Based on the requirements, modify the configuration file `config.cfg`, move the original data to the `data` folder, and run the script.

根据需求更改配置文件`config.cfg`，并将原数据移动到`data`文件夹中，运行脚本即可。

## Configuration

The configuration file `config.cfg` is used to specify the input and output formats of the data.

配置文件`config.cfg`用于指定数据的输入和输出格式。

Do not modify the format of the configuration file, otherwise the script may not run properly.

请不要改动配置文件中的格式，否则可能会导致脚本无法正常运行。

### Supported Conversions

支持的转换如下：

The following conversions are supported:

- `CGCS2000` to `WGS84`

以下转换是支持的：

- `CGCS2000` 到 `WGS84`

### Supported Configurations

支持的配置如下：

The following configurations are supported:

- 是否输出高程 默认为True 输出与否均会保留高程列
- Output height or not, default is True and the height column will be retained regardless of the output
- 输出格式 CSV或者Excel 默认为CSV
-Output format, CSV or Excel, default is CSV
- 原数据文件位置 基于当前文件夹 (你也可以复制绝对路径，会自动识别文件夹下的所有csv和xlsx文件)
- Input file location, based on the current folder (you can also copy the absolute path, and all csv and xlsx files in the folder will be automatically recognized)
- 输出文件位置 基于当前文件夹 （你也可以复制绝对路径，但为防止覆盖数据，不允许指定文件名）
- Output file location, based on the current folder (you can also copy the absolute path, but to prevent data from being overwritten, specifying the file name is not allowed)
- 数据精确度
- Data accuracy

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.

这个项目是根据GPL-3.0许可证许可的 - 有关详细信息，请参阅[LICENSE](LICENSE)文件。

## Acknowledgments

这个项目主要使用了以下库：

This project mainly uses the following libraries:

- [pyproj](https://pyproj4.github.io/pyproj/stable/)
- [pandas](https://pandas.pydata.org/)
- [openpyxl](https://openpyxl.readthedocs.io/en/stable/)

## Contact

If you have any other functions or suggestions, please feel free to create a new issue.

如果您有任何其他功能或建议，请随时创建新Issue。

If you have any questions, please contact me at the following email address: yuchenhaoran@outlook.com

如果您有任何问题，请通过以下电子邮件地址与我联系：yuchenhaoran@outlook.com