from troposphere import Template, Output, Ref, Export

from roles import StackSetRole


class Stack(object):
    def __init__(self):
        self.template = Template()
        self.template.add_version("2010-09-09")
        self.template.add_description("Configure the AWSCloudFormationStackSetAdministrationRole to enable use of AWS CloudFormation StackSets")

        iam_cf_stack_set_role = StackSetRole()
        for res in iam_cf_stack_set_role.values():
            self.template.add_resource(res)
