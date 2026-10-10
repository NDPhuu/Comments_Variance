"""Client LLM duy nhat cua he thong (quy tac clean_code #8): moi call deu qua day.

- GeminiClient: goi Google AI Studio (free tier) — doc GEMINI_API_KEY tu app/backend/.env.
- MockClient: tra loi dong san cho test/offline; giu cung interface.
Chi gui du lieu SYNTHETIC len API (quyet dinh #17).
"""

from __future__ import annotations

import json
import os
import re
import time

from dotenv import load_dotenv

from vwb import config


class LLMClient:
    model_id: str = "mock"

    def generate(self, prompt: str) -> str:  # pragma: no cover - interface
        raise NotImplementedError


class MockClient(LLMClient):
    """Tra cac response theo hang doi; mac dinh JSON abstain hop le."""

    def __init__(self, responses: list[str] | None = None):
        self.responses = list(responses or [])
        self.calls: list[str] = []
        self.model_id = "mock"

    def generate(self, prompt: str) -> str:
        self.calls.append(prompt)
        if self.responses:
            return self.responses.pop(0)
        return json.dumps({"draft_comment": "", "abstained": True})


class GeminiClient(LLMClient):
    def __init__(self, model: str | None = None):
        load_dotenv(config.BASE_DIR / ".env")
        key = os.environ.get("GEMINI_API_KEY")
        if not key:
            raise RuntimeError(
                "GEMINI_API_KEY chua co trong app/backend/.env — them dong "
                "GEMINI_API_KEY=<key tu Google AI Studio> roi chay lai."
            )
        from google import genai  # import muon de test khong can SDK hoat dong

        self._genai = genai
        self._client = genai.Client(api_key=key)
        self.model_id = model or config.GEN_MODEL

    def generate(self, prompt: str) -> str:
        last_err: Exception | None = None
        for attempt in range(3):
            try:
                resp = self._client.models.generate_content(
                    model=self.model_id,
                    contents=prompt,
                    config=self._genai.types.GenerateContentConfig(
                        temperature=config.GEN_TEMPERATURE
                    ),
                )
                return resp.text or ""
            except Exception as e:  # rate limit free tier -> cho roi thu lai
                last_err = e
                time.sleep(10 * (attempt + 1))
        raise RuntimeError(f"Gemini loi sau 3 lan thu: {last_err}")


def parse_json_output(text: str) -> dict:
    """Boc JSON tu output LLM (chiu duoc code fence ```json ... ```)."""
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise ValueError(f"khong tim thay JSON trong output: {text[:200]!r}")
    return json.loads(m.group(0))
