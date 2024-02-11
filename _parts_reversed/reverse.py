import sys
sys.dont_write_bytecode = True

from harbor3d import Dock, Shipwright
import os

sys.path.append(os.sep.join(os.path.dirname(os.path.abspath(__file__)).split(os.sep)[:-1]))
from path_info import Const as PathInfo
from spec_model import Const

def main():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    fname = ''

    sw = Shipwright(Dock())

    for key, item in Const.parts_reverse.items():
        target = sw.search_and_load_stl(PathInfo.dirs_parts_modeling, item + ".stl")
        if target == None:
            continue
        else:
            target.name = key

    sw.deformation_all(lambda x,y,z: (-x,y,z))
    for ship in sw.dock.ships:
        if ship.is_monocoque():
            for triangle in ship.monocoque_shell.triangles:
                triangle.inverse()

    sw.generate_stl_binary(path, fname, concatinated=False, divided=True)

if __name__ == "__main__":
    main()