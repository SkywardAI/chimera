# coding=utf-8

# Copyright [2024] [SkywardAI]
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import loguru

from src.config.manager import settings
from src.utilities.httpkit.httpx_kit import httpx_kit



async def dispose_httpx_client() -> None:
    loguru.logger.info("Httpx Client --- Disposing . . .")

    close_async = await httpx_kit.teardown_async_client()

    loguru.logger.info(
        "Httpx Async Client --- Successfully Disposed!" if close_async else "Httpx Async Client --- Failed to Dispose!"
    )

    close_sync = httpx_kit.teardown_sync_client()

    loguru.logger.info(
        "Httpx Sync Client --- Successfully Disposed!" if close_sync else "Httpx Sync Client --- Failed to Dispose!"
    )
