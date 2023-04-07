# -*- coding: utf-8 -*-
from pathlib import Path

_path = Path(__file__)
root = str(_path.parent.parent.parent.absolute()) + '/'
root_model = root + "models/"
root_resource = root + "resources/"
root_record = root + "records/"
