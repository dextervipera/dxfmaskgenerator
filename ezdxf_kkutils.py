def ezdxf_coords2rect(coords, size=None) -> list:
    if size:
        x0 = coords[0]
        y0 = coords[1]
        if type(size) in [list, tuple]:
            dx = size[0]
            dy = size[1]
        else:
            dx = dy = size;
        return [(x0, y0), (x0+dx, y0), (x0+dx, y0+dy), (x0, y0+dy), (x0, y0)]
    else:
        x0 = coords[0]
        y0 = coords[1]		
        x1 = coords[2]
        y1 = coords[3]
        return [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]