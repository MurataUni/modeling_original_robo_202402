import sys
sys.dont_write_bytecode = True

import numpy as np
import os

from harbor3d.util.bone_json_util import PostureWrapper
from harbor3d.util.json_util import JsonLoader

from path_info import Const as PathInfo

class Const:

    bone_default_len = 0.1
    bone_default_len_small = 0.01

    bones_relationship = {
        "base": None,
        "body_lower": "base", # parts body lower
        "body_spine_lower": "body_lower",
        "body_spine_internal": "body_spine_lower",
        "body_spine_upper": "body_spine_internal",
        "body_upper": "body_spine_upper", # parts body upper
        "neck": "body_upper",
        "head": "neck",
        "eye_sub_left_inner": "head",
        "eye_sub_left_outer": "head",
        "eye_sub_right_inner": "head",
        "eye_sub_right_outer": "head",
        "eye_main_left": "head",
        "eye_main_right": "head",
        "shoulder_base_l": "body_upper", # parts arm left
        "shoulder_l": "shoulder_base_l",
        "shoulder_base_l_rod_1": "shoulder_base_l",
        "shoulder_base_l_rod_2": "shoulder_base_l",
        "shoulder_base_l_rod_3": "shoulder_base_l",
        "upper_arm_l": "shoulder_l",
        "elbow_root_l": "upper_arm_l",
        "elbow_end_l": "elbow_root_l",
        "forearm_l": "elbow_end_l",
        "wrist_l": "forearm_l",
        "palm_l": "wrist_l",
        "palm_l_padding": "palm_l",
        "shoulder_base_r": "body_upper", # parts arm right
        "shoulder_r": "shoulder_base_r",
        "shoulder_base_r_rod_1": "shoulder_base_r",
        "shoulder_base_r_rod_2": "shoulder_base_r",
        "shoulder_base_r_rod_3": "shoulder_base_r",
        "upper_arm_r": "shoulder_r",
        "elbow_root_r": "upper_arm_r",
        "elbow_end_r": "elbow_root_r",
        "forearm_r": "elbow_end_r",
        "wrist_r": "forearm_r",
        "palm_r": "wrist_r",
        "palm_r_padding": "palm_r",
        "coxa_joint_l": "body_lower", # parts leg left
        "thigh_base_l": "coxa_joint_l",
        "thigh_l": "thigh_base_l",
        "shin_l": "thigh_l",
        "foot_l": "shin_l",
        "toe_l": "foot_l",
        "coxa_joint_r": "body_lower", # parts leg right
        "thigh_base_r": "coxa_joint_r",
        "thigh_r": "thigh_base_r",
        "shin_r": "thigh_r",
        "foot_r": "shin_r",
        "toe_r": "foot_r",
        "thumb_proximal_phalanx_l": "palm_l", # parts hand left
        "thumb_distal_phalanx_l": "thumb_proximal_phalanx_l",
        "index_f_proximal_phalanx_l": "palm_l",
        "index_f_middle_phalanx_l": "index_f_proximal_phalanx_l",
        "index_f_distal_phalanx_l": "index_f_middle_phalanx_l",
        "middle_f_proximal_phalanx_l": "palm_l",
        "middle_f_middle_phalanx_l": "middle_f_proximal_phalanx_l",
        "middle_f_distal_phalanx_l": "middle_f_middle_phalanx_l",
        "ring_f_proximal_phalanx_l": "palm_l",
        "ring_f_middle_phalanx_l": "ring_f_proximal_phalanx_l",
        "ring_f_distal_phalanx_l": "ring_f_middle_phalanx_l",
        "little_f_proximal_phalanx_l": "palm_l",
        "little_f_middle_phalanx_l": "little_f_proximal_phalanx_l",
        "little_f_distal_phalanx_l": "little_f_middle_phalanx_l",
        "thumb_proximal_phalanx_r": "palm_r", # parts hand right
        "thumb_distal_phalanx_r": "thumb_proximal_phalanx_r",
        "index_f_proximal_phalanx_r": "palm_r",
        "index_f_middle_phalanx_r": "index_f_proximal_phalanx_r",
        "index_f_distal_phalanx_r": "index_f_middle_phalanx_r",
        "middle_f_proximal_phalanx_r": "palm_r",
        "middle_f_middle_phalanx_r": "middle_f_proximal_phalanx_r",
        "middle_f_distal_phalanx_r": "middle_f_middle_phalanx_r",
        "ring_f_proximal_phalanx_r": "palm_r",
        "ring_f_middle_phalanx_r": "ring_f_proximal_phalanx_r",
        "ring_f_distal_phalanx_r": "ring_f_middle_phalanx_r",
        "little_f_proximal_phalanx_r": "palm_r",
        "little_f_middle_phalanx_r": "little_f_proximal_phalanx_r",
        "little_f_distal_phalanx_r": "little_f_middle_phalanx_r",
        "weapon_r": "palm_r", # parts weapon right
    }

    bones = bones_relationship.keys()

    alias = {
        "body_spine_lower": "body_spine", # parts body lower
        "body_spine_internal": "body_spine",
        "body_spine_upper": "body_spine",
        "eye_main_left": "eye_main",# parts body upper
        "eye_main_right": "eye_main",
        "eye_sub_left_inner": "eye_sub",
        "eye_sub_left_outer": "eye_sub",
        "eye_sub_right_inner": "eye_sub",
        "eye_sub_right_outer": "eye_sub",
        "shoulder_base_l_rod_1": "shoulder_base_rod",# parts arm left
        "shoulder_base_l_rod_2": "shoulder_base_rod",
        "shoulder_base_l_rod_3": "shoulder_base_rod",
        "wrist_l": "wrist",
        "shoulder_base_r_rod_1": "shoulder_base_rod",# parts arm right
        "shoulder_base_r_rod_2": "shoulder_base_rod",
        "shoulder_base_r_rod_3": "shoulder_base_rod",
        "wrist_r": "wrist",
        "thumb_proximal_phalanx_l": "thumb_proximal_phalanx", # parts hand left
        "thumb_distal_phalanx_l": "thumb_distal_phalanx",
        "index_f_proximal_phalanx_l": "f_proximal_phalanx",
        "index_f_middle_phalanx_l": "f_middle_phalanx",
        "index_f_distal_phalanx_l": "f_distal_phalanx",
        "middle_f_proximal_phalanx_l": "f_proximal_phalanx",
        "middle_f_middle_phalanx_l": "f_middle_phalanx",
        "middle_f_distal_phalanx_l": "f_distal_phalanx",
        "ring_f_proximal_phalanx_l": "f_proximal_phalanx",
        "ring_f_middle_phalanx_l": "f_middle_phalanx",
        "ring_f_distal_phalanx_l": "f_distal_phalanx",
        "little_f_proximal_phalanx_l": "f_proximal_phalanx",
        "little_f_middle_phalanx_l": "f_middle_phalanx",
        "little_f_distal_phalanx_l": "f_distal_phalanx",
        "thumb_proximal_phalanx_r": "thumb_proximal_phalanx", # parts hand right
        "thumb_distal_phalanx_r": "thumb_distal_phalanx",
        "index_f_proximal_phalanx_r": "f_proximal_phalanx",
        "index_f_middle_phalanx_r": "f_middle_phalanx",
        "index_f_distal_phalanx_r": "f_distal_phalanx",
        "middle_f_proximal_phalanx_r": "f_proximal_phalanx",
        "middle_f_middle_phalanx_r": "f_middle_phalanx",
        "middle_f_distal_phalanx_r": "f_distal_phalanx",
        "ring_f_proximal_phalanx_r": "f_proximal_phalanx",
        "ring_f_middle_phalanx_r": "f_middle_phalanx",
        "ring_f_distal_phalanx_r": "f_distal_phalanx",
        "little_f_proximal_phalanx_r": "f_proximal_phalanx",
        "little_f_middle_phalanx_r": "f_middle_phalanx",
        "little_f_distal_phalanx_r": "f_distal_phalanx",
    }

    alias_parts_premerged = {
        "body_spine_lower": "body_spine", # parts body lower
        "body_spine_internal": "body_spine",
        "body_spine_upper": "body_spine",
        "eye_main_left": "eye_main",# parts body upper
        "eye_main_right": "eye_main",
        "eye_sub_left_inner": "eye_sub",
        "eye_sub_left_outer": "eye_sub",
        "eye_sub_right_inner": "eye_sub",
        "eye_sub_right_outer": "eye_sub",
        "shoulder_base_l_rod_1": "shoulder_base_rod",# parts arm left
        "shoulder_base_l_rod_2": "shoulder_base_rod",
        "shoulder_base_l_rod_3": "shoulder_base_rod",
        "wrist_l": "wrist",
        "palm_l": "palm_and_finger_l",
        "palm_l_padding": "none",
        "shoulder_base_r_rod_1": "shoulder_base_rod",# parts arm right
        "shoulder_base_r_rod_2": "shoulder_base_rod",
        "shoulder_base_r_rod_3": "shoulder_base_rod",
        "wrist_r": "wrist",
        "palm_r": "palm_and_finger_r",
        "palm_r_padding": "none",
        "thumb_proximal_phalanx_l": "none", # parts hand left
        "thumb_distal_phalanx_l": "none",
        "index_f_proximal_phalanx_l": "none",
        "index_f_middle_phalanx_l": "none",
        "index_f_distal_phalanx_l": "none",
        "middle_f_proximal_phalanx_l": "none",
        "middle_f_middle_phalanx_l": "none",
        "middle_f_distal_phalanx_l": "none",
        "ring_f_proximal_phalanx_l": "none",
        "ring_f_middle_phalanx_l": "none",
        "ring_f_distal_phalanx_l": "none",
        "little_f_proximal_phalanx_l": "none",
        "little_f_middle_phalanx_l": "none",
        "little_f_distal_phalanx_l": "none",
        "thumb_proximal_phalanx_r": "none", # parts hand right
        "thumb_distal_phalanx_r": "none",
        "index_f_proximal_phalanx_r": "none",
        "index_f_middle_phalanx_r": "none",
        "index_f_distal_phalanx_r": "none",
        "middle_f_proximal_phalanx_r": "none",
        "middle_f_middle_phalanx_r": "none",
        "middle_f_distal_phalanx_r": "none",
        "ring_f_proximal_phalanx_r": "none",
        "ring_f_middle_phalanx_r": "none",
        "ring_f_distal_phalanx_r": "none",
        "little_f_proximal_phalanx_r": "none",
        "little_f_middle_phalanx_r": "none",
        "little_f_distal_phalanx_r": "none",
    }

    parts_reverse = {
        "shoulder_base_r": "shoulder_base_l", # parts arm right
        "shoulder_r": "shoulder_l",
        "upper_arm_r": "upper_arm_l",
        "elbow_root_r": "elbow_root_l",
        "elbow_end_r": "elbow_end_l",
        "forearm_r": "forearm_l",
        "palm_r": "palm_l",
        "coxa_joint_r": "coxa_joint_l", # parts leg right
        "thigh_base_r": "thigh_base_l",
        "thigh_r": "thigh_l",
        "shin_r": "shin_l",
        "foot_r": "foot_l",
        "toe_r": "toe_l",
    }

    bones_short = [
        "base",
        "thumb_proximal_phalanx_r",
        "thumb_distal_phalanx_l",
        "first_f_proximal_phalanx_l",
        "first_f_middle_phalanx_l",
        "first_f_distal_phalanx_l",
        "second_f_proximal_phalanx_l",
        "second_f_middle_phalanx_l",
        "second_f_distal_phalanx_l",
        "third_f_proximal_phalanx_l",
        "third_f_middle_phalanx_l",
        "third_f_distal_phalanx_l",
        "thumb_proximal_phalanx_r",
        "thumb_distal_phalanx_r",
        "first_f_proximal_phalanx_r",
        "first_f_middle_phalanx_r",
        "first_f_distal_phalanx_r",
        "second_f_proximal_phalanx_r",
        "second_f_middle_phalanx_r",
        "second_f_distal_phalanx_r",
        "third_f_proximal_phalanx_r",
        "third_f_middle_phalanx_r",
        "third_f_distal_phalanx_r",
    ]

def main():
    fnames = [PathInfo.file_posture_model_default, PathInfo.file_posture_model_posed]
    for fname in fnames:
        apply_const(os.path.join(PathInfo.dir_posture_json,fname))

def apply_const(posture_file):
    json_loader = JsonLoader(posture_file)
    pw = PostureWrapper(json_loader.fetch())
    for key in Const.bones:
        length = Const.bone_default_len
        if key in Const.bones_short:
            length = Const.bone_default_len_small
        
        if pw.has_key(key):
            pw.set_length(key, length)
        else:
            pw.add_bone(key, Const.bones_relationship[key], length)

    json_loader.dictionary = pw.postures
    json_loader.dump()
    
if __name__ == "__main__":
    main()
