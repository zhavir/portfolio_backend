import aws_cdk as cdk
from aws_cdk import Duration, aws_iam


class IAMStack(cdk.Stack):
    def __init__(self, scope: cdk.App, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        provider = aws_iam.OpenIdConnectProvider.from_open_id_connect_provider_arn(
            self, "GitHub", "arn:aws:iam::992382494893:oidc-provider/token.actions.githubusercontent.com"
        )
        organization = "zhavir"
        repository = "portfolio_backend"
        aws_iam.Role(
            self,
            "GitHubPortfolioBackend",
            role_name="GitHubPortfolioBackend",
            description="Role assumed for deploying from GitHub CI using AWS CDK",
            assumed_by=aws_iam.OpenIdConnectPrincipal(provider).with_conditions(
                conditions={
                    "StringLike": {
                        "token.actions.githubusercontent.com:sub": f"repo:{organization}/{repository}:ref:refs/heads/main",
                    },
                    "StringEquals": {
                        "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
                    },
                }
            ),
            max_session_duration=Duration.hours(1),
            inline_policies={
                "CDKDeploymentPolicy": aws_iam.PolicyDocument(
                    assign_sids=True,
                    statements=[
                        aws_iam.PolicyStatement(
                            effect=aws_iam.Effect.ALLOW,
                            actions=[
                                "cloudformation:DeleteStack",
                                "cloudformation:DescribeStackEvents",
                                "cloudformation:DescribeStackResources",
                                "cloudformation:DescribeStacks",
                                "cloudformation:GetTemplate",
                                "cloudformation:ListImports",
                                "ecr:CreateRepository",
                                "iam:PassRole",
                                "it:Connect",
                                "it:DescribeEndpoint",
                                "it:Publish",
                                "it:Receive",
                                "it:Subscribe",
                                "lambda:GetFunction",
                                "lambda:GetFunctionConfiguration",
                                "lambda:UpdateFunctionConfiguration",
                                "s3:ListBucket",
                                "s3:PutObjectAcl",
                                "s3:GetObject",
                                "s3:PutObject",
                                "s3:DeleteObject",
                                "s3:ListObjectsV2",
                                "s3:CreateBucket",
                                "s3:PutBucketPolicy",
                                "ssm:DeleteParameter",
                                "ssm:GetParameter",
                                "ssm:GetParameters",
                                "ssm:GetParametersByPath",
                                "ssm:PutParameter",
                                "sts:AssumeRole",
                            ],
                            resources=["*"],
                        )
                    ],
                )
            },
        )
