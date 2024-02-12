import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from matplotlib.lines import Line2D
from datetime import datetime
import ezdxf

_project = 'magmasks'
_version = '1'
_sub_version = '0'
_revision = '0'
_date = str(datetime.now().date())


def _infolabel():
    return f"[{_date}]{_project}-V{_version}.{_sub_version}.r{_revision}"


def give_me_mask(config: dict, filename: str):
    """
    Gets configuration dictionary and saves a plot and dxf file
    """
    spike_ystart = -config['spike_height']/2
    spike_yend = config['spike_height']/2
    spike_raster = (config['spike_width']+config['spike_sep_v'])*2
    spike_width = config.get('spike_width')
    spike_sep_v = config.get('spike_sep_v')
    snake_width = spike_raster * config.get('spike_count')
    spike_count = config.get('spike_count')
    spike_sep_h = config.get('spike_sep_h')
    spike_support = config.get('spike_support')
    pad_width = config.get('pad_width')
    pad_height = config.get('pad_height')
    border_x = config.get('mask_width')/2
    border_y = config.get('mask_height')/2
    
    
    mask = ezdxf.new("R2000", setup=True)
    mask_model = mask.modelspace()
    prev_fig = plt.figure()
    pax = prev_fig.add_axes([.1,.1,.8,.8])

    def add_line(x0, y0, x1, y1, color='red', lw=0.9):
        mask_model.add_line((x0,y0),(x1, y1))
        l1 = Line2D([x0,x1],[y0,y1], color=color, lw=lw)
        pax.add_line(l1)
        
        l2 = Line2D([-x0,-x1],[-y0,-y1], color=color, lw=lw)
        mask_model.add_line((-x0,-y0),(-x1, -y1))
        pax.add_line(l2)

    def add_spike(x0,y0,y1, **kwargs):
        color = kwargs.get('color', 'black')
        add_line(x0-spike_width/2, y0, x0-spike_width/2, y1, color=color)
        add_line(x0+spike_width/2, y0, x0+spike_width/2, y1, color=color)
        add_line(x0-spike_width/2, y1, x0+spike_width/2, y1, color=color)
        add_line(x0+spike_width/2, y0, x0+spike_raster/2, y0, color=color)
        add_line(x0-spike_width/2, y0, x0-spike_raster/2, y0, color=color)
    
    
    
    for spike in range(config['spike_count']):
        n_spike = spike-config['spike_count']/2
        x_spike = n_spike*spike_raster+0.25*spike_raster
        
        add_spike(x0=x_spike+spike_raster/2,
                  y0=spike_ystart,
                  y1=spike_yend-spike_sep_v,
                  color='blue')
    
    spike_xstart = (spike_count-0)/2*spike_raster+0.25*spike_raster
    add_line(spike_xstart, spike_ystart, spike_xstart, spike_ystart-spike_support, color='green')
    add_line(pad_width/2, spike_ystart-spike_support, spike_xstart, spike_ystart-spike_support, color='green')
    add_line(pad_width/2, spike_ystart-spike_support, pad_width/2, spike_ystart-spike_support-pad_height, color='green')
    add_line(pad_width/2, spike_ystart-spike_support-pad_height, -pad_width/2, spike_ystart-spike_support-pad_height, color='green')
    add_line(-pad_width/2, spike_ystart-spike_support, -pad_width/2, spike_ystart-spike_support-pad_height, color='green')
    add_line(-pad_width/2, spike_ystart-spike_support, -spike_xstart, spike_ystart-spike_support, color='green')
    add_line(-spike_xstart, spike_ystart, -spike_xstart, spike_ystart-spike_support, color='green')
    add_line(-spike_xstart, spike_ystart, -spike_xstart+spike_raster/2, spike_ystart, color='green')
    
    add_line(-border_x, -border_y, border_x, -border_y, color='olive')
    add_line(border_x, -border_y, border_x, border_y, color='olive')
    
    pax.set_xlim([-border_x*1.1, border_x*1.1])
    pax.set_ylim([-border_y*1.1, border_y*1.1])
    pax.set_xlabel('x [mm]')
    pax.set_ylabel('y [mm]')
    pax.set_aspect('equal', 'box')
    pax.grid()
    
    prev_fig.savefig(f"results/{_infolabel()}_{filename}.png", bbox_inches = 'tight')
    mask.saveas(f'results/{_infolabel()}_{filename}.dxf')
    return prev_fig, pax