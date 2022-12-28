import pandas as pd
from plotly.basedatatypes import BasePlotlyType
from plotly.graph_objs import Figure
from .plots import process_plotly_xml
from .tables import process_xml_pandas


def process_confluence_template_args(kwargs):
    image_list = []
    modified_kwargs = {}
    for k, v in kwargs.items():
        if isinstance(v, pd.DataFrame):
            modified_kwargs[k] = process_xml_pandas(v)
        elif isinstance(v, (BasePlotlyType, Figure)):
            item = process_plotly_xml(v, k)
            modified_kwargs[k] = item["xml"]
            image_list.append(item["image"])
        else:
            modified_kwargs[k] = v
    return modified_kwargs, image_list
