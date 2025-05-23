"""A module to perform experimental thermochemical data analysis."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pymatgen.core.composition import Composition

if TYPE_CHECKING:
    from typing_extensions import Self

__author__ = "Shyue Ping Ong"
__copyright__ = "Copyright 2012, The Materials Project"
__version__ = "0.1"
__maintainer__ = "Shyue Ping Ong"
__email__ = "shyuep@gmail.com"
__date__ = "Jun 10, 2012"

STANDARD_TEMP = 298.0


class ThermoData:
    """Container for experimental thermo-chemical data."""

    def __init__(
        self,
        data_type,
        cpdname,
        phaseinfo,
        formula,
        value,
        ref="",
        method="",
        temp_range=(298, 298),
        uncertainty=None,
    ):
        """
        Args:
            data_type: The thermochemical data type. Should be one of the
                following: fH - Formation enthalpy, S - Entropy,
                A, B, C, D, E, F, G, H - variables for use in the various
                equations for generating formation enthalpies or Cp at
                various temperatures.
            cpdname (str): A name for the compound. For example, hematite for
                Fe2O3.
            phaseinfo (str): Denoting the phase. For example, "solid", "liquid",
                "gas" or "tetragonal".
            formula (str): A proper string formula, e.g. Fe2O3
            value (float): The value of the data.
            ref (str): A reference, if any, for the data.
            method (str): The method by which the data was determined,
                if available.
            temp_range ([float, float]): Temperature range of validity for the
                data in Kelvin. Defaults to 298 K only.
            uncertainty (float):
                An uncertainty for the data, if available.
        """
        self.type = data_type
        self.formula = formula
        self.composition = Composition(self.formula)
        self.reduced_formula = self.composition.reduced_formula
        self.compound_name = cpdname
        self.phaseinfo = phaseinfo
        self.value = value
        self.temp_range = temp_range
        self.method = method
        self.ref = ref
        self.uncertainty = uncertainty

    @classmethod
    def from_dict(cls, dct: dict) -> Self:
        """
        Args:
            dct (dict): Dict representation.

        Returns:
            ThermoData
        """
        return cls(
            dct["type"],
            dct["compound_name"],
            dct["phaseinfo"],
            dct["formula"],
            dct["value"],
            dct["ref"],
            dct["method"],
            dct["temp_range"],
            dct.get("uncertainty"),
        )

    def as_dict(self):
        """Get MSONable dict."""
        return {
            "@module": type(self).__module__,
            "@class": type(self).__name__,
            "type": self.type,
            "formula": self.formula,
            "compound_name": self.compound_name,
            "phaseinfo": self.phaseinfo,
            "value": self.value,
            "temp_range": self.temp_range,
            "method": self.method,
            "ref": self.ref,
            "uncertainty": self.uncertainty,
        }

    def __repr__(self):
        props = [
            "formula",
            "compound_name",
            "phaseinfo",
            "type",
            "temp_range",
            "value",
            "method",
            "ref",
            "uncertainty",
        ]
        return "\n".join(f"{k} : {getattr(self, k)}" for k in props)

    def __str__(self):
        return (
            f"{self.type}_{self.formula}_{self.phaseinfo} = {self.value}, Valid T : {self.temp_range}, Ref = {self.ref}"
        )
