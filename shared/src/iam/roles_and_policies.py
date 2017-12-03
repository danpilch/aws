#!/usr/bin/env python
import sys 
sys.path.append("../../../")

from awacs import aws
from troposphere import AWS_STACK_NAME, iam, Ref, Join, AccountId

from helpers.magicdict import MagicDict
from parameters import Parameters
from groups import Groups


class RolesAndPolicies(MagicDict):
    def __init__(self, parameters, groups):
        """
        :type parameters Parameters
        :type groups Groups
        """

        super(RolesAndPolicies, self).__init__()

        self.EC2Baseline = iam.Role(
            "EC2Baseline",
            AssumeRolePolicyDocument=aws.Policy(
                Version="2012-10-17",
                Statement=[
                    aws.Statement(
                        Action=[aws.Action("sts", "AssumeRole")],
                        Effect=aws.Allow,
                        Principal=aws.Principal(
                            "Service", "ec2.amazonaws.com"
                        )
                    )
                ],
            )
        )

        self.LambdaBasicExecution = iam.Role(
            "LambdaBasicExecution",
            AssumeRolePolicyDocument=aws.Policy(
                Version="2012-10-17",
                Statement=[
                    aws.Statement(
                        Action=[aws.Action("sts", "AssumeRole")],
                        Effect=aws.Allow,
                        Principal=aws.Principal(
                            "Service", "lambda.amazonaws.com"
                        )
                    )
                ],
            ),

        )
        
        self.ECSClusterServiceRole = iam.Role(
            "ECSClusterServiceRole",
            Policies=[
                iam.Policy(
                    PolicyName=Join("", [Ref(AWS_STACK_NAME), "-ecs-service"]),
                    PolicyDocument=aws.Policy(
                        Version="2012-10-17",
                        Statement=[
                            aws.Statement(
                                Action=[
                                    aws.Action("ec2", "AuthorizeSecurityGroupIngress"),
                                    aws.Action("ec2", "Describe*"),
                                    aws.Action("elasticloadbalancing", "DeregisterInstancesFromLoadBalancer"),
                                    aws.Action("elasticloadbalancing", "Describe*"),
                                    aws.Action("elasticloadbalancing", "RegisterInstancesWithLoadBalancer"),
                                    aws.Action("elasticloadbalancing", "DeregisterTargets"),
                                    aws.Action("elasticloadbalancing", "DescribeTargetGroups"),  # todo: remove
                                    aws.Action("elasticloadbalancing", "DescribeTargetHealth"),  # todo: remove
                                    aws.Action("elasticloadbalancing", "RegisterTargets"),
                                ],
                                Resource=["*"],
                                Effect=aws.Allow
                            )
                        ]
                    )
                )
            ],
            AssumeRolePolicyDocument=aws.Policy(
                Version="2012-10-17",
                Statement=[
                    aws.Statement(
                        Action=[aws.Action("sts", "AssumeRole")],
                        Effect=aws.Allow,
                        Principal=aws.Principal(
                            "Service", "ecs.amazonaws.com"
                        )
                    )
                ],
            )
        )
        
        self.ForceMFA= iam.ManagedPolicy(
            "ForceMFA",
            PolicyDocument=aws.Policy(
                Version="2012-10-17",
                Statement=[
                    aws.Statement(
                        Sid="AllowAllUsersToListAccounts",
                        Action=[
                            aws.Action("iam", "ListAccountAliases"),
                            aws.Action("iam", "ListUsers"),
                            aws.Action("iam", "GetAccountSummary"),
                        ],
                        Resource=["*"],
                        Effect=aws.Allow
                    ),
                    aws.Statement(
                        Sid="AllowIndividualUserToSeeAndManageOnlyTheirOwnAccountInformation",
                        Action=[
                            aws.Action("iam", "ChangePassword"),
                            aws.Action("iam", "CreateAccessKey"),
                            aws.Action("iam", "CreateLoginProfile"),
                            aws.Action("iam", "DeleteAccessKey"),
                            aws.Action("iam", "DeleteLoginProfile"),
                            aws.Action("iam", "GetAccountPasswordPolicy"),
                            aws.Action("iam", "GetLoginProfile"),
                            aws.Action("iam", "ListAccessKeys"),
                            aws.Action("iam", "UpdateAccessKey"),
                            aws.Action("iam", "UpdateLoginProfile"),
                            aws.Action("iam", "ListSigningCertificates"),
                            aws.Action("iam", "DeleteSigningCertificate"),
                            aws.Action("iam", "UpdateSigningCertificate"),
                            aws.Action("iam", "UploadSigningCertificate"),
                            aws.Action("iam", "ListSSHPublicKeys"),
                            aws.Action("iam", "GetSSHPublicKey"),
                            aws.Action("iam", "DeleteSSHPublicKey"),
                            aws.Action("iam", "UpdateSSHPublicKey"),
                            aws.Action("iam", "UploadSSHPublicKey"),
                        ],
                        Resource=[Join("", ["arn:aws:iam::", AccountId, ":user/${aws:username}"])],
                        Effect=aws.Allow
                    ),
                    aws.Statement(
                        Sid="AllowIndividualUserToListOnlyTheirOwnMFA",
                        Action=[
                            aws.Action("iam", "ListVirtualMFADevices"),
                            aws.Action("iam", "ListMFADevices"),
                        ],
                        Resource=[
                            Join("", ["arn:aws:iam::", AccountId, ":mfa/*"]),
                            Join("", ["arn:aws:iam::", AccountId, ":user/${aws:username}"])
                        ],
                        Effect=aws.Allow
                    ),
                    aws.Statement(
                        Sid="AllowIndividualUserToDeactivateOnlyTheirOwnMFAOnlyWhenUsingMFA",
                        Action=[
                            aws.Action("iam", "DeactivateMFADevice"),
                        ],
                        Condition=aws.Condition(
                            aws.Bool("aws:MultiFactorAuthPresent", True)
                        ),
                        Resource=[
                            Join("", ["arn:aws:iam::", AccountId, ":mfa/${aws:username}"]),
                            Join("", ["arn:aws:iam::", AccountId, ":user/${aws:username}"])
                        ],
                        Effect=aws.Allow
                    ),
                    aws.Statement(
                        Sid="BlockAnyAccessOtherThanAboveUnlessSignedInWithMFA",
                        Condition=aws.Condition(
                            aws.BoolIfExists("aws:MultiFactorAuthPresent", False)
                        ),
                        NotAction=[
                            aws.Action("iam", "*"),
                        ],
                        Resource=["*"],
                        Effect=aws.Deny
                    ),
                ],

            ),
            Description="Forces MFA usage on all users in assigned groups",
            Groups=[
                Ref(groups.AWSEngineers.title),
                Ref(groups.ReadOnlyUsers.title),
            ],
        )

        self.FullAdministrator = iam.ManagedPolicy(
            "FullAdministrator",
            PolicyDocument=aws.Policy(
                Version="2012-10-17",
                Statement=[
                    aws.Statement(
                        Action=[
                            aws.Action("*")
                        ],
                        Resource=["*"],
                        Effect=aws.Allow
                    )
                ]
            ),
            Description="Allows full access to all AWS",
            Groups=[
                Ref(groups.AWSEngineers.title),
            ],
        )
        
        self.CIDeploymentPolicy = iam.ManagedPolicy(
            "CIDeploymentPolicy",
            PolicyDocument=aws.Policy(
                Version="2012-10-17",
                Statement=[
                    aws.Statement(
                        Action=[
                            aws.Action("cloudformation", "DescribeStacks"),
                            aws.Action("cloudformation", "DescribeStackEvents"),
                            aws.Action("cloudformation", "DescribeStackResources"),
                            aws.Action("cloudformation", "DescribeChangeSet"),
                            aws.Action("cloudformation", "GetTemplate"),
                            aws.Action("cloudformation", "GetTemplateSummary"),
                            aws.Action("cloudformation", "List*"),
                            aws.Action("cloudformation", "PreviewStackUpdate"),
                            aws.Action("cloudformation", "CancelUpdateStack"),
                            aws.Action("cloudformation", "ContinueUpdateRollback"),
                            aws.Action("cloudformation", "CreateChangeSet"),
                            aws.Action("cloudformation", "CreateStack"),
                            aws.Action("cloudformation", "CreateUploadBucket"),
                            aws.Action("cloudformation", "ExecuteChangeSet"),
                            aws.Action("cloudformation", "SignalResource"),
                            aws.Action("cloudformation", "UpdateStack"),
                            aws.Action("cloudformation", "ValidateTemplate"),
                            aws.Action("cloudformation", "SetStackPolicy"),
                            aws.Action("ecs", "Describe*"),
                            aws.Action("ecs", "RegisterTaskDefinition"),
                            aws.Action("ecs", "UpdateService"),
                            aws.Action("ecs", "List*"),
                            aws.Action("ecs", "DeregisterTaskDefinition"),
                            aws.Action("ecs", "DiscoverPollEndpoint"),
                            aws.Action("ecs", "Poll"),
                            aws.Action("ecr", "DescribeRepositories"),
                            aws.Action("ecr", "ListImages"),
                            aws.Action("ecr", "BatchCheckLayerAvailability"),
                            aws.Action("ecr", "BatchGetImage"),
                            aws.Action("ecr", "GetAuthorizationToken"),
                            aws.Action("ecr", "GetDownloadUrlForLayer"),
                            aws.Action("ecr", "GetRepositoryPolicy"),
                            aws.Action("ecr", "CompleteLayerUpload"),
                            aws.Action("ecr", "InitiateLayerUpload"),
                            aws.Action("ecr", "PutImage"),
                            aws.Action("ecr", "UploadLayerPart"),
                            aws.Action("logs", "Describe*"),
                        ],
                        Resource=["*"],
                        Effect=aws.Allow
                    )
                ]
            ),
            Description="Allows access to cloudformation for CircleCI",
            Groups=[
                Ref(groups.CIDeploymentServices.title),
            ],
        )

        self.S3Administrator = iam.ManagedPolicy(
            "S3Administrator",
            PolicyDocument=aws.Policy(
                Version="2012-10-17",
                Statement=[
                    aws.Statement(
                        Action=[
                            aws.Action("s3", "*"),
                        ],
                        Resource=["*"],
                        Effect=aws.Allow
                    )
                ]
            ),
            Description="Allows full management of S3",
            Groups=[
                Ref(groups.AWSEngineers.title)
            ],
            Users=[
            ],
        )

        self.LoggingAndMonitoring = iam.ManagedPolicy(
            "LoggingAndMonitoring",
            PolicyDocument=aws.Policy(
                Version="2012-10-17",
                Statement=[
                    aws.Statement(
                        Action=[
                            aws.Action("cloudwatch", "GetMetricStatistics"),
                            aws.Action("cloudwatch", "ListMetrics"),
                            aws.Action("cloudwatch", "PutMetricData"),
                            aws.Action("ec2", "DescribeTags"),
                            aws.Action("logs", "CreateLogGroup"),
                            aws.Action("logs", "CreateLogStream"),
                            aws.Action("logs", "DescribeLogGroups"),
                            aws.Action("logs", "DescribeLogStreams"),
                            aws.Action("logs", "PutLogEvents"),
                            aws.Action("sns", "Publish"),
                        ],
                        Resource=["*"],
                        Effect=aws.Allow
                    )
                ]
            ),
            Description="Allows ingestion of logs and metrics into CloudWatch and publishing to SNS topics",
            Roles=[Ref(self.EC2Baseline)],
        )
