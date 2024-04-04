import { LambdaRestApi } from "aws-cdk-lib/aws-apigateway";
import { Runtime } from "aws-cdk-lib/aws-lambda";
import { PythonFunction } from "@aws-cdk/aws-lambda-python-alpha"
import { StackContext } from "sst/constructs";

export function Site({ app, stack }: StackContext) {
  
  const lambdaFunction = new PythonFunction(stack, 'Function', {
    entry: 'src',
    runtime: Runtime.PYTHON_3_12,
    index: 'app/sst.py',
    environment: {application_version: process.env.APPLICATION_VERSION || "0.1.0", application_environment: "prod"},
    bundling: {
      assetExcludes: ["tests", ".ruff_cache", ".pytest_cache", "__pycache__"]
    },
  });
  const gateway = new LambdaRestApi(stack, "API", {handler: lambdaFunction})
  stack.addOutputs({
    GatewayUrl: gateway.url,
  });
}
