#!/usr/bin/env python
import sys 
sys.path.append("../../../")

from helpers.magicdict import MagicDict

from troposphere import Parameter
from troposphere.constants import KEY_PAIR_NAME


class Parameters(MagicDict):
    def __init__(self):
        super(Parameters, self).__init__()

        self.InstanceImage = Parameter(
            "InstanceImage",
            Default="ami-3cd6c45f",
            Type="String",
            Description="AMI image for OpenVPN server"
        )

        self.InstanceKeyPair = Parameter(
            "InstanceKeyPair",
            Type=KEY_PAIR_NAME,
            Description="Keypair for initial connections"
        )

        self.InstanceStorageOS = Parameter(
            "InstanceStorageOS",
            Default="8",
            Type="Number",
            Description="The amount of storage, in GB, to add to the OS disk"
        )

        self.InstanceType = Parameter(
            "InstanceType",
            Default="t2.micro",
            Type="String",
            Description="Instance type",
            AllowedValues=["t2.micro", "t2.medium"]
        )

        self.VPC = Parameter(
            "VPC",
            Type="String",
            Description="The VPC that this stack is being deployed into",
            Default="dev",
            AllowedValues=["dev", "staging", "prod"]
        )
