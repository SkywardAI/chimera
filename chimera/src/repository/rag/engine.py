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

from typing import Any
from collections.abc import AsyncGenerator
import loguru
import httpx
import json
from src.repository.rag.base import BaseRAGRepository
from src.repository.inference_eng import InferenceHelper
from src.utilities.httpkit.httpx_kit import httpx_kit
from src.utilities.formatters.ds_formatter import DatasetFormatter


class RAGChatModelRepository(BaseRAGRepository):
    def format_prompt(self, prmpt: str, current_context: str = InferenceHelper.instruction) -> str:
        """
        Format the input questions, can be used for saving the conversation history

        Args:
        prmpt (str): input message
        current_context (str): the context we got from the vector database

        Returns:
        str: formatted prompt
        """
        return f"### System: {current_context}\n" + f"\n### Human: {prmpt}\n### Assistant:"

    def inference(
        self,
        input_msg: str,
        temperature: float = 0.2,
        top_k: int = 40,
        top_p: float = 0.9,
        n_predict: int = 128,
    ) -> str:
        """
        **Inference using seperate service:(llamacpp)**

        **Args:**
        - **session_id (int):** session id
        - **input_msg (str):** input message
        - **chat_repo:** chat repository
        - **temperature (float):** temperature for inference(float)
        - **top_k (int):** top_k parameter for inference(int)
        - **top_p (float):** top_p parameter for inference(float)
        - **n_predict (int):** n_predict parameter for inference(int)

        **Returns:**
        str: response message
        """

        data = {
            "prompt": self.format_prompt(input_msg),
            "temperature": temperature,
            "top_k": top_k,
            "top_p": top_p,
            "n_keep": 0,  # If the context window is full, we keep 0 tokens
            "n_predict": 128 if n_predict == 0 else n_predict,
            "cache_prompt": True,
            "slot_id": -1,  # for cached prompt
            "stop": ["\n### Human:"],
            "stream": True,
        }
        try:
            with httpx.Client() as client:
                response = client.post(
                    InferenceHelper.instruct_infer_url(),
                    headers={"Content-Type": "application/json"},
                    json=data,
                    timeout=httpx.Timeout(timeout=None),
                )
                lines = response.content.decode('utf-8').splitlines()
                combined_content = ""
                for line in lines:
                    if line.startswith('data: '):
                        json_data = json.loads(line[len('data: '):])
                        combined_content += json_data['content']
                return combined_content
        except httpx.ReadError as e:
            loguru.logger.error(f"An error occurred while requesting {e.request.url!r}.")
        except httpx.HTTPStatusError as e:
            loguru.logger.error(f"Error response {e.response.status_code} while requesting {e.request.url!r}.")