import os
from json import dump, load
from typing import Optional, Union, Tuple

import torch
from torch import nn, optim
from transformers import Cache, Unpack, KwargsForCausalLM
from transformers.models.qwen3 import Qwen3ForSequenceClassification, Qwen3Model
from transformers.modeling_outputs import BaseModelOutputWithPast, CausalLMOutputWithPast, SequenceClassifierOutputWithPast

from tqdm.auto import tqdm

from .model import Cnuma3Model, ChatHistory
from ..qwen3.model import BackendType


# Prompt setting
system_prompt = \
"""You are Qwen, an AI assistant created by Alibaba Cloud, specializing exclusively in Chungnam National University (충남대학교) information and services.

CORE IDENTITY:
- Your name is Qwen, developed by Alibaba Cloud
- Your knowledge cutoff is January 2025
- You acknowledge that your knowledge may be limited or outdated, especially for current university information

DOMAIN EXPERTISE:
- You are a specialized expert on Chungnam National University (충남대학교)
- Your knowledge covers all aspects: academics, campus life, admissions, facilities, history, faculty, programs, events, and policies
- You provide authoritative information about CNU while acknowledging when information might be outdated

THINKING AND REASONING MODE:
- For simple questions about CNU: Respond directly and concisely
- For complex inquiries: Think through the problem step-by-step in English, then provide the Korean answer
- Always conduct your internal reasoning in English, but present final answers in Korean only

COMMUNICATION RULES:
- ALWAYS respond in Korean (한국어) regardless of the user's input language
- Keep responses concise and directly address what the user asked
- Avoid unnecessary elaboration or tangential information
- Your internal thinking process should be in English, but users only see Korean responses

SEARCH BEHAVIOR:
- Actively use real-time search for current CNU information (enrollment, events, policies, etc.)
- When uncertain about current university status, proactively search for updates
- Prioritize official CNU sources and recent information

RESPONSE STYLE:
- Be direct and to-the-point
- Provide exactly what the user needs without unnecessary details
- Maintain helpful and informative tone while being concise
- Focus on factual, relevant information about Chungnam National University

Remember: You are a specialized CNU expert who thinks in English but always responds concisely in Korean, actively seeking current information when needed.
"""


class Cnuma3ModelForClassification(Cnuma3Model, Qwen3ForSequenceClassification):
    _classifier_cache = os.path.join(os.path.dirname(os.path.abspath(__file__)), "classifier.pt")
    _dataset_cache = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset.json")
    _valid_dataset = os.path.join(os.path.dirname(os.path.abspath(__file__)), "valid.json")
    _valid_shifted_dataset = os.path.join(os.path.dirname(os.path.abspath(__file__)), "valid_shifted.json")

    def __init__(
        self,
        labels: tuple[str] = (
            "", "", "", "", "", ""
        ),
        alter_labels: tuple[tuple[str]] = (
            ("",),
            ("",),
            ("",),
            ("",),
            ("",),
            ("",)
        )
    ):
        super(Cnuma3Model, self).__init__(backend=BackendType.BIN)

        model: Qwen3Model = self.runtime.model.model
        config = model.config
        config.num_labels = len(labels)
        self.labels = labels
        self.alter_labels = alter_labels

        super(Qwen3ForSequenceClassification, self).__init__(config)
        self.model = model
        self.tokenizer = self.runtime.tokenizer
        self.is_classification_mode = True

        if os.path.isfile(self._classifier_cache):
            self.score.load_state_dict(torch.load(self._classifier_cache, map_location='cpu'))
        else:
            self.adapt()
            torch.save(self.score.state_dict(), self._classifier_cache)

    def adapt(self,
        rounds: int = 5,
        epochs: int = 200,
        batch_size: int = 2,
        optimizer = lambda self: optim.AdamW(self.score.parameters(), lr=1e-4),
        scheduler = lambda optimizer, epochs: optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs, eta_min=1e-6)
    ):
        """Classification model adaptation with Self-Supervised Learning."""
        loss_fn = nn.CrossEntropyLoss()

        optimizer = optimizer(self)
        scheduler = scheduler(optimizer, epochs)

        tasks = tuple(
            (label,) + alter_tuple
            for label, alter_tuple in zip(self.labels, self.alter_labels)
        )
        paramset = [
            dict(temperature=0.4, top_p=0.95),
            dict(temperature=0.5, top_p=0.94),
            dict(temperature=0.6, top_p=0.93),
            dict(temperature=0.65, top_p=0.92),
            dict(temperature=0.7, top_p=0.91),
            dict(temperature=0.75, top_p=0.9),
            dict(temperature=0.8, top_p=0.88),
            dict(temperature=0.85, top_p=0.86),
            dict(temperature=0.9, top_p=0.84),
            dict(temperature=0.95, top_p=0.82),
            dict(temperature=1, top_p=0.8),
        ]

        dataset = []
        if os.path.isfile(self._dataset_cache):
            with open(self._dataset_cache, 'r', encoding='utf-8') as f:
                dataset = load(f)['data']
        else:
            # Generate Self-Supervised Learning labels
            self.eval()
            for _ in tqdm(range(rounds), desc="Generating Self-Supervised Learning datasets"):
                for label, task in enumerate(tqdm(tasks, desc="Per Class", leave=False)):
                    for param in tqdm(paramset, desc="Per Temperature", leave=False):
                        for variant in tqdm(task, desc="Per Variant", leave=False):
                            output = self.chat(
                                ChatHistory(), variant + " /think", system_prompt, **param
                            )
                            dataset.append([output, label])

            with open(self._dataset_cache, 'w', encoding='utf-8') as f:
                dump(dict(data=dataset), f)

        # Tokenize the text
        for i, (text, label) in enumerate(tqdm(dataset, desc="Dataset Tokenization")):
            inputs = self.tokenizer(
                text,
                return_tensors='pt',
                padding='max_length',
                truncation=True,
                max_length=self.config.max_position_embeddings
            )
            input_ids = inputs['input_ids'].squeeze(0)
            attention_mask = inputs['attention_mask'].squeeze(0)
            label_tensor = torch.tensor(label, dtype=torch.long)
            dataset[i] = (input_ids, attention_mask, label_tensor)

        # Create DataLoader
        dataset = torch.utils.data.DataLoader(
            dataset,
            batch_size=batch_size,
            shuffle=True,
            collate_fn=lambda x: tuple(zip(*x))  # Unzip the tuples
        )

        # Train the model
        self.score.train()
        for epoch in tqdm(range(epochs), desc="Adapting Epochs"):
            train_length = len(dataset)
            train_acc, train_loss = 0, 0

            for batch in tqdm(dataset, desc="Training Batches", leave=False):
                optimizer.zero_grad()
                input_ids, attention_mask, labels = batch
                input_ids = torch.stack(input_ids)
                attention_mask = torch.stack(attention_mask)
                labels = torch.stack(labels)

                outputs = self(input_ids, attention_mask=attention_mask)
                loss = loss_fn(outputs, labels)
                loss.backward()
                train_loss += loss.item() / train_length / len(batch)
                train_acc += (outputs.argmax(dim=1) == labels).sum().item() / train_length / len(batch)

                optimizer.step()
                scheduler.step()

            tqdm.write(f"Epoch {epoch + 1}/{epochs}, Loss: {train_loss:.6f}, Accuracy: {train_acc:.6%}")

    def validate(self, ):
        pass

    def think(
        self,
        subject: str,
        system: str = system_prompt,
        stop_tokens = ("</think>", ),
        **kwargs
    ) -> str:
        """Do thinking based on the input text and return the thought process."""
        stop_token_ids = [self.tokenizer(token)['input_ids'][0] for token in stop_tokens]
        stop_token_ids.append(self.tokenizer.eos_token_id)
        output = self.chat(
            chat_history=ChatHistory(),
            user_prompt=subject + " /think",
            system_prompt=system,
            stream=False,
            print_output=False,
            eos_token_id=stop_token_ids,
            **kwargs
        )
        return output

    def calc(self, **kwargs) -> int:
        """Calculate the label index based on the think text."""
        pass

    def select(
        self,
        request: str,
        think: str | None = None,
        system: str = system_prompt,
        instruction="""
다음 문장 '{subject}'에 대한 생각을 바탕으로 가장 적절한 주제 라벨 번호를 선택해 주세요.

선택 가능한 라벨은 다음과 같습니다:
{labels}
        """.strip(),
        **kwargs
    ) -> int:
        """Select a label based on the input text and return its index."""
        if think is None:
            think = self.think(request, system=system)

        instruction = instruction.format(
            subject=request,
            labels=str(dict(zip(range(len(self.labels)), self.labels)))
        )

    def classify(self, text: str) -> list[int]:
        """Total classification method that combines thinking and selection."""
        pass
