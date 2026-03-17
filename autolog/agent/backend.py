from abc import ABC, abstractmethod

import autolog.config as config


class LLMBackend(ABC):
    @abstractmethod
    def generate(self, messages: list[dict], image_path: str | None = None, **kwargs) -> str: ...


class TransformersBackend(LLMBackend):
    def __init__(self) -> None:
        from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

        quant_config = (
            BitsAndBytesConfig(load_in_4bit=True) if config.LOAD_IN_4BIT else None
        )
        self.tokenizer = AutoTokenizer.from_pretrained(config.MODEL_ID)
        self.model = AutoModelForCausalLM.from_pretrained(
            config.MODEL_ID,
            quantization_config=quant_config,
            device_map=config.DEVICE_MAP,
        )

    def generate(self, messages: list[dict], image_path: str | None = None, **kwargs) -> str:
        if image_path is not None:
            raise NotImplementedError("TransformersBackend does not support image input")

        chat_text = self.tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=False,
        )
        inputs = self.tokenizer(chat_text, return_tensors="pt").to(self.model.device)
        input_ids = inputs["input_ids"]

        output_ids = self.model.generate(
            **inputs,
            max_new_tokens=kwargs.get("max_new_tokens", config.MAX_NEW_TOKENS),
        )
        new_tokens = output_ids[0][input_ids.shape[-1]:]
        return self.tokenizer.decode(new_tokens, skip_special_tokens=True)


def get_backend() -> LLMBackend:
    if config.BACKEND == "transformers":
        return TransformersBackend()
    raise ValueError(f"Unknown backend: {config.BACKEND!r}")
