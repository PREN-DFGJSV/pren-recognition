import string
from dataclasses import dataclass

import EOrientierung


@dataclass
class CubePart:
    orientierung: EOrientierung
    unten_links: string
    unten_rechts: string
    oben_links: string
    oben_rechts: string


