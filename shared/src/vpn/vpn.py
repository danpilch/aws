#!/usr/bin/env python
import sys 
sys.path.append("../../../")

from helpers.magicdict import MagicDict

from awacs import aws
from troposphere import AWS_STACK_NAME, FindInMap, GetAtt, ImportValue, Join, Ref, Tags, iam
from troposphere import ec2, elasticloadbalancing, route53, cloudwatch


class Vpn(MagicDict):
    def __init__(self, parameters):
        super(Vpn, self).__init__()

        self.VpnSG = ec2.SecurityGroup(
            "VpnSG",
            SecurityGroupIngress=[
                ec2.SecurityGroupRule(
                    ToPort=22,
                    IpProtocol="tcp",
                    CidrIp="180.181.214.196/32",
                    FromPort=22
                ),
                ec2.SecurityGroupRule(
                    ToPort=943,
                    IpProtocol="tcp",
                    CidrIp="180.181.214.196/32",
                    FromPort=943
                ),
                ec2.SecurityGroupRule(
                    ToPort=443,
                    IpProtocol="tcp",
                    CidrIp="180.181.214.196/32",
                    FromPort=443
                ),
                ec2.SecurityGroupRule(
                    ToPort=1194,
                    IpProtocol="udp",
                    CidrIp="180.181.214.196/32",
                    FromPort=1194
                ),
            ],
            VpcId=ImportValue("master-vpc"),
            GroupDescription="SG for VPN external connectivity",
            Tags=Tags(
                Name=Join("-", [Ref(AWS_STACK_NAME), "vpn-sg"]),
            ),
        )

        self.VpnInstance = ec2.Instance(
            "VpnInstance",
            Tags=Tags(
                Name=Join(".", [
                    Ref(AWS_STACK_NAME),
                    ImportValue("master-zone-internal-name")
                ]),
                Ansible="true",
            ),
            SecurityGroupIds=[
                Ref(self.VpnSG)
            ],
            SubnetId=ImportValue("master-subnet-shared-public-a"),
            ImageId=Ref(parameters.InstanceImage.title),
            IamInstanceProfile=ImportValue("iam-role-ec2-baseline"),
            SourceDestCheck=False,
            BlockDeviceMappings=[
                ec2.BlockDeviceMapping(
                    DeviceName="/dev/sda1",
                    Ebs=ec2.EBSBlockDevice(
                        VolumeSize=Ref(parameters.InstanceStorageOS.title),
                        VolumeType="gp2"
                )),
            ],
            KeyName=Ref(parameters.InstanceKeyPair.title),
            InstanceType=Ref(parameters.InstanceType.title)
        )

        self.VpnInstanceEIP = ec2.EIP(
            "VpnInstanceEIP",
            InstanceId=Ref(self.VpnInstance),
            Domain="vpc",
        )

        self.VpnPrivateRecord = route53.RecordSetType(
            "VpnPrivateRecord",
            HostedZoneId=ImportValue("master-zone-internal-id"),
            Name=Join(".", [
                Ref(AWS_STACK_NAME),
                ImportValue("master-zone-internal-name")
            ]),
            ResourceRecords=[GetAtt(self.VpnInstance, "PrivateIp")],
            Type="A",
            TTL="3600",
        )
        
        self.VpnPublicRecord = route53.RecordSetType(
            "VpnPublicRecord",
            HostedZoneId=FindInMap("VPCResourcesMap", Ref(parameters.VPC.title), "Route53PublicZone"),
            Name=Join(".", [
                Ref(AWS_STACK_NAME),
                ImportValue("master-zone-internal-name")
            ]),
            ResourceRecords=[Ref(self.VpnInstanceEIP)],
            Type="A",
            TTL="3600",
        )
