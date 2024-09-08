# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import sys

from typing import List

from alibabacloud_dingtalk.drive_1_0.client import Client as dingtalkdrive_1_0Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dingtalk.drive_1_0 import models as dingtalkdrive__1__0_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient


class Sample:
    def __init__(self):
        pass

    @staticmethod
    def create_client() -> dingtalkdrive_1_0Client:
        """
        使用 Token 初始化账号Client
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config()
        config.protocol = 'https'
        config.region_id = 'central'
        return dingtalkdrive_1_0Client(config)

    @staticmethod
    def main(
        args: List[str],
    ) -> None:
        client = Sample.create_client()
        add_space_headers = dingtalkdrive__1__0_models.AddSpaceHeaders()
        add_space_headers.x_acs_dingtalk_access_token = 'd6b6ac7bf5833a8ea091436adf4e4518'
        add_space_request = dingtalkdrive__1__0_models.AddSpaceRequest(
            name='maosen',
            union_id='sKUPRiijiSrqsuwqcPiSdbeNwiXxx'
        )
        try:
            return client.add_space_with_options(add_space_request, add_space_headers, util_models.RuntimeOptions())
        except Exception as err:
            if not UtilClient.empty(err.code) and not UtilClient.empty(err.message):
                # err 中含有 code 和 message 属性，可帮助开发定位问题
                pass

    @staticmethod
    async def main_async(
        args: List[str],
    ) -> None:
        client = Sample.create_client()
        add_space_headers = dingtalkdrive__1__0_models.AddSpaceHeaders()
        add_space_headers.x_acs_dingtalk_access_token = 'd6b6ac7bf5833a8ea091436adf4e4518'
        add_space_request = dingtalkdrive__1__0_models.AddSpaceRequest(
            name='maosen',
            union_id='sKUPRiijiSrqsuwqcPiSdbeNwiXxx'
        )
        try:
            await client.add_space_with_options_async(add_space_request, add_space_headers, util_models.RuntimeOptions())
        except Exception as err:
            if not UtilClient.empty(err.code) and not UtilClient.empty(err.message):
                # err 中含有 code 和 message 属性，可帮助开发定位问题
                pass


if __name__ == '__main__':
    print(Sample.main(sys.argv[1:]))