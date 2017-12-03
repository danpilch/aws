#!/usr/bin/env python
import sys 
sys.path.append("../../../")


from awacs import aws
from troposphere import iam, Ref

from helpers.magicdict import MagicDict
from parameters import Parameters
from groups import Groups
from roles_and_policies import RolesAndPolicies


class Users(MagicDict):
    def __init__(self, parameters, groups, roles):
        super(Users, self).__init__()

        self.DanielPilch = iam.User(
            "DanielPilch",
            Path="/",
            LoginProfile=iam.LoginProfile(
                Password=Ref(parameters.DefaultPassword.title),
                PasswordResetRequired=True
            ),
        )
        

        self.CIUser = iam.User(
            "CIUser",
        )

        # User to group memberships
        self.AWSEngineersMembership = iam.UserToGroupAddition(
            "AWSEngineersMembership",
            GroupName=Ref(groups.AWSEngineers),
            Users=[
                Ref(self.DanielPilch), 
            ],
        )

        self.CIDeploymentMembership = iam.UserToGroupAddition(
            "CIDeploymentMembership",
            GroupName=Ref(groups.CIDeploymentServices),
            Users=[
                Ref(self.CIUser),
            ],
        )

        # EC2 Baseline Instance Profile
        self.EC2BaselineProfile = iam.InstanceProfile(
            "EC2BaselineProfile",
            Path="/",
            Roles=[Ref(roles.EC2Baseline)]
        )
