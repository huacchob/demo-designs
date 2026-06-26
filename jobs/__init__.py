"""The __init__.py module is required for Nautobot to load the jobs via Git."""

from .core_site import CoreSiteDesign
from .create_vlans_and_tags import CreateVLANsAndTagsDesign
from .edge_site import EdgeDesign
from .initial_data import InitialDesign
from .p2p import P2PDesign

__all__ = [
    "CoreSiteDesign",
    "CreateVLANsAndTagsDesign",
    "EdgeDesign",
    "InitialDesign",
    "P2PDesign",
]
