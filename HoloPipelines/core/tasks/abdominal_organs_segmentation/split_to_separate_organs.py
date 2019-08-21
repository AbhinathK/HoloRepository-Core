"""
This module contains the functionality of the abdominal_organs_segmentation pipeline
of splitting the combined result into multiple sub-results.
"""

# TODO: Depending on how we deciide for this pipeline, this component may get removed.
# Otherwise, separate organs need to be merged again! (can also be in this task, which
# should then be renamed though)
# TODO: If we keep this, refactor and verify
# Refactoring should include only doing the OBJs in here, and transforming to GLB on
# pipeline level

import logging

import numpy as np

from core.adapters.glb_file import convert_obj_to_glb_and_write
from core.adapters.obj_file import write_mesh_as_obj
from core.services.marching_cubes import generate_mesh


def get_organ_name(hu_value: int):
    """
    Maps the "HU valuee" to the according organ name. Note that this is just an
    assumption. The paper (Automatic multi-organ segmentation on abdominal CT with
    dense v-networks https://doi.org/10.1109/TMI.2018.2806309) doesn't actually state
    the mapping. But it always uses this order, thus the assumption. Also, I manually
    compared outputs with Google image search :-) Note that 0 is how the authors
    encoded empty space around the organs.
    """
    organs = [
        None,
        "Spleen",
        "Left_Kidney",
        "Gallbladder",
        "Esophagus",
        "Liver",
        "Stomach",
        "Pancreas",
        "Duodenum",
    ]
    return organs[hu_value]


def split_to_separate_organs(input: np.ndarray, output_directory_path: str):
    logging.info("Separating different organs")
    # Each segmented organ has been masked with a unique "HU value"
    unique_hu_values = np.unique(input)

    # Value 0 is the empty space, remove
    unique_hu_values = unique_hu_values[1:]

    for hu_value in unique_hu_values:
        organ_name = get_organ_name(hu_value)
        logging.info(f"Processing organ: {organ_name} [{hu_value}]")
        organ_mask = input == hu_value
        organ_mask = organ_mask.astype(int)
        threshold = 0

        obj_output_path = f"{output_directory_path}/Organ_{hu_value}.obj"
        glb_output_path = f"{output_directory_path}/Organ_{hu_value}.glb"
        verts, faces, norm = generate_mesh(organ_mask, threshold)
        write_mesh_as_obj(verts, faces, norm, obj_output_path)

        convert_obj_to_glb_and_write(obj_output_path, glb_output_path)
