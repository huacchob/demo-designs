"""Render context for the Create Networks design."""

from __future__ import annotations

import ipaddress

from django.core.exceptions import ValidationError
from nautobot.ipam.models import Prefix
from nautobot_design_builder.context import Context, context_file

SUPERNET_PREFIX_LENGTH = 21
NETWORK_PREFIX_LENGTH = 24
MANAGEMENT_PREFIX_LENGTH = 26


@context_file("context.yaml")
class CreateNetworksContext(Context):
    """Render context for the Create Networks design."""

    prefix: str

    def __hash__(self) -> int:
        """Hash the context on its supplied prefix."""
        return hash(self.prefix)

    def validate_prefix_is_a_supernet(self) -> None:
        """Ensure the supplied supernet is a /21.

        Raises:
            ValidationError: If the supplied prefix is not a /21.
        """
        network: ipaddress.IPv4Network = ipaddress.ip_network(address=self.prefix, strict=False)
        if network.prefixlen != SUPERNET_PREFIX_LENGTH:
            raise ValidationError({"prefix": f"The supplied prefix must be a /{SUPERNET_PREFIX_LENGTH}."})

    def validate_prefix_does_not_exist(self) -> None:
        """Ensure the supplied supernet has not already been created.

        Raises:
            ValidationError: If the supplied prefix already exists.
        """
        network: ipaddress.IPv4Network = ipaddress.ip_network(address=self.prefix, strict=False)
        if Prefix.objects.filter(
            network=str(network.network_address),
            prefix_length=network.prefixlen,
        ).exists():
            raise ValidationError({"prefix": "Prefix already exists."})

    @property
    def child_prefixes(self) -> list[str]:
        """The eight /24 networks contained within the supplied /21."""
        network: ipaddress.IPv4Network = ipaddress.ip_network(address=self.prefix, strict=False)
        return [str(subnet) for subnet in network.subnets(new_prefix=NETWORK_PREFIX_LENGTH)]

    @property
    def management_network(self) -> str:
        """The /24 (last of the eight) that is carved up for management traffic."""
        return self.child_prefixes[-1]

    @property
    def management_prefix(self) -> str:
        """The first /26 carved from the management /24."""
        network: ipaddress.IPv4Network = ipaddress.ip_network(self.management_network)
        return str(next(network.subnets(new_prefix=MANAGEMENT_PREFIX_LENGTH)))
