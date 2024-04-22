import { Runtime } from 'aws-cdk-lib/aws-lambda';
import { PythonFunction } from '@aws-cdk/aws-lambda-python-alpha';
import { StackContext } from 'sst/constructs';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as sns from 'aws-cdk-lib/aws-sns';
import * as subscriptions from 'aws-cdk-lib/aws-sns-subscriptions';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as route53Targets from 'aws-cdk-lib/aws-route53-targets';
import * as route53 from 'aws-cdk-lib/aws-route53';
import * as acm from 'aws-cdk-lib/aws-certificatemanager';
import * as cdk from 'aws-cdk-lib';

export function Site({ app, stack }: StackContext) {
  const emailSNSTopic = new sns.Topic(stack, 'EmailTopic');
  const domainName = 'andreaaramini.space';
  const apiGatewayAlias = `api.${domainName}`;

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
  const snsTopicPolicy = new iam.PolicyStatement({
    actions: ['sns:publish'],
    resources: [emailSNSTopic.topicArn],
  });
  lambdaFunction.addToRolePolicy(snsTopicPolicy);

  const hostedZone = route53.HostedZone.fromLookup(stack, 'HostedZone', {
    domainName: domainName,
  });
  const certificate = new acm.Certificate(this, 'cert', {
    domainName: apiGatewayAlias,
    validation: acm.CertificateValidation.fromDns(hostedZone),
  });
  const gateway = new apigateway.LambdaRestApi(stack, 'API', {
    handler: lambdaFunction,
    integrationOptions: {
      timeout: cdk.Duration.seconds(10),
    },
    domainName: {
      domainName: apiGatewayAlias,
      certificate: certificate,
      endpointType: apigateway.EndpointType.EDGE,
      securityPolicy: apigateway.SecurityPolicy.TLS_1_2,
    },
    defaultCorsPreflightOptions: {
      allowOrigins: [`https://${domainName}`],
      allowMethods: apigateway.Cors.ALL_METHODS,
      allowHeaders: apigateway.Cors.DEFAULT_HEADERS,
      maxAge: cdk.Duration.days(1),
    },
  });

  const eventRule = new cdk.aws_events.Rule(this, 'LambdaSchedule', {
    schedule: cdk.aws_events.Schedule.rate(cdk.Duration.minutes(5)),
  });
  eventRule.addTarget(
    new cdk.aws_events_targets.ApiGateway(gateway, {
      path: '/api/v1/healthcheck/',
      method: 'GET',
      stage: 'prod',
    }),
  );

  const recordProps = {
    recordName: apiGatewayAlias,
    zone: hostedZone,
    target: route53.RecordTarget.fromAlias(
      new route53Targets.ApiGateway(gateway),
    ),
  };
  new route53.ARecord(stack, 'AlternateARecord', recordProps);
  stack.addOutputs({
    GatewayUrl: gateway.url,
  });
}
