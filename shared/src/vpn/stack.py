from troposphere import Template, Output, GetAtt

from parameters import Parameters
from vpn import Vpn
from helpers.mappings import Mappings


class Stack(object):
    def __init__(self):
        self.template = Template()
        self.template.add_version("2010-09-09")
        self.template.add_description("Creates resources for a Ethereum node")

        parameters = Parameters()
        vpn = Vpn(parameters=parameters)

        for key, value in Mappings().mappings.iteritems():
            self.template.add_mapping(key, value)

        for param in parameters.values():
            self.template.add_parameter(param)
        
        for res in vpn.values():
            self.template.add_resource(res)
        
        self.template.add_metadata({
            "AWS::CloudFormation::Interface": {
                "ParameterGroups": [
                    {
                        "Label": {"default": "EC2"},
                        "Parameters": ["InstanceImage", "InstanceKeyPair", "InstanceStorageData", "InstanceStorageOS", "InstanceType"]
                    },
                    {
                        "Label": {"default": "VPC"},
                        "Parameters": ["VPC"]
                    },
                ]
            }
        })

