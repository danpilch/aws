#!/usr/bin/env python
import sys
sys.path.append("../../../")

from troposphere import Parameter
from helpers.magicdict import MagicDict


class Parameters(MagicDict):
    def __init__(self):
        super(Parameters, self).__init__()
        
        self.AvailabilityZoneA = Parameter(
            "AvailabilityZoneA",
            Description="Availability Zone A for stack (must correspond to region deploying into)",
            Type="String"
        )
        
        self.AvailabilityZoneB = Parameter(
            "AvailabilityZoneB",
            Description="Availability Zone B for stack (must correspond to region deploying into)",
            Type="String"
        )

        self.Environment = Parameter(
            "Environment",
            AllowedValues=["dev", "staging", "prod"],
            Description="Environment to deploy into",
            Default="dev",
            Type="String"
        )

        self.DomainName = Parameter(
            "DomainName",
            Description="Domain used for internal and public DNS zones",
            Default="example.com",
            Type="String",
        )
        
        self.DeployNATGateways = Parameter(
            "DeployNATGateways",
            AllowedValues=["true", "false"],
            Description="Whether to deploy NAT Gateways or not. Gateways cost money",
            Default="false",
            Type="String",
        )
            
        self.VPCCIDR = Parameter(
            "VPCCIDR",
            AllowedPattern="(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})/(\d{1,2})",
            ConstraintDescription="Must be a valid IP CIDR range of the form x.x.x.x/x",
            Description="CIDR block for the VPC /16 range",
            Default="10.2.0.0/16",
            Type="String"
        )

        self.GeneralPrivateSubnetACIDR = Parameter(
            "GeneralPrivateSubnetACIDR",
            AllowedPattern="(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})/(\d{1,2})",
            ConstraintDescription="Must be a valid IP CIDR range of the form x.x.x.x/x",
            Description="A /21 CIDR block for the general-private-a subnet",
            Default="10.2.0.0/21",
            Type="String"
        )
        
        self.GeneralPrivateSubnetBCIDR = Parameter(
            "GeneralPrivateSubnetBCIDR",
            AllowedPattern="(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})/(\d{1,2})",
            ConstraintDescription="Must be a valid IP CIDR range of the form x.x.x.x/x",
            Description="A /21 CIDR block for the general-private-b subnet",
            Default="10.2.8.0/21",
            Type="String"
        )

        self.SharedServicesPublicSubnetACIDR = Parameter(
            "SharedServicesPublicSubnetACIDR",
            AllowedPattern="(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})/(\d{1,2})",
            ConstraintDescription="Must be a valid IP CIDR range of the form x.x.x.x/x",
            Description="A /21 CIDR block for the shared-public-a subnet",
            Default="10.2.16.0/21",
            Type="String"
        )

        self.SharedServicesPublicSubnetBCIDR = Parameter(
            "SharedServicesPublicSubnetBCIDR",
            AllowedPattern="(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})/(\d{1,2})",
            ConstraintDescription="Must be a valid IP CIDR range of the form x.x.x.x/x",
            Description="A /21 CIDR block for the shared-public-b subnet",
            Default="10.2.24.0/21",
            Type="String"
        )

        self.SharedServicesPrivateSubnetACIDR = Parameter(
            "SharedServicesPrivateSubnetACIDR",
            AllowedPattern="(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})/(\d{1,2})",
            ConstraintDescription="Must be a valid IP CIDR range of the form x.x.x.x/x",
            Description="A /21 CIDR block for the shared-private-a subnet",
            Default="10.2.32.0/21",
            Type="String"
        )
        
        self.SharedServicesPrivateSubnetBCIDR = Parameter(
            "SharedServicesPrivateSubnetBCIDR",
            AllowedPattern="(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})/(\d{1,2})",
            ConstraintDescription="Must be a valid IP CIDR range of the form x.x.x.x/x",
            Description="A /21 CIDR block for the shared-private-b subnet",
            Default="10.2.40.0/21",
            Type="String"
        )

        self.LBSubnetACIDR = Parameter(
            "LBSubnetACIDR",
            AllowedPattern="(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})/(\d{1,2})",
            ConstraintDescription="Must be a valid IP CIDR range of the form x.x.x.x/x",
            Description="A /21 CIDR block for the web-public-a subnet",
            Default="10.2.48.0/21",
            Type="String"
        )
        
        self.LBSubnetBCIDR = Parameter(
            "LBSubnetBCIDR",
            AllowedPattern="(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})/(\d{1,2})",
            ConstraintDescription="Must be a valid IP CIDR range of the form x.x.x.x/x",
            Description="A /21 CIDR block for the web-public-b subnet",
            Default="10.2.56.0/21",
            Type="String"
        )
