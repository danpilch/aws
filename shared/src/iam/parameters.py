#!/usr/bin/env python
import sys 
sys.path.append("../../../")

from troposphere import Parameter
from helpers.magicdict import MagicDict


class Parameters(MagicDict):
    def __init__(self):
        super(Parameters, self).__init__()

        self.DefaultPassword = Parameter(
            "DefaultPassword",
            NoEcho=True,
            Type="String",
            ConstraintDescription="The password must be at least 12 characters long",
            Description="Password to use for new IAM accounts",
            MinLength="12",
        )
