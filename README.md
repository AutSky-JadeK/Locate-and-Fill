This repository stores the code and data related to ACL2023 Findings paper: `Incomplete Utterance Rewriting by A Two-Phase Locate-and-Fill Regime`.
Running Steps on `CANARD`, it is similar on `CQR` and `MuDoCo`.

## Data generation

```console
python CANARD-work/lcs_becky.py
python CANARD-work/trans-ner-to-ours-rule.py
python CANARD-work/make-ours-rule-rules.py
```

## Step1: Locating the rewriting positions

```console
python CANARD-work/NER_BERT_CRF.py
```

## Step2: Filling in the blanks

```console
python -u run_summarization.py \
    --model_name_or_path /home/t5-small-original \
    --do_train \
    --do_eval \
    --do_predict \
    --num_train_epochs 20 \
    --train_file train-becky-prompt-5571-T5.json \
    --validation_file dev-becky-prompt-5571-T5.json \
    --test_file test-becky-prompt-5571-T5.json \
    --output_dir /home/tst-T5-becky \
    --overwrite_output_dir \
    --per_device_train_batch_size=4 \
    --per_device_eval_batch_size=4 \
    --predict_with_generate
python testT5.py
```

## Rule based method

```console
python rules.py
```

## Evaluation

```console
python CANARD-work/work-standard-T5-F1.py
```