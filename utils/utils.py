from io import BytesIO


def plot_to_img(plt):
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf
