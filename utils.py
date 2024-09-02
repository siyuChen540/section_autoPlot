# -*- encoding: utf-8 -*-
'''
@File        :  utils.py
@Time        :  2024/8/27 23:16:00
@Author      :  chen siyu
@Mail        :  chensy57@mail2.sysu.edu.cn
@Version     :  1.0
@Description :  section plot of marine scientific research
@envName     :  nc_cartopy(laptop); geoDraw(pc)
'''


import numpy as np
import xarray as xr

from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature


def custom_cmap():
    colors = [
        (127/255, 0, 0),                # dark red
        (168/255, 0, 0),                # red
        (207/255, 24/255, 0),           # red orange
        (241/255, 88/255, 0),           # orange
        (255/255, 118/255, 0),          # orange
        (255/255, 158/255, 0),          # orange
        (255/255, 194/255, 0),          # yellow
        (232/255, 217/255, 36/255),     # yellow
        (181/255, 202/255, 43/255),     # yellow green
        (123/255, 180/255, 62/255),     # green
        (68/255, 162/255, 96/255),      # green
        (0, 126/255, 137/255),          # green
        (0, 77/255, 217/255),           # blue
        (0/255, 42/255, 235/255),       # blue
        (0/255, 14/255, 217/255),       # blue
        (8/255, 77/255, 152/255),       # blue
        (204/255, 223/255, 241/255)     # light blue
    ]
    from matplotlib.colors import ListedColormap
    cmap = ListedColormap(colors)
    return cmap

def hillshade(array,azimuth,angle_altitude):
    """
    Decsription: generate hillshade
    Function:
        $$山体阴影 = 255.0 * (( cos(zenith_I)*cos(slope_T))+(sin(zenith_I)*sin(slope_T)*cos(azimuth_I-aspect_T))$$
    Help:
        http://webhelp.esri.com/arcgisdesktop/9.2/index.cfm?TopicName=How%20Hillshade%20works.
    Input:
        array: elevation array
        azimuth: azimuth
        angle_altitude: angle_altitude
    Output:
        shaded: hillshade
    example:
        shaded = hillshade(array, 315, 45)
        plt.imshow(array, cmap='terrain', vmin=-6000, vmax=200)
        plt.imshow(shaded, cmap='gray',alpha=0.5)
    """
    azimuth = 360.0 - azimuth 
    
    x, y = np.gradient(array)
    slope = np.pi/2. - np.arctan(np.sqrt(x*x + y*y))
    aspect = np.arctan2(-x, y)
    azimuthrad = azimuth*np.pi/180.
    altituderad = angle_altitude*np.pi/180.
 
    shaded = np.sin(altituderad)*np.sin(slope) + np.cos(altituderad)*np.cos(slope)*np.cos((azimuthrad - np.pi/2.) - aspect)
    
    return 255*(shaded + 1)/2

def generate_land_mask(ll_bbox, shape):
    """
    Description: generate land mask by longitude and latitude border box
    Input:
        ll_bbox: [lon_min, lon_max, lat_min, lat_max]
        shape: (lat_length, lon_length)
    Output:
        land_mask: land mask
    """
    from global_land_mask import globe

    lon_ = np.linspace(
        start=ll_bbox[0],
        stop=ll_bbox[1],
        num=shape[1]
    )
    lat_ = np.linspace(
        start=ll_bbox[2],
        stop=ll_bbox[3],
        num=shape[0]
    )
    lons, lats = np.meshgrid(lon_, lat_)
    land_mask = globe.is_land(lats, lons)
    return land_mask

def cal_center(ll_bbox):
    """
    Description: calculate center coordinate from longitute latitude border box
    Input:
        ll_bbox: [lon_min, lon_max, lat_min, lat_max]
    Output:
        center: (lon, lat)
    """
    center = ((ll_bbox[0]+ll_bbox[1])/2, (ll_bbox[2]+ll_bbox[3])/2)
    return center

def generate_rectangle(ll_bbox:list,edgecolor:str='k',zorder:int=1):
    """
    Description: generate a matplotlib.patches.Rectangle object
    The rectangle extends from ``xy[0]`` to ``xy[0] + width`` in x-direction
    and from ``xy[1]`` to ``xy[1] + height`` in y-direction. ::
    
      :                +------------------+
      :                |                  |
      :              height               |
      :                |                  |
      :               (xy)---- width -----+
    
    Input:
        ll_bbox: [lon_min, lon_max, lat_min, lat_max]
        edgecolor: edge color
        zorder: zorder
    Output:
        rect: matplotlib.patches.Rectangle object
    """
    from matplotlib.patches import Rectangle
    
    xy = (ll_bbox[0],ll_bbox[2])
    width = ll_bbox[1]-ll_bbox[0]
    height = ll_bbox[3]-ll_bbox[2]
    
    rect = Rectangle(
                xy,width,height,
                linewidth=1,
                edgecolor=edgecolor,
                facecolor='none',
                zorder=zorder
            )
    return rect


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

def logit_cut(lon_array:np.ndarray, lat_array:np.ndarray, cut_array:np.ndarray, LL_BBOX:list) -> np.ndarray:
    """
        Description: cut the array by longitude and latitude, 
        LL_BBOX is the target longitude and latitude range::

            :          +----------------(lon_max, lat_max)
            :          |                         |
            :         lat                        |
            :          |                         |
            : (lon_min, lat_min)------ lon ------+
        
        Input:
            lon_array: longitude array
            lat_array: latitude array
            cut_array: array to be cut
            LL_BBOX: [lon_min, lon_max, lat_min, lat_max]
    
        Output:
            col_row_cut: cut array
    """
    lon_min, lon_max, lat_min, lat_max = LL_BBOX

    lat_bool:bool = (lat_array > lat_min) & (lat_array < lat_max)
    lon_bool:bool = (lon_array > lon_min) & (lon_array < lon_max)
    
    row_cut:np.ndarray = cut_array[lat_bool]
    col_cut:np.ndarray = row_cut[:, lon_bool]
    return col_cut