from typing import Any, Optional

import boto3
import botocore.client
import botocore.session
from fastapi.concurrency import run_in_threadpool
from mypy_boto3_sns import SNSClient

from app.core.settings import get_settings


class BotoClientProxy:
    def __init__(self, region_name: Optional[str] = None, session: Optional[botocore.session.Session] = None) -> None:
        settings = get_settings()
        boto_session = boto3.Session(region_name=region_name, botocore_session=session)

        self._endpoint = settings.aws.endpoint
        self._sns_client: SNSClient = boto_session.client(
            "sns", config=botocore.client.Config(tcp_keepalive=True), endpoint_url=settings.aws.endpoint
        )

    async def send_sns_message(self, *args: Any, **kwargs: Any) -> None:
        await run_in_threadpool(self._sns_client.publish, *args, **kwargs)


def get_boto_client_proxy(
    region_name: Optional[str] = None, session: Optional[botocore.session.Session] = None
) -> BotoClientProxy:
    return BotoClientProxy(region_name=region_name, session=session)
