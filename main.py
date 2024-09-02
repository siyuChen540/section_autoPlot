# -*- encoding: utf-8 -*-
'''
@File        :  main.py
@Time        :  2024/8/27 23:16:00
@Author      :  chen siyu
@Mail        :  chensy57@mail2.sysu.edu.cn
@Version     :  1.0
@Description :  section plot of marine scientific research
@envName     :  nc_cartopy(laptop); geoDraw(pc)
'''

import warnings
from glob import glob
# 获取当前位置
import os
import sys
# current_dire = sys.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeat
from cartopy.mpl.geoaxes import GeoAxes

from param import *
from utils import *

warnings.filterwarnings(
    'ignore', 
    message='facecolor will have no effect as it has been defined as "never".'
)
warnings.filterwarnings(
    'ignore', 
    message='The .ylabels_right attribute is deprecated. Please'
)
warnings.filterwarnings(
    'ignore', 
    message='The .xlabels_top attribute is deprecated. Please'
)


plt.rcParams['font.family'] = ['times new roman']       # 定义英文字体为新罗马
plt.rcParams["font.sans-serif"]=["SimHei"]              # 定义中文字体为宋体


def main():
    # 设置常量
    DPI = 1200                                          # 分辨率
    SCATTER_SIZE = 15                                   # 散点大小
    SCATTER_LINEWIDTH = 0.5                             # 散点线宽
    SCATTER_ALPHA = 0.8                                 # 散点透明度

    LL_BBOX = [105, 125, 5, 25]                         # 经纬度边界
    PROJ = ccrs.PlateCarree()                           # 投影方式
    
    ROOT = os.path.dirname(os.path.abspath(__file__))   # 获取当前文件路径
    OUT  = "marineRsearch.png"                          # 输出文件名
    
    GRID_FONTSIZE = 8                                   # 网格字体大小
    LEGEND_FONTSIZE = 5                                 # 图例字体大小
    
    AZIMUTH = 315                                       # 光源方位角
    ALTITUDE = 45                                       # 光源高度角

    lon_min, lon_max, lat_min, lat_max = LL_BBOX        # 分取边界角点

    fig = plt.figure(dpi=DPI)
    
    ax:GeoAxes = fig.add_subplot(1,1,1,projection=PROJ)
    ax.set_extent(LL_BBOX,crs=ccrs.PlateCarree())       # 设置显示范围
    
    # 添加相关shp资料
    ax.coastlines(resolution='50m',linewidth=0.5, edgecolor='black',zorder=20)
    ax.add_feature(cfeat.BORDERS, linewidth=0.8, linestyle='-',zorder=20)
    ax.add_feature(cfeat.LAND, facecolor='gray', zorder=10)
    
    for _, value in shp_dir.items():
        ABS_DIR = os.path.join(ROOT, value['dir'])

        # 基于已定义的投影坐标系读取Shapfiles
        shp_var = cfeat.ShapelyFeature(
            Reader(ABS_DIR).geometries(),
            PROJ,
        )
        # 添加Shapfiles变量
        ax.add_feature(
            shp_var, 
            facecolor = value["facecolor"],
            edgecolor = value["edgecolor"],
            linewidth = value["linewidth"],
            linestyle = value["linestyle"],
            zorder    = value["zorder"],
        )
        del _, value
    
    # 添加深度数据并获取经纬度范围
    depth = load_depth_ds(gebcco_dir["SCS"])
    hill_shade = hillshade(-depth,AZIMUTH,ALTITUDE)

    # 添加自定义color map
    cmap = custom_cmap()

    # 绘制深度图及深度梯度计算所得山体阴影
    cf = ax.imshow(
        depth,
        origin = 'lower',
        cmap = cmap,
        extent = LL_BBOX,
        transform = PROJ,
        vmin = -6000, vmax = 200,
        interpolation = 'nearest'
        )
    
    ax.imshow(
        hill_shade,
        origin = 'lower',
        cmap = 'Greys_r',
        extent = LL_BBOX,
        transform = PROJ,
        alpha = 0.5,
        interpolation = 'nearest'
        )

    # 设定colorbar
    cbar = fig.colorbar(
        cf, ax = ax, 
        extend = 'both', 
        shrink = 0.5, 
        pad = 0.1, 
        orientation = 'horizontal', 
        boundaries = np.linspace(-6000, 200, 13))
    cbar.ax.set_xlabel('Depth (m)', fontsize = GRID_FONTSIZE)
    cbar.ax.tick_params(labelsize = GRID_FONTSIZE)
    cbar.ax.yaxis.set_tick_params(labelsize = GRID_FONTSIZE)

    gl = ax.gridlines(crs=ccrs.PlateCarree(),
        draw_labels=True,
        linestyle='--',
        color='gray',
        linewidth=0.5,
        alpha=0.5,
        xlocs=np.arange(lon_min,lon_max,5),
        ylocs=np.arange(lat_min,lat_max,5)
        )
    
    ax._autoscaleXon = False
    ax._autoscaleYon = False
    gl.xlabels_top   = False  
    gl.ylabels_right = False  
    gl.xlabel_style  = {'size': GRID_FONTSIZE, 'color': 'black'}
    gl.ylabel_style  = {'size': GRID_FONTSIZE, 'color': 'black'}

    # 绘制航次站点
    files = glob(os.path.join(ROOT, "assets", "*.xlsx"))
    for idx, file in enumerate(files):
        section_name = file.split("\\")[-1].split(".")[0]
        ds = pd.read_excel(file, sheet_name=0)

        # 转为10分制
        try:
            ds['decimal_lon'] = ds['经度(度)'].dropna() + ds['经度(分)'].dropna() / 60
            ds['decimal_lat'] = ds['纬度(度)'].dropna() + ds['纬度(分)'].dropna() / 60
        except:
            raise NameError, "excel文件经纬度数据列名错误"
        
        # facecolor使用jet等额划分
        facecolor = plt.cm.jet((len(files) - idx) / len(files))

        ax.scatter(
            ds['decimal_lon'],
            ds['decimal_lat'],
            color = facecolor,
            alpha = SCATTER_ALPHA,
            edgecolors = 'black',
            s = SCATTER_SIZE,
            label = section_name,
            linewidth = SCATTER_LINEWIDTH,
            transform = PROJ
        )
    legend = ax.legend(
        loc = 'lower right', fontsize = LEGEND_FONTSIZE, ncol = 1,
        )
    legend.set_zorder(25)
    plt.savefig(OUT, dpi = DPI, bbox_inches = 'tight')

if __name__ == "__main__":
    main()