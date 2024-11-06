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


import pydantic

from src.config.manager import settings


class InferenceHelper:
    infer_eng_url: pydantic.StrictStr = settings.INFERENCE_ENG
    infer_eng_port: pydantic.PositiveInt = settings.INFERENCE_ENG_PORT
    instruction: pydantic.StrictStr = settings.INSTRUCTION


    def init(self) -> None:
        raise NotImplementedError("InferenceHelper is a singleton class. Use inference_helper instead.")

    @classmethod
    def instruct_infer_url(cls) -> str:
        """
        Get the URL for the inference engine

        Returns:
        str: URL for the inference engine
        """
        return f"http://{cls.infer_eng_url}:{cls.infer_eng_port}/completion"