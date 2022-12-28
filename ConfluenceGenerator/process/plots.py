import io


def process_plotly_xml(fig, _variable_name):
    return (
        ("{_variable_name}.png", get_plotly_bytes(fig)),
        f"""<ac:image ac:align="center" ac:layout="wide">
    <ri:attachment ri:filename="{_variable_name}.png" ri:version-at-save="4" />
    </ac:image>""",
    )


def get_plotly_bytes(plot):
    b = io.BytesIO()
    plot.write_image(b)
    b.seek(0)
    return b.read()