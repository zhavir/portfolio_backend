import aws_cdk as cdk
from iam import IAMStack
from stack import ApiStack

app = cdk.App()

IAMStack(app, "IAMStack")
ApiStack(app, "ApiStack")

app.synth()
