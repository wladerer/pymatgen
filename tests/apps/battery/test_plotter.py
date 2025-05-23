from __future__ import annotations

import json

from monty.json import MontyDecoder

from pymatgen.apps.battery.conversion_battery import ConversionElectrode
from pymatgen.apps.battery.insertion_battery import InsertionElectrode
from pymatgen.apps.battery.plotter import VoltageProfilePlotter
from pymatgen.core.composition import Composition
from pymatgen.entries.computed_entries import ComputedEntry
from pymatgen.util.testing import TEST_FILES_DIR

TEST_DIR = f"{TEST_FILES_DIR}/apps/battery"


class TestVoltageProfilePlotter:
    def setup_method(self):
        entry_Li = ComputedEntry("Li", -1.90753119)

        with open(f"{TEST_DIR}/LiTiO2_batt.json", encoding="utf-8") as file:
            entries_LTO = json.load(file, cls=MontyDecoder)
        self.ie_LTO = InsertionElectrode.from_entries(entries_LTO, entry_Li)

        with open(f"{TEST_DIR}/FeF3_batt.json", encoding="utf-8") as file:
            entries = json.load(file, cls=MontyDecoder)
        self.ce_FF = ConversionElectrode.from_composition_and_entries(Composition("FeF3"), entries)

    def test_name(self):
        plotter = VoltageProfilePlotter(xaxis="frac_x")
        plotter.add_electrode(self.ie_LTO, "LTO insertion")
        plotter.add_electrode(self.ce_FF, "FeF3 conversion")
        assert plotter.get_plot_data(self.ie_LTO) is not None
        assert plotter.get_plot_data(self.ce_FF) is not None

    def test_plotly(self):
        plotter = VoltageProfilePlotter(xaxis="frac_x")
        plotter.add_electrode(self.ie_LTO, "LTO insertion")
        plotter.add_electrode(self.ce_FF, "FeF3 conversion")
        fig = plotter.get_plotly_figure()
        assert fig.layout.xaxis.title.text == "Atomic Fraction of Li"

        plotter = VoltageProfilePlotter(xaxis="x_form")
        plotter.add_electrode(self.ce_FF, "FeF3 conversion")
        fig = plotter.get_plotly_figure()
        assert fig.layout.xaxis.title.text == "x in Li<sub>x</sub>FeF3"

        plotter.add_electrode(self.ie_LTO, "LTO insertion")
        fig = plotter.get_plotly_figure()
        assert fig.layout.xaxis.title.text == "x Work Ion per Host F.U."
