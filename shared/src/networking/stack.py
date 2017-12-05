from troposphere import Template, Equals, Ref

from parameters import Parameters
from outputs import Outputs
from vpc import Vpc


class Stack(object):
    def __init__(self):
        self.template = Template()
        self.template.add_version("2010-09-09")
        self.template.add_description("Create resources for the \
AWS account environment. Includes VPC, shared services and network elements")

        parameters = Parameters()
        vpc = Vpc(parameters=parameters)
        outputs = Outputs(vpc=vpc, parameters=parameters)

        for resource in parameters.values():
            self.template.add_parameter(resource)
        
        # Condition to specify whether NAT gateways should be deployed (NAT GWs cost $$$)
        self.template.add_condition("DeployNATGateways", Equals(Ref(parameters.DeployNATGateways), "true"))

        # Condition to specify whether to create a production route53 zone
        self.template.add_condition("CreateProductionZone", Equals(Ref(parameters.Environment), "prod")) 
        
        for resource in vpc.values():
            self.template.add_resource(resource)

        for res in outputs.values():
            self.template.add_output(res)



        self.template.add_metadata({
            "AWS::CloudFormation::Interface": {
                "ParameterGroups": [
                    {
                        "Label": {"default": "Availability Zones"},
                        "Parameters": ["AvailabilityZoneA", "AvailabilityZoneB"]
                    },
                    {
                        "Label": {"default": "Environment"},
                        "Parameters": ["Environment"]
                    },
                    {
                        "Label": {"default": "Domain"},
                        "Parameters": ["DomainName"]
                    },
                    {
                        "Label": {"default": "NAT Gateway"},
                        "Parameters": ["DeployNATGateways"]
                    },
                    {
                        "Label": {"default": "VPC"},
                        "Parameters": ["VPCCIDR"]
                    },
                    {
                        "Label": {"default": "Private Subnets"},
                        "Parameters": ["GeneralPrivateSubnetACIDR", "GeneralPrivateSubnetBCIDR"]
                    },
                    {
                        "Label": {"default": "Shared Services Public Subnets"},
                        "Parameters": ["SharedServicesPublicSubnetACIDR", "SharedServicesPublicSubnetBCIDR"]
                    },
                    {
                        "Label": {"default": "Shared Services Private Subnets"},
                        "Parameters": ["SharedServicesPrivateSubnetACIDR", "SharedServicesPrivateSubnetBCIDR"]
                    },
                    {
                        "Label": {"default": "Load Balancer Subnets"},
                        "Parameters": ["LBSubnetACIDR", "LBSubnetBCIDR"]
                    },
                ]
            }
        })
