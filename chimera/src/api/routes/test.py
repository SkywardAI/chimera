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

import fastapi
from src.models.schemas.health import HealthCheckResponse


router = fastapi.APIRouter(prefix="/test", tags=["test"])


@router.post("/chat", name="test:chat")
async def health_check() -> HealthCheckResponse:
    """
    Check the health of the service

    ```bash
    curl http://localhost:8000/api/test -> {"status":"ok"}
    ```

    Return:
    - **status**: The status of the service
    """
    return HealthCheckResponse(status="ok")
