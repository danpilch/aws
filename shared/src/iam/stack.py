from troposphere import Template, Output, Ref, Export

from parameters import Parameters
from groups import Groups
from roles_and_policies import RolesAndPolicies
from users import Users
from outputs import Outputs


class Stack(object):
    def __init__(self):
        self.template = Template()
        self.template.add_version("2010-09-09")
        self.template.add_description("Create IAM users, groups and policies for environments")

        parameters = Parameters()
        for param in parameters.values():
            self.template.add_parameter(param)

        groups = Groups(parameters=parameters)
        for res in groups.values():
            self.template.add_resource(res)

        roles = RolesAndPolicies(parameters=parameters, groups=groups)
        for res in roles.values():
            self.template.add_resource(res)

        users = Users(parameters=parameters, groups=groups, roles=roles)
        for res in users.values():
            self.template.add_resource(res)

        outputs = Outputs(groups=groups, roles=roles, users=users)
        for res in outputs.values():
            self.template.add_output(res)

