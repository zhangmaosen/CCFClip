# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import sys

from typing import List

from alibabacloud_dingtalk.contact_1_0.client import Client as dingtalkcontact_1_0Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dingtalk.contact_1_0 import models as dingtalkcontact__1__0_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient


class Sample:
    def __init__(self):
        pass

    @staticmethod
    def create_client() -> dingtalkcontact_1_0Client:
        """
        使用 Token 初始化账号Client
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config()
        config.protocol = 'https'
        config.region_id = 'central'
        return dingtalkcontact_1_0Client(config)

    @staticmethod
    def main(
        args: List[str],
    ) -> None:
        client = Sample.create_client()
        search_user_headers = dingtalkcontact__1__0_models.SearchUserHeaders()
        search_user_headers.x_acs_dingtalk_access_token = 'af69524a98c335b6b743c04290dbd2b1'
        search_user_request = dingtalkcontact__1__0_models.SearchUserRequest(
            query_word='zhangmaosenccf',
            offset=0,
            size=10,
            full_match_field=1
        )
        try:
            return client.search_user_with_options(search_user_request, search_user_headers, util_models.RuntimeOptions())
        except Exception as err:
            if not UtilClient.empty(err.code) and not UtilClient.empty(err.message):
                print(err)# err 中含有 code 和 message 属性，可帮助开发定位问题
                pass

    @staticmethod
    async def main_async(
        args: List[str],
    ) -> None:
        client = Sample.create_client()
        search_user_headers = dingtalkcontact__1__0_models.SearchUserHeaders()
        search_user_headers.x_acs_dingtalk_access_token = 'af69524a98c335b6b743c04290dbd2b1'
        search_user_request = dingtalkcontact__1__0_models.SearchUserRequest(
            query_word='小红',
            offset=0,
            size=10,
            full_match_field=1
        )
        try:
            await client.search_user_with_options_async(search_user_request, search_user_headers, util_models.RuntimeOptions())
        except Exception as err:
            if not UtilClient.empty(err.code) and not UtilClient.empty(err.message):
                # err 中含有 code 和 message 属性，可帮助开发定位问题
                pass


if __name__ == '__main__':
    print(Sample.main(sys.argv[1:]))