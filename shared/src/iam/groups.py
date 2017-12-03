#!/usr/bin/env python
import sys 
sys.path.append("../../../")

from troposphere import iam

from helpers.magicdict import MagicDict


class Groups(MagicDict):
    def __init__(self, parameters):
        super(Groups, self).__init__()

        self.ReadOnlyUsers = iam.Group(
            "ReadOnlyUsers",
            ManagedPolicyArns=["arn:aws:iam::aws:policy/ReadOnlyAccess"],
        )

        self.AWSEngineers = iam.Group(
            "AWSEngineers",
        )

        self.CIDeploymentServices = iam.Group(
            "CIDeploymentServices",
        )
