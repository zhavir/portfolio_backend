#!/bin/bash
printf "Configuring localstack components...\n"

set +x

awslocal sns create-topic --name ${SNS_TEST_TOPIC_NAME:-EmailTopic} --region us-east-1 --output table | cat
