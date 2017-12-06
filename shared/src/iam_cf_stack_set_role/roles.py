#!/usr/bin/env python
import sys 
sys.path.append("../../../")

from awacs import aws
from troposphere import iam, Ref

from helpers.magicdict import MagicDict


class StackSetRole(MagicDict):
    def __init__(self, parameters):
        super(StackSetRole, self).__init__()

        self.AdministrationRole = iam.Role(
            "AdministrationRole",
            RoleName="AWSCloudFormationStackSetAdministrationRole",
            Path="/",
            AssumeRolePolicyDocument=aws.Policy(
                Version="2012-10-17",
                Statement=[
                    aws.Statement(
                        Action=[aws.Action("sts", "AssumeRole")],
                        Effect=aws.Allow,
                        Principal=aws.Principal(
                            "Service", "cloudformation.amazonaws.com"
                        )
                    )
                ],
            ),
            Policies=[
                iam.Policy(
                    PolicyName="AssumeRole-AWSCloudFormationStackSetExecutionRole",
                    PolicyDocument=aws.Policy(
                        Version="2012-10-17",
                        Statement=[
                            aws.Statement(
                                Action=[aws.Action("sts", "AssumeRole")],
                                Effect=aws.Allow,
                                Resource=["arn:aws:iam::*:role/AWSCloudFormationStackSetExecutionRole"],
                            )
                        ]
                    ),
                )
            ]
        )

        self.ExecutionRole = iam.Role(
            "ExecutionRole",
            RoleName="AWSCloudFormationStackSetExecutionRole",
            Path="/",
            ManagedPolicyArns=["arn:aws:iam::aws:policy/AdministratorAccess"],
            AssumeRolePolicyDocument=aws.Policy(
                Version="2012-10-17",
                Statement=[
                    aws.Statement(
                        Action=[aws.Action("sts", "AssumeRole")],
                        Effect=aws.Allow,
                        Principal=aws.Principal(
                            "AWS", Ref(parameters.AdministratorAccountId)
                        )
                    )
                ]
            )
        )

