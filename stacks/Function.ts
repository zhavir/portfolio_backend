import { Runtime } from 'aws-cdk-lib/aws-lambda';
import { PythonFunction } from '@aws-cdk/aws-lambda-python-alpha';
import { StackContext } from 'sst/constructs';
import * as sns from 'aws-cdk-lib/aws-sns';
import * as subscriptions from 'aws-cdk-lib/aws-sns-subscriptions';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as ssm from 'aws-cdk-lib/aws-ssm';

export function Site({ stack }: StackContext) {
  const emailSNSTopic = new sns.Topic(stack, 'EmailTopic');
  const domainName = 'andreaaramini.space';
  if (process.env.PERSONAL_EMAIL_SUBSCRIPTION) {
    emailSNSTopic.addSubscription(
      new subscriptions.EmailSubscription(
        process.env.PERSONAL_EMAIL_SUBSCRIPTION,
      ),
    );
  }

  const lambdaFunction = new PythonFunction(stack, 'Function', {
    entry: 'src',
    runtime: Runtime.PYTHON_3_12,
    index: 'app/sst.py',
    environment: {
      application_version: process.env.APPLICATION_VERSION || '0.1.0',
      application_environment: 'prod',
      application_allow_origin: `https://${domainName}`,
      application_cv_download_link: process.env.CV_DOWNLOAD_LINK || '',
      aws_email_topic_arn: emailSNSTopic.topicArn,
    },
    bundling: {
      assetExcludes: ['tests', '.ruff_cache', '.pytest_cache', '__pycache__'],
    },
    memorySize: 512,
  });
  lambdaFunction.addPermission('APIGateway', {
    principal: new iam.ServicePrincipal('apigateway.amazonaws.com'),
  });
  const snsTopicPolicy = new iam.PolicyStatement({
    actions: ['sns:publish'],
    resources: [emailSNSTopic.topicArn],
  });
  lambdaFunction.addToRolePolicy(snsTopicPolicy);
  new ssm.StringParameter(stack, 'portfolioBackendLambdaArn', {
    parameterName: 'portfolioBackendLambdaArn',
    stringValue: lambdaFunction.functionArn,
  });
}
