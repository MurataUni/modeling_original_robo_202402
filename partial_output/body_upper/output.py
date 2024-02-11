import sys
sys.dont_write_bytecode = True

from harbor3d import Dock, Shipwright
import os

from harbor3d.util.bone_json_util import PostureWrapper, BoneKeys
from harbor3d.util.json_util import JsonLoader

sys.path.append(os.sep.join(os.path.dirname(os.path.abspath(__file__)).split(os.sep)[:-2]))
from path_info import Const as PathInfo
from spec_model import Const

def main():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    fname = path.split(os.sep)[-1] + '.stl'
    posture = os.path.join(PathInfo.dir_posture_json, PathInfo.file_posture_model_posed)
    target_name = "body_upper"

    sw = Shipwright(Dock())

    json_loader = JsonLoader(posture)
    pw = PostureWrapper(json_loader.fetch())
    del pw.postures["elbow_root_l"], pw.postures["elbow_root_r"]

    pw.remove_rotation(target_name)
    objects, scale = sw.load_bones(pw, target_name)
    sw.load_submodules_name_match(objects, [PathInfo.dir_parts_renamed], {})

    sw.generate_stl_binary(path, fname=fname, concatinated=False)

if __name__ == "__main__":
    main()