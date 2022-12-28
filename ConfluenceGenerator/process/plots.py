import io


def process_plotly_xml(fig, _variable_name):
    return {
        "image": (f"{_variable_name}.png", get_plotly_bytes(fig)),
        "xml": f"""<ac:image ac:align="center">
    <ri:attachment ri:filename="{_variable_name}.png" ri:version-at-save="4" />
    </ac:image>""",
    }


def get_plotly_bytes(plot):
    b = io.BytesIO()
    plot.write_image(b)
    b.seek(0)
    return b.read()
