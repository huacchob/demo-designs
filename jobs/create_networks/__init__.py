"""Design to create a prefix hierarchy for a new site."""

from nautobot.apps.jobs import StringVar, register_jobs
from nautobot_design_builder.choices import DesignModeChoices
from nautobot_design_builder.design_job import DesignJob

from .context import CreateNetworksContext


class CreateNetworksDesign(DesignJob):
    """Create a /21 container broken into /24 networks plus a management /26.

    Properties:
        prefix (str): The /21 supernet to be created, must include CIDR.
    """

    prefix = StringVar(
        label="Supernet prefix",
        description="The /21 prefix to allocate, including CIDR (e.g. 10.0.0.0/21).",
    )

    class Meta:
        """Metadata needed to implement the Create Networks design."""

        design_mode = DesignModeChoices.DEPLOYMENT
        name = "Create Networks Design"
        dryrun_default = True
        has_sensitive_variables = False
        design_files = [
            "designs/0001_ipam.yaml.j2",
        ]
        context_class = CreateNetworksContext
        version = "0.1.0"
        description = "Create a /21 container, eight /24 networks, and a management /26."
        docs = """This design creates a prefix hierarchy from a single /21 supernet.

The user input data is:
    - prefix: The /21 supernet to be created, must include CIDR.

The outcome of the design contains:
    - A /21 `Prefix` of type `container`.
    - Eight /24 `Prefix` objects within the /21. Seven are type `network`; the
      one reserved for management is type `container`.
    - A management /26 `Prefix` of type `network`, carved from the management /24.
"""


name = "Demo Designs"
register_jobs(CreateNetworksDesign)
