import { Duration } from 'aws-cdk-lib';
import * as iam from 'aws-cdk-lib/aws-iam';
import { Stack, StackContext } from 'sst/constructs';
import * as ssm from 'aws-cdk-lib/aws-ssm';
import { IOpenIdConnectProvider } from 'aws-cdk-lib/aws-iam';

function getProvider(stack: Stack): IOpenIdConnectProvider {
  const openIdConnectProviderArn = ssm.StringParameter.valueForStringParameter(
    stack,
    'openIdConnectProviderArn',
  );
  return iam.OpenIdConnectProvider.fromOpenIdConnectProviderArn(
    stack,
    'GitHub',
    openIdConnectProviderArn,
  );
}

export function IAM({ app, stack }: StackContext) {
  if (app.stage === 'production') {
    const provider = getProvider(stack);
    const organization = 'zhavir';
    const repository = 'portfolio_backend';

    new iam.Role(stack, 'GitHubActionsRole', {
      assumedBy: new iam.OpenIdConnectPrincipal(provider).withConditions({
        StringLike: {
          'token.actions.githubusercontent.com:sub': `repo:${organization}/${repository}:ref:refs/heads/main`,
        },
        StringEquals: {
          'token.actions.githubusercontent.com:aud': 'sts.amazonaws.com',
        },
      }),
      description: 'Role assumed for deploying from GitHub CI using AWS CDK',
      roleName: 'GitHubPortfolioBackend',
      maxSessionDuration: Duration.hours(1),
      inlinePolicies: {
        SSTDeploymentPolicy: new iam.PolicyDocument({
          assignSids: true,
          statements: [
            new iam.PolicyStatement({
              effect: iam.Effect.ALLOW,
              actions: [
                'cloudformation:DeleteStack',
                'cloudformation:DescribeStackEvents',
                'cloudformation:DescribeStackResources',
                'cloudformation:DescribeStacks',
                'cloudformation:GetTemplate',
                'cloudformation:ListImports',
                'ecr:CreateRepository',
                'iam:PassRole',
                'it:Connect',
                'it:DescribeEndpoint',
                'it:Publish',
                'it:Receive',
                'it:Subscribe',
                'lambda:GetFunction',
                'lambda:GetFunctionConfiguration',
                'lambda:UpdateFunctionConfiguration',
                's3:ListBucket',
                's3:PutObjectAcl',
                's3:GetObject',
                's3:PutObject',
                's3:DeleteObject',
                's3:ListObjectsV2',
                's3:CreateBucket',
                's3:PutBucketPolicy',
                'ssm:DeleteParameter',
                'ssm:GetParameter',
                'ssm:GetParameters',
                'ssm:GetParametersByPath',
                'ssm:PutParameter',
                'sts:AssumeRole',
              ],
              resources: ['*'],
            }),
          ],
        }),
      },
    });
  }
}
