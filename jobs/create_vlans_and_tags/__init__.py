"""Design to create VLANs and the tags applied to them."""

from nautobot.apps.jobs import register_jobs
from nautobot_design_builder.design_job import DesignJob

from .context import CreateVLANsContext


class CreateVLANsAndTagsDesign(DesignJob):
    """Create VLANs and the tags applied to them."""

    class Meta:
        """Metadata needed to implement the Create VLANs and Tags design."""

        name = "Create VLANs and Tags Design"
        dryrun_default = True
        has_sensitive_variables = False
        design_file = "designs/0001_vlans.yaml.j2"
        context_class = CreateVLANsContext
        nautobot_version = ">=2"
        version = "0.1.0"
        description = "Create a 'dhcp' tag and a VLAN tagged with it."
        docs = """This design creates VLANs and the tags applied to them.

This design takes no user input.

The outcome of the design contains:
    - A `Tag` named `dhcp` applicable to `VLAN` objects.
    - A `VLAN` with VID 30 named `test` (status `Active`), tagged with `dhcp`.
"""


name = "Demo Designs"
register_jobs(CreateVLANsAndTagsDesign)
