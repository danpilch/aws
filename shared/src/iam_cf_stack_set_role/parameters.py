#!/usr/bin/env python
import sys
sys.path.append("../../../")

from troposphere import Parameter
from helpers.magicdict import MagicDict


class Parameters(MagicDict):
    def __init__(self):
        super(Parameters, self).__init__()
        
        self.AdministratorAccountId = Parameter(
            "AdministratorAccountId",
            Description="AWS Account Id of the administrator account (the account in which StackSets will be created).",
            Type="String",
            MaxLength=12,
            MinLength=12
        )
