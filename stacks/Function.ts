import { LambdaRestApi } from 'aws-cdk-lib/aws-apigateway';
import { Runtime } from 'aws-cdk-lib/aws-lambda';
import { PythonFunction } from '@aws-cdk/aws-lambda-python-alpha';
import { StackContext } from 'sst/constructs';
import { Duration } from 'aws-cdk-lib';
import * as sns from 'aws-cdk-lib/aws-sns';
import * as subscriptions from 'aws-cdk-lib/aws-sns-subscriptions';
import * as iam from 'aws-cdk-lib/aws-iam';

export function Site({ app, stack }: StackContext) {
  const emailSNSTopic = new sns.Topic(stack, 'EmailTopic');

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
      aws_email_topic_arn: emailSNSTopic.topicArn,
    },
    bundling: {
      assetExcludes: ['tests', '.ruff_cache', '.pytest_cache', '__pycache__'],
    },
  });
  const snsTopicPolicy = new iam.PolicyStatement({
    actions: ['sns:publish'],
    resources: [emailSNSTopic.topicArn],
  });
  lambdaFunction.addToRolePolicy(snsTopicPolicy);
  const gateway = new LambdaRestApi(stack, 'API', {
    handler: lambdaFunction,
    integrationOptions: {
      timeout: Duration.seconds(10),
    },
  });
  stack.addOutputs({
    GatewayUrl: gateway.url,
  });
}
