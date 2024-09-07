# -*- encoding: utf-8 -*-
'''
@File        :  param.py
@Time        :  2024/8/27 23:16:00
@Author      :  chen siyu
@Mail        :  chensy57@mail2.sysu.edu.cn
@Version     :  1.0
@Description :  parameter
@envName     :  nc_cartopy(laptop); geoDraw(pc)
'''

table_dir:str = r"assets/*.xlsx"

shp_dir:dict = {
    "city"      : {
        "dir"       : r"assets/shp/City/CN_city.shp",
        "facecolor" : 'none',
        "edgecolor" : 'black',
        "linewidth" : 0.1,
        "linestyle" : '--',
        "zorder"    : 20
    },
    "river3"    : {
        "dir"       : r"assets/shp/R3/hyd2_4p.shp",
        "facecolor" : 'none',
        "edgecolor" : 'black',
        "linewidth" : 0.1,
        "linestyle" : '--',
        "zorder"    : 20
        },
    "river5"    : {
        "dir"       : r"assets/shp/R5/River5_polyline.shp",
        "facecolor" : None,
        "edgecolor" : None,
        "linewidth" : 1,
        "linestyle" : '-',
        "zorder"    : 20
        },
    "nineline"  : {
        "dir"       : r"assets/shp/SouthSea/nineline.shp",
        "facecolor" : None,
        "edgecolor" : 'black',
        "linewidth" : 1,
        "linestyle" : '-',
        "zorder"    : 20
        },
    "islands"   : {
        "dir"       : r"assets/shp/SouthSea/islands.shp",
        "facecolor" : None,
        "edgecolor" : 'black',
        "linewidth" : 0.01,
        "linestyle" : '-',
        "zorder"    : 20
        },
    # "bou2_4l"   : {
    #     "dir"       : r"assets/shp/SouthSea/bou2_4l.shp",
    #     "facecolor" : None,
    #     "edgecolor" : 'black',
    #     "linewidth" : 1,
    #     "linestyle" : '-',
    #     "zorder"    : 20
    #     },
    "zhujiang"  : {
        "dir"       : r"assets/shp/SouthSea/zhujiang.shp",
        "facecolor" : 'blue',
        "edgecolor" : 'deepblue',
        "linewidth" : 1,
        "linestyle" : '-',
        "zorder"    : 20
        }
}

gebcco_dir:dict = {
    "SCS":r"assets/bathymetry/GEBCO_2022_105_125_5_25.nc"
}