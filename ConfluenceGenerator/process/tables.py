from ..utils import *


def _process_xml_visual_input(visual_input, row_length):
    if isinstance(visual_input, (list, tuple)):
        if len(visual_input) != row_length:
            raise ValueError("visual_input must be the same length as row_length")
        return visual_input
    else:
        return row_length * [visual_input]


def create_xml_table(
    value_matrix,
    cell_colour_matrix=COLOUR.white,
    text_colour_matrix=COLOUR.black,
    bold_matrix=False,
    italic_matrix=False,
    text_align_matrix="center",
):

    row_length = len(value_matrix)
    cell_colour_matrix = _process_xml_visual_input(cell_colour_matrix, row_length)
    text_colour_matrix = _process_xml_visual_input(text_colour_matrix, row_length)
    bold_matrix = _process_xml_visual_input(bold_matrix, row_length)
    italic_matrix = _process_xml_visual_input(italic_matrix, row_length)
    text_align_matrix = _process_xml_visual_input(text_align_matrix, row_length)

    xml_table_rows = "".join(
        [
            create_xml_table_row(
                value_list,
                cell_colour_list,
                text_colour_list,
                bold_list,
                italic_list,
                text_align_list,
            )
            for value_list, cell_colour_list, text_colour_list, bold_list, italic_list, text_align_list in zip(
                value_matrix,
                cell_colour_matrix,
                text_colour_matrix,
                bold_matrix,
                italic_matrix,
                text_align_matrix,
            )
        ]
    )

    table_xml = f"""
    <table data-layout="wide">
    <tbody>
    {xml_table_rows}
    </tbody>
    </table>
    """
    return table_xml


def create_xml_table_row(
    value_list,
    cell_colour_list=COLOUR.white,
    text_colour_list=COLOUR.black,
    bold_list=False,
    italic_list=False,
    text_align_list="center",
):
    row_length = len(value_list)

    cell_colour_list = _process_xml_visual_input(cell_colour_list, row_length)
    text_colour_list = _process_xml_visual_input(text_colour_list, row_length)
    bold_list = _process_xml_visual_input(bold_list, row_length)
    italic_list = _process_xml_visual_input(italic_list, row_length)
    text_align_list = _process_xml_visual_input(text_align_list, row_length)

    row_value_list = [
        get_xml_table_value(value, cell_colour, text_colour, bold, italic, text_align)
        for value, cell_colour, text_colour, bold, italic, text_align in zip(
            value_list,
            cell_colour_list,
            text_colour_list,
            bold_list,
            italic_list,
            text_align_list,
        )
    ]

    return f"""<tr>
    {"".join(row_value_list)}
    </tr>"""


def get_xml_table_value(
    value,
    cell_colour=COLOUR.white,
    text_colour=COLOUR.black,
    bold=False,
    italic=False,
    text_align="center",
):
    BOLD_START = "<strong>" if bold else ""
    BOLD_END = "</strong>" if bold else ""

    ITALIC_START = "<em>" if italic else ""
    ITALIC_END = "</em>" if italic else ""

    return f"""<td data-highlight-colour="{cell_colour}"><p style="text-align: {text_align};">{BOLD_START}{ITALIC_START}<span style="color: {text_colour};">{value}</span>{ITALIC_END}{BOLD_END}</p></td>"""


def process_xml_pandas(df):

    values_list = df.values.tolist()
    value_matrix = [list(df.columns)] + values_list
    cell_colour_matrix = [COLOUR.blue] + len(values_list) * [COLOUR.white]
    text_colour_matrix = [COLOUR.white] + len(values_list) * [COLOUR.black]
    bold_matrix = [True] + len(values_list) * [False]

    return create_xml_table(value_matrix, cell_colour_matrix)
