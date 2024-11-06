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

from src.api.dependencies.repository import get_rag_repository
from src.models.schemas.health import HealthCheckResponse
from src.repository.rag.engine import RAGChatModelRepository

router = fastapi.APIRouter(prefix="/test", tags=["test"])


@router.post("/chat", name="test:chat")
async def test_chat(
    msg: str,
    rag_chat_repo: RAGChatModelRepository = fastapi.Depends(get_rag_repository(repo_type=RAGChatModelRepository)),
    ) -> HealthCheckResponse:
    """
    Check the health of the service

    ```bash
    curl http://localhost:8000/api/test/chat -> {"status":"ok"}
    ```

    Return:
    - **status**: The status of the service
    """
    result = rag_chat_repo.inference( input_msg=msg )
    print('-------------------------------')
    print(result)
    print('-------------------------------')
    return HealthCheckResponse(status=result)
