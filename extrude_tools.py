from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism, BRepPrimAPI_MakeCylinder
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCC.Core.gp import gp_Vec, gp_Dir, gp_Pnt, gp_Ax2
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeSolid


def extrude_shape(shape, axis='Y', distance=100):
    from OCC.Core.Bnd import Bnd_Box
    from OCC.Core.BRepBndLib import brepbndlib
    from OCC.Core.gp import gp_Trsf, gp_Vec
    from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
    from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism

    # حساب حدود الشكل
    bbox = Bnd_Box()
    brepbndlib.Add(shape, bbox)
    xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()

    # نقل الشكل إلى (0,0,0)
    dx = -xmin
    dy = -ymin
    dz = -zmin
    trsf = gp_Trsf()
    trsf.SetTranslation(gp_Vec(dx, dy, dz))
    moved = BRepBuilderAPI_Transform(shape, trsf, True).Shape()

    # تنفيذ الإكسترود مباشرة
    if axis == "Y":
        vec = gp_Vec(0, distance, 0)
    elif axis == "Z":
        vec = gp_Vec(0, 0, distance)
    else:
        vec = gp_Vec(distance, 0, 0)

    prism = BRepPrimAPI_MakePrism(moved, vec).Shape()
    return prism

def add_hole(shape, x, y, z, dia, axis='Y'):
    if axis == "Y":
        dir_vec = gp_Dir(0,1,0)
    elif axis == "Z":
        dir_vec = gp_Dir(0,0,1)
    else:
        dir_vec = gp_Dir(1,0,0)
    height = 10000
    cyl = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(x,y,z), dir_vec), dia/2, height).Shape()
    new_shape = BRepAlgoAPI_Cut(shape, cyl).Shape()
    return new_shape

def preview_hole(x, y, z, dia, axis='Y'):
    if axis == "Y":
        dir_vec = gp_Dir(0,1,0)
    elif axis == "Z":
        dir_vec = gp_Dir(0,0,1)
    else:
        dir_vec = gp_Dir(1,0,0)
    height = 50
    cyl = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(x,y,z), dir_vec), dia/2, height).Shape()
    return cyl
