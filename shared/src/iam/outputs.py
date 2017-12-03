#!/usr/bin/env python
import sys 
sys.path.append("../../../")

from troposphere import Output, Ref, Export, GetAtt

from helpers.magicdict import MagicDict
from groups import Groups
from roles_and_policies import RolesAndPolicies
from users import Users


class Outputs(MagicDict):
    def __init__(self, groups, roles, users):
        super(Outputs, self).__init__()

        self.EC2BaselineProfile = Output(
            "EC2BaselineProfile",
            Description="Allows EC2 instances to use the role created by this stack",
            Value=Ref(users.EC2BaselineProfile),
            Export=Export("iam-role-ec2-baseline")
        )

        self.ECSClusterServiceRole = Output(
            "ECSClusterServiceRole",
            Description="Allows ECS services to use the role created by this stack",
            Value=Ref(roles.ECSClusterServiceRole),
            Export=Export("iam-role-ecs-service")
        )
