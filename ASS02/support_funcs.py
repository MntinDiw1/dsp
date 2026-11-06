from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent


def import_ecg_data(filename):
    """
    Parameters:
    filename: str or Path
        The name of the file containing the ECG data.

    Returns:
    tuple[np.ndarray, np.ndarray, float]
        (t, ecg, sample_rate) - time vector (s), ECG signal (V), and sampling rate (Hz).
    """
    ECG_COLUMN = 8  # ADC channel 2
    data = np.loadtxt(BASE_DIR / filename)
    t = data[:, 0]
    ecg = data[:, ECG_COLUMN]
    sample_rate = 1 / (t[1] - t[0])  # fs = 250 Hz

    return t, ecg, sample_rate


def vector_plot_export(savename):
    """
    Exports the current matplotlib figure as vector graphics (.svg and .pdf) to Report/figs/.

    Parameters:
    savename: str or Path
        Output file name (without extension).
    """
    figs_dir = BASE_DIR / "Report" / "figs"
    figs_dir.mkdir(parents=True, exist_ok=True)
    stem = Path(savename).stem
    plt.savefig(figs_dir / f"{stem}.svg", format="svg", bbox_inches="tight")
    plt.savefig(figs_dir / f"{stem}.pdf", format="pdf", bbox_inches="tight")
