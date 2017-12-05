#!/usr/bin/env python
import sys
sys.path.append("../../../")

from helpers.magicdict import MagicDict
from troposphere import AWS_STACK_NAME, AWS_REGION, Ref, Join, Tags, GetAtt
from troposphere.ec2 import VPC, VPCEndpoint, SecurityGroup, EIP, NatGateway, PortRange 
from troposphere.ec2 import Subnet, SubnetNetworkAclAssociation, SubnetRouteTableAssociation
from troposphere.ec2 import NetworkAcl, NetworkAclEntry, RouteTable, Route, InternetGateway
from troposphere.route53 import HostedZone, HostedZoneVPCs, HostedZoneConfiguration
from troposphere.ec2 import ICMP, VPCGatewayAttachment, SecurityGroupRule


class Vpc(MagicDict):
    def __init__(self, parameters):
        super(Vpc, self).__init__()

        # Virtual Private Cloud
        self.vpc = VPC(
            "VPC",
            CidrBlock=Ref(parameters.VPCCIDR),
            EnableDnsHostnames=True,
            Tags=Tags(
                Name=Ref(AWS_STACK_NAME),
            )
        )
        
        # Public NACL
        self.GeneralPublicNACL = NetworkAcl(
            "GeneralPublicNACL",
            VpcId=Ref(self.vpc),
            Tags=Tags(
                Name=Join("-", [Ref(AWS_STACK_NAME), "public"]),
            ),
        )

        # Private NACL
        self.GeneralPrivateNACL = NetworkAcl(
            "GeneralPrivateNACL",
            VpcId=Ref(self.vpc),
            Tags=Tags(
                Name=Join("-", [Ref(AWS_STACK_NAME), "private"]),
            ),
        )

        # NACL Rules
        self.PublicNACLIngressRule100 = NetworkAclEntry(
            "PublicNACLIngressRule100",
            NetworkAclId=Ref(self.GeneralPublicNACL),
            RuleNumber="100",
            Protocol="-1",
            Egress=False,
            RuleAction="allow",
            CidrBlock="0.0.0.0/0",
        )

        self.PublicNACLEgressRule100 = NetworkAclEntry(
            "PublicNACLEgressRule100",
            NetworkAclId=Ref(self.GeneralPublicNACL),
            RuleNumber="100",
            Protocol="-1",
            Egress=True,
            RuleAction="allow",
            CidrBlock="0.0.0.0/0",
        )

        self.PrivateNACLEgressRule100 = NetworkAclEntry(
            "PrivateNACLEgressRule100",
            NetworkAclId=Ref(self.GeneralPrivateNACL),
            RuleNumber="100",
            Protocol="-1",
            Egress=True,
            RuleAction="allow",
            CidrBlock="0.0.0.0/0",
        )
        
        self.PrivateNACLIngressRule100 = NetworkAclEntry(
            "PrivateNACLIngressRule100",
            NetworkAclId=Ref(self.GeneralPrivateNACL),
            RuleNumber="100",
            Protocol="-1",
            Egress=False,
            RuleAction="allow",
            CidrBlock=Ref(parameters.VPCCIDR),
        )

        self.PrivateNACLIngressRule220 = NetworkAclEntry(
            "PrivateNACLIngressRule220",
            NetworkAclId=Ref(self.GeneralPrivateNACL),
            RuleNumber="220",
            Protocol="-1",
            Egress=False,
            RuleAction="allow",
            CidrBlock="0.0.0.0/0",
        )

        self.PrivateNACLIngressRule400 = NetworkAclEntry(
            "PrivateNACLIngressRule400",
            NetworkAclId=Ref(self.GeneralPrivateNACL),
            RuleNumber="400",
            Protocol="6",
            PortRange=PortRange(To="65535", From="1024"),
            Egress=False,
            RuleAction="allow",
            CidrBlock="0.0.0.0/0",
        )

        self.PrivateNACLIngressRule420 = NetworkAclEntry(
            "PrivateNACLIngressRule420",
            NetworkAclId=Ref(self.GeneralPrivateNACL),
            RuleNumber="420",
            Protocol="1",
            Egress=False,
            RuleAction="allow",
            Icmp=ICMP(
                Code="-1",
                Type="-1"
            ),
            CidrBlock="0.0.0.0/0",
        )

        self.PrivateNACLIngressRule440 = NetworkAclEntry(
            "PrivateNACLIngressRule440",
            NetworkAclId=Ref(self.GeneralPrivateNACL),
            RuleNumber="440",
            Protocol="17",
            PortRange=PortRange(To="65535", From="1024"),
            Egress=False,
            RuleAction="allow",
            CidrBlock="0.0.0.0/0",
        )

        # Shared services 
        self.GeneralPrivateSubnetA = Subnet(
            "GeneralPrivateSubnetA",
            Tags=Tags(
                Name=Join("-", [Ref(AWS_STACK_NAME), "general-private-a"]),
            ),
            VpcId=Ref(self.vpc),
            MapPublicIpOnLaunch=False,
            CidrBlock=Ref(parameters.GeneralPrivateSubnetACIDR),
            AvailabilityZone=Ref(parameters.AvailabilityZoneA),
        )

        self.GeneralPrivateSubnetB = Subnet(
            "GeneralPrivateSubnetB",
            Tags=Tags(
                Name=Join("-", [Ref(AWS_STACK_NAME), "general-private-b"]),
            ),
            VpcId=Ref(self.vpc),
            MapPublicIpOnLaunch=False,
            CidrBlock=Ref(parameters.GeneralPrivateSubnetBCIDR),
            AvailabilityZone=Ref(parameters.AvailabilityZoneB),
        )

        self.SharedServicesPublicSubnetA = Subnet(
            "SharedServicesPublicSubnetA",
            VpcId=Ref(self.vpc),
            AvailabilityZone=Ref(parameters.AvailabilityZoneA),
            CidrBlock=Ref(parameters.SharedServicesPublicSubnetACIDR),
            MapPublicIpOnLaunch=False,
            Tags=Tags(
                Name=Join("-", [Ref(AWS_STACK_NAME), "shared-public-a"]),
            )
        )
        
        self.SharedServicesPublicSubnetB = Subnet(
            "SharedServicesPublicSubnetB",
            VpcId=Ref(self.vpc),
            AvailabilityZone=Ref(parameters.AvailabilityZoneB),
            CidrBlock=Ref(parameters.SharedServicesPublicSubnetBCIDR),
            MapPublicIpOnLaunch=False,
            Tags=Tags(
                Name=Join("-", [Ref(AWS_STACK_NAME), "shared-public-b"]),
            )
        )
        
        self.SharedServicesPrivateSubnetA = Subnet(
            "SharedServicesPrivateSubnetA",
            VpcId=Ref(self.vpc),
            AvailabilityZone=Ref(parameters.AvailabilityZoneA),
            CidrBlock=Ref(parameters.SharedServicesPrivateSubnetACIDR),
            MapPublicIpOnLaunch=False,
            Tags=Tags(
                Name=Join("-", [Ref(AWS_STACK_NAME), "shared-private-a"]),
            )
        )
        
        self.SharedServicesPrivateSubnetB = Subnet(
            "SharedServicesPrivateSubnetB",
            VpcId=Ref(self.vpc),
            AvailabilityZone=Ref(parameters.AvailabilityZoneB),
            CidrBlock=Ref(parameters.SharedServicesPrivateSubnetBCIDR),
            MapPublicIpOnLaunch=False,
            Tags=Tags(
                Name=Join("-", [Ref(AWS_STACK_NAME), "shared-private-b"]),
            )
        )

        self.SharedServicesPublicNACLSubnetAAssocation = SubnetNetworkAclAssociation(
            "SharedServicesPublicNACLSubnetAAssocation",
            SubnetId=Ref(self.SharedServicesPublicSubnetA),
            NetworkAclId=Ref(self.GeneralPublicNACL),
        )

        self.SharedServicesPublicNACLSubnetBAssocation = SubnetNetworkAclAssociation(
            "SharedServicesPublicNACLSubnetBAssocation",
            SubnetId=Ref(self.SharedServicesPublicSubnetB),
            NetworkAclId=Ref(self.GeneralPublicNACL),
        )
        
        self.SharedServicesPrivateNACLSubnetAAssocation = SubnetNetworkAclAssociation(
            "SharedServicesPrivateNACLSubnetAAssocation",
            SubnetId=Ref(self.SharedServicesPrivateSubnetA),
            NetworkAclId=Ref(self.GeneralPrivateNACL),
        )

        self.SharedServicesPrivateNACLSubnetBAssocation = SubnetNetworkAclAssociation(
            "SharedServicesPrivateNACLSubnetBAssocation",
            SubnetId=Ref(self.SharedServicesPrivateSubnetB),
            NetworkAclId=Ref(self.GeneralPrivateNACL),
        )

        self.GeneralPrivateNACLSubnetAAssocation = SubnetNetworkAclAssociation(
            "GeneralPrivateNACLSubnetAAssocation",
            SubnetId=Ref(self.GeneralPrivateSubnetA),
            NetworkAclId=Ref(self.GeneralPrivateNACL),
        )
        
        self.GeneralPrivateNACLSubnetBAssocation = SubnetNetworkAclAssociation(
            "GeneralPrivateNACLSubnetBAssocation",
            SubnetId=Ref(self.GeneralPrivateSubnetB),
            NetworkAclId=Ref(self.GeneralPrivateNACL),
        )

        # Route tables
        self.PublicRouteTable = RouteTable(
            "PublicRouteTable",
            VpcId=Ref(self.vpc),
            Tags=Tags(
                Name=Join("-", [Ref(AWS_STACK_NAME), "public"]),
            ),  
        )

        self.PrivateARouteTable = RouteTable(
            "PrivateARouteTable",
            VpcId=Ref(self.vpc),
            Tags=Tags(
                Name=Join("-", [Ref(AWS_STACK_NAME), "private-a"]),
            ),
        )

        self.PrivateBRouteTable = RouteTable(
            "PrivateBRouteTable",
            VpcId=Ref(self.vpc),
            Tags=Tags(
                Name=Join("-", [Ref(AWS_STACK_NAME), "private-b"]),
            ),
        )

        # Internet Gateway
        self.InternetGateway = InternetGateway(
            "InternetGateway",
            Tags=Tags(
                Name=Join("-", [Ref(AWS_STACK_NAME)]),
            ),
        )

        self.VPNAttachment = VPCGatewayAttachment(
            "VPNAttachment",
            VpcId=Ref(self.vpc),
            InternetGatewayId=Ref(self.InternetGateway)
        )

        # NAT Gateways
        self.NATGatewayAEIP = EIP(
            "NATGatewayAEIP",
            Domain=Ref(self.vpc),
            Condition="DeployNATGateways"
        )
        
        self.NATGatewayBEIP = EIP(
            "NATGatewayBEIP",
            Domain=Ref(self.vpc),
            Condition="DeployNATGateways"
        )

        self.NATGatewayA = NatGateway(
            "NATGatewayA",
            SubnetId=Ref(self.SharedServicesPublicSubnetA),
            AllocationId=GetAtt(self.NATGatewayAEIP, "AllocationId"),
            Condition="DeployNATGateways"
        )
        
        self.NATGatewayB = NatGateway(
            "NATGatewayB",
            SubnetId=Ref(self.SharedServicesPublicSubnetB),
            AllocationId=GetAtt(self.NATGatewayBEIP, "AllocationId"),
            Condition="DeployNATGateways"
        )

        # S3 VPC enpoint connection 
        self.VPCS3Endpoint = VPCEndpoint(
            "VPCS3Endpoint",
            VpcId=Ref(self.vpc),
            ServiceName=Join("", ["com.amazonaws.", Ref(AWS_REGION), ".s3"]),
            RouteTableIds=[Ref(self.PublicRouteTable), Ref(self.PrivateARouteTable), Ref(self.PrivateBRouteTable)],
        )

        # Security Groups
        self.ICMPSecurityGroup = SecurityGroup(
            "ICMPSecurityGroup",
            SecurityGroupIngress=[{ "ToPort": "-1", "IpProtocol": "icmp", "CidrIp": "0.0.0.0/0", "FromPort": "-1" }],
            VpcId=Ref(self.vpc),
            GroupDescription="Allows servers to be reached by ICMP",
            Tags=Tags(
                Name=Join("-", [Ref(AWS_STACK_NAME), "icmp"]),
            ),
        )

        self.OpenPublicSSHSecurityGroup = SecurityGroup(
            "OpenPublicSSHSecurityGroup",
            SecurityGroupIngress=[{ "ToPort": "22", "IpProtocol": "tcp", "CidrIp": "0.0.0.0/0", "FromPort": "22" }],
            VpcId=Ref(self.vpc),
            GroupDescription="Allows instance to be publically managed over SSH from anywhere, probably a bad idea",
            Tags=Tags(
                Name=Join("-", [Ref(AWS_STACK_NAME), "open-public-ssh"]),
            ),
        )

        # Route Tables
        self.GeneralPrivateSubnetARouteTable = SubnetRouteTableAssociation(
            "GeneralPrivateSubnetARouteTable",
            SubnetId=Ref(self.GeneralPrivateSubnetA),
            RouteTableId=Ref(self.PrivateARouteTable),
        )
        
        self.GeneralPrivateSubnetBRouteTable = SubnetRouteTableAssociation(
            "GeneralPrivateSubnetBRouteTable",
            SubnetId=Ref(self.GeneralPrivateSubnetB),
            RouteTableId=Ref(self.PrivateBRouteTable),
        )
        
        self.SharedServicesPublicSubnetARouteTable = SubnetRouteTableAssociation(
            "SharedServicesPublicSubnetARouteTable",
            SubnetId=Ref(self.SharedServicesPublicSubnetA),
            RouteTableId=Ref(self.PublicRouteTable),
        )

        self.SharedServicesPublicSubnetBRouteTable = SubnetRouteTableAssociation(
            "SharedServicesPublicSubnetBRouteTable",
            SubnetId=Ref(self.SharedServicesPublicSubnetB),
            RouteTableId=Ref(self.PublicRouteTable),
        )

        self.SharedServicesPrivateSubnetARouteTable = SubnetRouteTableAssociation(
            "SharedServicesPrivateSubnetARouteTable",
            SubnetId=Ref(self.SharedServicesPrivateSubnetA),
            RouteTableId=Ref(self.PrivateARouteTable),
        )

        self.SharedServicesPrivateSubnetBRouteTable = SubnetRouteTableAssociation(
            "SharedServicesPrivateSubnetBRouteTable",
            SubnetId=Ref(self.SharedServicesPrivateSubnetB),
            RouteTableId=Ref(self.PrivateBRouteTable),
        )
        
        # Routes
        self.PublicSharedRoute = Route(
            "PublicSharedRoute",
            DestinationCidrBlock="0.0.0.0/0",
            GatewayId=Ref(self.InternetGateway),
            RouteTableId=Ref(self.PublicRouteTable),
        )
    
        self.PrivateANATRoute = Route(
            "PrivateANATRoute",
            DestinationCidrBlock="0.0.0.0/0",
            RouteTableId=Ref(self.PrivateARouteTable),
            NatGatewayId=Ref(self.NATGatewayB),
            #DependsOn=self.NATGatewayA,
            Condition="DeployNATGateways"
        )

        self.PrivateBNATRoute = Route(
            "PrivateBNATRoute",
            DestinationCidrBlock="0.0.0.0/0",
            RouteTableId=Ref(self.PrivateBRouteTable),
            NatGatewayId=Ref(self.NATGatewayB),
            #DependsOn=self.NATGatewayB,
            Condition="DeployNATGateways"
        )

        # Internal Zone standard
        self.InternalZone = HostedZone(
            "InternalZone",
            VPCs=[
                HostedZoneVPCs(
                    VPCId=Ref(self.vpc), 
                    VPCRegion=Ref("AWS::Region"),
            )],
            HostedZoneConfig=HostedZoneConfiguration(
                Comment="Internal (private) zone for name resolution"
            ),
            HostedZoneTags=Tags(
                Name=Join("-", [Ref(AWS_STACK_NAME), "internal"]),
            ),
            Name=Ref(parameters.DomainName),
        )
        
        # Internal Zone production website
        self.InternalZoneProductionWebsite = HostedZone(
            "InternalZoneProductionWebsite",
            VPCs=[
                HostedZoneVPCs(
                    VPCId=Ref(self.vpc), 
                    VPCRegion=Ref("AWS::Region"),
            )],
            HostedZoneConfig=HostedZoneConfiguration(
                Comment="Internal (private) zone for name resolution for public website"
            ),
            HostedZoneTags=Tags(
                Name=Join("-", [Ref(AWS_STACK_NAME), "internal-public-site"]),
            ),
            Name="sharpe.capital",
            Condition="CreateProductionZone"
        )

        # Custom Security Groups
        self.OpenPublicSSHSecurityGroup = SecurityGroup(
            "OpenPublicSSHSecurityGroup",
            GroupDescription="Allows server to be publically managed over SSH from anywhere",
            SecurityGroupIngress=[
                SecurityGroupRule(
                    IpProtocol="tcp", 
                    FromPort="22",
                    ToPort="22",
                    CidrIp="0.0.0.0/0"
                ),
            ],
            VpcId=Ref(self.vpc),
            Tags=Tags(
                Name=Join("-", [Ref(AWS_STACK_NAME), "open-public-ssh-access"]),
            ),
        )

        # Public Load Balancer NACL 
        self.PublicLBNACL = NetworkAcl(
            "PublicLBNACL",
            VpcId=Ref(self.vpc),
            Tags=Tags(
                Name=Ref(AWS_STACK_NAME),
            ),
        )
        
        self.PublicLBRouteTable = RouteTable(
            "PublicLBRouteTable",
            VpcId=Ref(self.vpc),
            Tags=Tags(
                Name=Ref(AWS_STACK_NAME),
            ),
        )
        
        self.LBPublicSubnetA = Subnet(
            "LBPublicSubnetA",
            VpcId=Ref(self.vpc),
            AvailabilityZone=Ref(parameters.AvailabilityZoneA),
            CidrBlock=Ref(parameters.LBSubnetACIDR),
            Tags=Tags(
                Name=Join("-", [Ref(AWS_STACK_NAME), "lb-public-a"]),
            ),
        )
        
        self.LBPublicSubnetB = Subnet(
            "LBPublicSubnetB",
            VpcId=Ref(self.vpc),
            AvailabilityZone=Ref(parameters.AvailabilityZoneB),
            CidrBlock=Ref(parameters.LBSubnetBCIDR),
            Tags=Tags(
                Name=Join("-", [Ref(AWS_STACK_NAME), "lb-public-b"]),
            ),
        )
        
        self.LBNACLIn100 = NetworkAclEntry(
            "LBNACLIn100",
            NetworkAclId=Ref(self.PublicLBNACL),
            RuleNumber=100,
            Protocol=6,
            PortRange=PortRange(To=443, From=443),
            Egress=False,
            RuleAction="allow",
            CidrBlock="0.0.0.0/0",
        )

        self.LBNACLIn200 = NetworkAclEntry(
            "LBNACLIn200",
            NetworkAclId=Ref(self.PublicLBNACL),
            RuleNumber=200,
            Protocol=6,
            PortRange=PortRange(To=80, From=80),
            Egress=False,
            RuleAction="allow",
            CidrBlock="0.0.0.0/0",
        )
        
        self.LBNACLIn300 = NetworkAclEntry(
            "LBNACLIn300",
            NetworkAclId=Ref(self.PublicLBNACL),
            RuleNumber=300,
            Protocol=6,
            PortRange=PortRange(To=65535, From=1024),
            Egress=False,
            RuleAction="allow",
            CidrBlock="0.0.0.0/0",
        )
        
        self.LBNACLOut100 = NetworkAclEntry(
            "LBNACLOut100",
            NetworkAclId=Ref(self.PublicLBNACL),
            RuleNumber=100,
            Protocol=6,
            PortRange=PortRange(To=65535, From=1024),
            Egress=True,
            RuleAction="allow",
            CidrBlock="0.0.0.0/0",
        )
        
        self.LBRouteTableAssociationA = SubnetRouteTableAssociation(
            "LBRouteTableAssociationA",
            SubnetId=Ref(self.LBPublicSubnetA),
            RouteTableId=Ref(self.PublicLBRouteTable),
        )
        
        self.LBRouteTableAssociationB = SubnetRouteTableAssociation(
            "LBRouteTableAssociationB",
            SubnetId=Ref(self.LBPublicSubnetB),
            RouteTableId=Ref(self.PublicLBRouteTable),
        )
        
        self.LBNACLAssociationB = SubnetNetworkAclAssociation(
            "LBNACLAssociationB",
            SubnetId=Ref(self.LBPublicSubnetB),
            NetworkAclId=Ref(self.PublicLBNACL),
        )
        
        self.LBNACLAssociationA = SubnetNetworkAclAssociation(
            "LBNACLAssociationA",
            SubnetId=Ref(self.LBPublicSubnetA),
            NetworkAclId=Ref(self.PublicLBNACL),
        )
        
        self.LBInternetGatewayRoute = Route(
            "LBInternetGatewayRoute",
            GatewayId=Ref(self.InternetGateway),
            DestinationCidrBlock="0.0.0.0/0",
            RouteTableId=Ref(self.PublicLBRouteTable),
        )
        
        self.LBICMPSecurityGroup = SecurityGroup(
            "LBICMPSecurityGroup",
            SecurityGroupIngress=[{ "ToPort": "-1", "IpProtocol": "icmp", "CidrIp": "0.0.0.0/0", "FromPort": "-1" }],
            VpcId=Ref(self.vpc),
            GroupDescription="Allows servers to be reached by ICMP",
            Tags=Tags(
                Name=Join("-", [Ref(AWS_STACK_NAME), "icmp"]),
            ),
        )
        
        self.LBSecurityGroup = SecurityGroup(
            "LBSecurityGroup",
            SecurityGroupIngress=[{ "ToPort": 80, "FromPort": 80, "IpProtocol": "tcp", "CidrIp": "0.0.0.0/0" }, 
                { "ToPort": 443, "FromPort": 443, "IpProtocol": "tcp", "CidrIp": "0.0.0.0/0" }],
            VpcId=Ref(self.vpc),
            GroupDescription="Securty group for public facing web load balancers",
            Tags=Tags(
                Name=Ref(AWS_STACK_NAME),
            ),
        )
