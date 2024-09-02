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
import xarray as xr
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


plt.rcParams['font.family'] = ['times new roman']   # 定义英文字体为新罗马
plt.rcParams["font.sans-serif"]=["SimHei"]          # 定义中文字体为宋体

def load_depth_ds(ncdir:str) -> np.array:
    """
        Description : load depth netCDF format dataset and mask land
        Input       : gebcco depth dataset directory
        output      : np array
    """
    ds         = xr.open_dataset(ncdir)
    depth      = ds['depth'].values
    depth      = depth.astype(np.float32)
    ll_bbox    = [
        ds['lon'].values[0], 
        ds['lon'].values[-1], 
        ds['lat'].values[0], 
        ds['lat'].values[-1]]

    mask         = generate_land_mask(ll_bbox, depth.shape)      # 生成陆地掩膜
    depth[mask]  = np.nan

    return depth

def main():
    # 设置常量
    DPI = 1200                                        # 分辨率
    SCATTER_SIZE = 15                                 # 散点大小
    SCATTER_LINEWIDTH = 0.5                           # 散点线宽
    LL_BBOX = [105, 125, 5, 25]                       # 经纬度边界
    PROJ = ccrs.PlateCarree()                         # 投影方式
    ROOT = os.path.dirname(os.path.abspath(__file__)) # 获取当前文件路径
    OUT  = "marineRsearch.png"                        # 输出文件名

    fig = plt.figure(dpi=DPI)
    
    ax:GeoAxes = fig.add_subplot(1,1,1,projection=PROJ)
    ax.set_extent(LL_BBOX,crs=ccrs.PlateCarree())       # 设置显示范围
    
    # 添加相关shp资料
    ax.coastlines(resolution='50m',linewidth=0.5, edgecolor='black',zorder=20)
    ax.add_feature(cfeat.BORDERS, linewidth=0.8, linestyle='-',zorder=20)
    ax.add_feature(cfeat.LAND, facecolor='gray', zorder=10)
    
    for _, value in shp_dir.items():
        ABS_DIR = os.path.join(ROOT, value['dir'])
        shp_var = cfeat.ShapelyFeature(
            Reader(ABS_DIR).geometries(),
            PROJ,
        )
        ax.add_feature(
            shp_var, 
            facecolor = value["facecolor"],
            edgecolor = value["edgecolor"],
            linewidth = value["linewidth"],
            linestyle = value["linestyle"],
            zorder    = value["zorder"],
        )
        del _, value
    
    # # 添加深度数据并获取经纬度范围
    depth = load_depth_ds(gebcco_dir["SCS"])
    hill_shade = hillshade(-depth,315,45)

    # # 添加自定义color map
    cmap = custom_cmap()

    # # 绘制深度图及深度梯度计算所得山体阴影
    cf = ax.imshow(
        depth,
        origin = 'lower',
        cmap = cmap,
        extent = LL_BBOX,
        transform = PROJ,
        vmin = -6000, vmax = 200,
        interpolation = 'nearest'
        )
    
    cd = ax.imshow(
        hill_shade,
        origin = 'lower',
        cmap = 'Greys_r',
        extent = LL_BBOX,
        transform = PROJ,
        alpha = 0.5,
        interpolation = 'nearest'
        )

    # 设定colorbar
    cbar = fig.colorbar(cf, 
        ax=ax, extend='both', 
        shrink=0.5, pad=0.1, 
        orientation='horizontal', 
        boundaries=np.linspace(-6000, 200, 13))
    cbar.ax.set_xlabel('Depth (m)',fontsize=8)
    cbar.ax.tick_params(labelsize=8)
    cbar.ax.yaxis.set_tick_params(labelsize=8)

    gl = ax.gridlines(crs=ccrs.PlateCarree(),
        draw_labels=True,
        linestyle='--',
        color='gray',
        linewidth=0.5,
        alpha=0.5,
        xlocs=np.arange(105,125,5),
        ylocs=np.arange(5,25,5)
        )
    ax._autoscaleXon = False
    ax._autoscaleYon = False
    gl.xlabels_top = False  
    gl.ylabels_right = False  
    gl.xlabel_style = {'size': 8, 'color': 'black'}
    gl.ylabel_style = {'size': 8, 'color': 'black'}

    # 绘制航次站点
    xlsx_files = glob(os.path.join(ROOT, "assets", "*.xlsx"))
    for idx, xlsx_file in enumerate(xlsx_files):
        section_name = xlsx_file.split("\\")[-1].split(".")[0]
        xlsx_table = pd.read_excel(xlsx_file, sheet_name=0)

        # 转为10分制
        xlsx_table['decimal_lon'] = xlsx_table['经度(度)'].dropna() + xlsx_table['经度(分)'].dropna() / 60
        xlsx_table['decimal_lat'] = xlsx_table['纬度(度)'].dropna() + xlsx_table['纬度(分)'].dropna() / 60

        # facecolor使用jet等额划分
        facecolor = plt.cm.jet((7-idx)/7)

        ax.scatter(
            xlsx_table['decimal_lon'],
            xlsx_table['decimal_lat'],
            color = facecolor,
            alpha = 0.8,
            edgecolors = 'black',
            s = SCATTER_SIZE,
            label = section_name,
            linewidth = SCATTER_LINEWIDTH,
            transform = PROJ
        )
    legend = ax.legend(
        loc='lower right',fontsize=5, ncol=1,
        )
    legend.set_zorder(25)
    plt.savefig(OUT, dpi=DPI, bbox_inches='tight')

if __name__ == "__main__":
    main()