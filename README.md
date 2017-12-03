# AWS Cloudformation Templates

[![N|Slid](https://avatars0.githubusercontent.com/u/19900777?s=400&v=4)](https://aws.amazon.com/cloudformation/)

This repo is to aid in setting up a new AWS account from scratch.

### Installation

[Troposphere](https://github.com/cloudtools/troposphere) is required to generate all Cloudformation templates in this repo. 

To install Troposphere:

```sh
$ pip install --user troposphere
```

### Generating templates

To output a Troposphere template as Cloudformation JSON compatible, execute the `__main__.py` in the root of each directory, for example:

```sh
$ cd iam 
$ python __main__.py > iam.py
```

You will now have a cloudformation template that is ready to be ran inside AWS.

### Setting up environment

In this guide, we will be setting up a development account (dev)

#### Route 53 domain

Firstly, I would suggest setting up a new domain in Route 53 that can be used with the stacks we will be creating. You can obviously use an already registered domain however this guide is aimed at setting up a brand new AWS account.

#### Stack Naming conventions

General rule of thumb, when creating stacks I usually go with this naming format:

`ORG_NAME-STACK-ENV-INCREMENTIAL_NUMBER`

So for example, for an IAM stack:

`ctrl-iam-dev`

If there were to be more than one stack, perhaps you're creating multiple environments, you can add an incremental number to the end:

`ctrl-iam-dev-01`
`ctrl-iam-dev-02`

If you are creating stacks in multiple regions, you can also add a region to the stack name e.g.

`ctrl-iam-dev-syd-01`

#### Stack Tagging conventions

When creating CloudFormation stacks, it is useful to define tags so that all resources are trackable for billing and searching purposes. I usually go with these four standard tags:

| Tag        | Value           | Description  |
| ------------- |-------------| -----|
| Name  | `ctrl-iam-dev-01` | Name of the stack |
| Service      | `ctrl-iam-dev-01`      |  Service name (generally the same as Name)|
| Owner | `ctrl`      | The owner (usually the business name) |
| Environment | `dev` | The environment this account is servicing e.g. dev, stage, prod |

#### IAM stack

Update `users.py` with at least one new user. (You can use `DanielPilch` as an example, don't forget to remove it!). 

Next step is to run the stack into CloudFormation via the console. You will need to specify a default user password; make a note of it as all new Users you add to the stack will use this password initially!

##### MFA Authentication
Once the stack has been deployed, all new users will be forced to use MFA authentication for security. Try and log out of the root account and lop in with the user you created in the IAM stack. Once you have logged in, no resources will be available until you have enabled MFA under IAM.

#### Networking stack

Firstly, Update `helpers/mappings.py` and update `self.AWSDevAccountId` with your account ID. Next, update `Route53PublicZone` with the ID of the zone you created before.



