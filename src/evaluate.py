"""Run reproducible zero-shot, few-shot, or two-stage translation evaluation.

Example:
python -m src.evaluate --dataset deliverables/final_benchmark_70.csv \
  --model Qwen/Qwen2.5-1.5B-Instruct --condition zero_shot \
  --output results/new_run.jsonl
"""

from __future__ import annotations

import argparse
import json
import os
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import set_seed

from .analysis import LABELS, normalize_label


def load_model(model_id: str, revision: str | None):
    tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision, token=os.getenv("HF_TOKEN"))
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        revision=revision,
        token=os.getenv("HF_TOKEN"),
        torch_dtype=(
            torch.bfloat16 if torch.cuda.is_available() and torch.cuda.is_bf16_supported()
            else torch.float16 if torch.cuda.is_available() else torch.float32
        ),
        device_map="auto" if torch.cuda.is_available() else None,
    )
    model.eval()
    return tokenizer, model


def generate(tokenizer, model, prompt: str, max_new_tokens: int) -> str:
    messages = [{"role": "user", "content": prompt}]
    if hasattr(tokenizer, "apply_chat_template"):
        rendered = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
    else:
        rendered = prompt
    inputs = tokenizer(rendered, return_tensors="pt").to(model.device)
    with torch.inference_mode():
        output = model.generate(
            **inputs,
            do_sample=False,
            max_new_tokens=max_new_tokens,
            pad_token_id=tokenizer.eos_token_id,
        )
    continuation = output[0][inputs["input_ids"].shape[1]:]
    return tokenizer.decode(continuation, skip_special_tokens=True).strip()


def prompt_zero_shot(claim: str) -> str:
    return (
        "Classify the claim as exactly one of Supported, Refuted, or Insufficient. "
        "Return only the label.\nClaim: " + claim + "\nLabel:"
    )


def prompt_translation(claim: str, form: str) -> str:
    return (
        f"Translate this {form} health claim into English. Preserve negation, modality, "
        "quantifiers, numbers, units, dates, medical terms, and qualifiers. Return only "
        f"the translation.\nClaim: {claim}\nEnglish translation:"
    )


def prompt_verify_english(claim: str) -> str:
    return (
        "Classify the following English health claim as exactly one of Supported, Refuted, "
        f"or Insufficient. Return only the label.\nClaim: {claim}\nLabel:"
    )


def run(args: argparse.Namespace) -> None:
    set_seed(args.seed)
    data = pd.read_csv(args.dataset)
    required = {"claim_id", "english", "urdu", "roman_urdu", "gold_label", "topic", "claim_type"}
    missing = required - set(data.columns)
    if missing:
        raise ValueError(f"Dataset missing columns: {sorted(missing)}")
    if data["claim_id"].duplicated().any():
        raise ValueError("Duplicate claim_id in dataset")
    if args.condition == "few_shot":
        if not args.demonstrations:
            raise ValueError("Few-shot requires --demonstrations outside the test set")
        demos = pd.read_csv(args.demonstrations)
        overlap = set(demos["claim_id"]) & set(data["claim_id"])
        if overlap:
            raise ValueError(f"Few-shot leakage: {sorted(overlap)}")
    else:
        demos = None

    tokenizer, model = load_model(args.model, args.revision)
    forms = ["english", "urdu", "roman_urdu"]
    args.output = Path(args.output)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        for item in data.itertuples():
            for form in forms:
                claim = getattr(item, form)
                translation = None
                translation_prompt = None
                translation_raw = None
                if args.condition == "translate_then_verify" and form != "english":
                    translation_prompt = prompt_translation(claim, form)
                    translation_raw = generate(
                        tokenizer, model, translation_prompt, args.max_new_tokens
                    )
                    translation = translation_raw
                    verification_prompt = prompt_verify_english(translation)
                elif args.condition == "few_shot":
                    examples = "\n".join(
                        f"Claim: {getattr(row, form)}\nLabel: {row.gold_label}"
                        for row in demos.itertuples()
                    )
                    verification_prompt = (
                        examples + "\n\n" + prompt_zero_shot(claim)
                    )
                else:
                    verification_prompt = prompt_zero_shot(claim)

                started = time.time()
                error = None
                try:
                    raw = generate(tokenizer, model, verification_prompt, args.max_new_tokens)
                except Exception as exc:
                    raw = ""
                    error = repr(exc)
                record = {
                    "run_id": str(uuid.uuid4()),
                    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                    "model_requested": args.model,
                    "model_revision_requested": args.revision,
                    "condition": args.condition,
                    "prompting_condition": args.condition,
                    "seed": args.seed,
                    "temperature": 0.0,
                    "max_new_tokens": args.max_new_tokens,
                    "claim_id": item.claim_id,
                    "topic": item.topic,
                    "claim_type": item.claim_type,
                    "form": form,
                    "claim_text": claim,
                    "gold_label": item.gold_label,
                    "translation_prompt": translation_prompt,
                    "translation_raw": translation_raw,
                    "translation_text": translation,
                    "verification_prompt": verification_prompt,
                    "raw_response": raw,
                    "predicted_label": normalize_label(raw),
                    "invalid_reason": "unparseable_or_empty" if normalize_label(raw) is None else None,
                    "latency_seconds": time.time() - started,
                    "error": error,
                }
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--revision")
    parser.add_argument("--condition", choices=["zero_shot", "few_shot", "translate_then_verify"], required=True)
    parser.add_argument("--demonstrations")
    parser.add_argument("--output", required=True)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max-new-tokens", type=int, default=32)
    run(parser.parse_args())


if __name__ == "__main__":
    main()
