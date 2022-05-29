from elements.elementsTypes import *

"""
Notes
COLORS:
rgb(210,213,73) (yellow)
rgb(102,102,109) (grey)
"""

class Settings:
    part_root = 'root/part'
    json_part_root = 'part'

    # part model path for every use
    part_model_path = 'backend/appData/partModels/default_part_model.xml'

    # property to filter in dropbox of filterWidget
    filter_dropdown_types = 'part/general_information/type'

    color_palette = {
        'TF-colors': {
            'yellow': 'TO DO HEX -> RGB'
        }
    }

    # --- STORE VIEWER SETTINGS -----
    move_click_offset = 500
    zoom_click_offset = 500


    # ----- STORE SETTINGS -----
    store_object_max_height = 1000


    # ----- SHELVES SETTINGS -----
    default_shelf_net_height = 10   # cm

    # ----- CONTAINER SETTINGS -----
    containers = [BIN, SPACE_CONTAINER]
    custom_containers = [SPACE_CONTAINER]
    bin_weight_capacity = 45    # kg

