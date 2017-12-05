#!/usr/bin/env python
import sys 
sys.path.append("../../../")

from helpers.magicdict import MagicDict
from troposphere import AWS_STACK_NAME, Output, Ref, Export, GetAtt, Join


class Outputs(MagicDict):
    def __init__(self, vpc, parameters):
        super(Outputs, self).__init__()

        self.PrivateZoneId = Output(
            "PrivateZoneId",
            Description="The ID for the private Route53 zone",
            Export=Export("master-zone-internal-id"),
            Value=Ref(vpc.InternalZone),
        )
        
        self.PrivateZoneIdProductionWebsite = Output(
            "PrivateZoneIdProductionWebsite",
            Description="The ID for the private Route53 zone",
            Export=Export("master-zone-internal-id-production-site"),
            Value=Ref(vpc.InternalZoneProductionWebsite),
            Condition="CreateProductionZone"
        )

        self.PublicRouteTable = Output(
            "PublicRouteTable",
            Description="PublicRouteTable",
            Export=Export("PublicRouteTable"),
            Value=Ref(vpc.PublicRouteTable),
        )

        self.PrivateARouteTable = Output(
            "PrivateARouteTable",
            Description="PrivateARouteTable",
            Export=Export("master-zone-private-a-route-table"),
            Value=Ref(vpc.PrivateARouteTable),
        )
        
        self.PrivateBRouteTable = Output(
            "PrivateBRouteTable",
            Description="PrivateBRouteTable",
            Export=Export("master-zone-private-b-route-table"),
            Value=Ref(vpc.PrivateBRouteTable),
        )
        
        self.PrivateZoneName = Output(
            "PrivateZoneName",
            Description="The name for the private Route53 zone",
            Export=Export("master-zone-internal-name"),
            Value=Ref(parameters.DomainName),
        )
        
        self.PrivateZoneNameProductionWebsite = Output(
            "PrivateZoneNameProductionWebsite",
            Description="The name for the private Route53 zone",
            Export=Export("master-zone-internal-name-production-site"),
            Value="sharpe.capital",
            Condition="CreateProductionZone"
        )
        
        self.AllICMPSecurityGroup = Output(
            "AllICMPSecurityGroup",
            Description="All ICMP SG created by this stack",
            Export=Export("master-sg-all-icmp"),
            Value=Ref(vpc.ICMPSecurityGroup),
        )
        
        # Shared services
        self.SharedServicesPrivateSubnetA = Output(
            "SharedServicesPrivateSubnetA",
            Description="Private subnet for shared resources in eu-west-1a",
            Export=Export("master-subnet-shared-private-a"),
            Value=Ref(vpc.SharedServicesPrivateSubnetA),
        )
        
        self.SharedServicesPrivateSubnetB = Output(
            "SharedServicesPrivateSubnetB",
            Description="Private subnet for shared resources in eu-west-1b",
            Export=Export("master-subnet-shared-private-b"),
            Value=Ref(vpc.SharedServicesPrivateSubnetB),
        )
        
        self.SharedServicesPrivateSubnetACidr = Output(
            "SharedServicesPrivateSubnetACidr",
            Description="Private subnet cidr for shared resources in eu-west-1a",
            Export=Export("master-cidr-shared-private-a"),
            Value=Ref(parameters.SharedServicesPrivateSubnetACIDR),
        )
        
        self.SharedServicesPrivateSubnetBCidr = Output(
            "SharedServicesPrivateSubnetBCidr",
            Description="Private cidr range for shared resources in eu-west-1b",
            Export=Export("master-cidr-shared-private-b"),
            Value=Ref(parameters.SharedServicesPrivateSubnetBCIDR),
        )
        
        self.GeneralPrivateSubnetB = Output(
            "GeneralPrivateSubnetB",
            Description="Private subnet for general resources in eu-west-1b",
            Export=Export("master-subnet-general-private-b"),
            Value=Ref(vpc.GeneralPrivateSubnetB),
        )
        
        self.VPCId = Output(
            "VPCId",
            Description="VPC created by this stack",
            Export=Export("master-vpc"),
            Value=Ref(vpc.vpc),
        )
        
        self.SharedServicesPrivateSubnetA = Output(
            "SharedServicesPrivateSubnetA",
            Description="Private subnet for shared resources in eu-west-1a",
            Export=Export("master-subnet-shared-private-a"),
            Value=Ref(vpc.SharedServicesPrivateSubnetA),
        )
        
        self.GeneralPrivateSubnetA = Output(
            "GeneralPrivateSubnetA",
            Description="Private subnet for general resources in eu-west-1a",
            Export=Export("master-subnet-general-private-a"),
            Value=Ref(vpc.GeneralPrivateSubnetA),
        )
        
        self.SharedServicesPublicSubnetA = Output(
            "SharedServicesPublicSubnetA",
            Description="Public subnet for shared resources in eu-west-1a",
            Export=Export("master-subnet-shared-public-a"),
            Value=Ref(vpc.SharedServicesPublicSubnetA),
        )
        
        self.SharedServicesPublicSubnetB = Output(
            "SharedServicesPublicSubnetB",
            Description="Public subnet for shared resources in eu-west-1b",
            Export=Export("master-subnet-shared-public-b"),
            Value=Ref(vpc.SharedServicesPublicSubnetB),
        )
        
        self.InternetGatewayId = Output(
            "InternetGatewayId",
            Description="Internet gateway created by this stack",
            Export=Export("master-ig"),
            Value=Ref(vpc.InternetGateway),
        )

        self.LBSubnetA = Output(
            "LBSubnetA",
            Export=Export(Join("-", [Ref(AWS_STACK_NAME), "lb-subnet-a"])),
            Description="Subnet for running public resources in AZ A",
            Value=Ref(vpc.LBPublicSubnetA),
        )

        self.LBSubnetB = Output(
            "LBSubnetB",
            Export=Export(Join("-", [Ref(AWS_STACK_NAME), "lb-subnet-b"])),
            Description="Subnet for running public resources in AZ B",
            Value=Ref(vpc.LBPublicSubnetB),
        )

