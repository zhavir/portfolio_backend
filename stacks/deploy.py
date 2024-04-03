import aws_cdk as cdk
from stack import ApiStack

app = cdk.App()
ApiStack(app, "ApiStack")

app.synth()
