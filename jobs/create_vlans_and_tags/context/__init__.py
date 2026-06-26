"""Render context for the Create VLANs and Tags design."""

from nautobot_design_builder.context import Context, context_file


@context_file("context.yaml")
class CreateVLANsContext(Context):
    """Render context for the Create VLANs and Tags design."""
