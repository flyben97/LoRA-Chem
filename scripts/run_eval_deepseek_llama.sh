#!/bin/bash
#SBATCH --gpus=1
#SBATCH --ntasks=1
#SBATCH --output=../logs/train_eval_output_%j.log   
#SBATCH --error=../logs/train_eval_error_%j.log     

mkdir -p ../logs

llamafactory-cli train \
    --stage sft \
    --model_name_or_path ../DeepSeek-R1-Distill-llama-8B \
    --adapter_name_or_path ../SHC-oAK_train_with_names \
    --preprocessing_num_workers 16 \
    --finetuning_type lora \
    --quantization_method bitsandbytes \
    --template deepseek3 \
    --flash_attn auto \
    --dataset_dir ../LLaMA-Factory/data \
    --eval_dataset SHC-oAK_test_with_names_smiles \
    --cutoff_len 1024 \
    --max_samples 100000 \
    --per_device_eval_batch_size 2 \
    --predict_with_generate True \
    --max_new_tokens 512 \
    --top_p 0.7 \
    --temperature 0.95 \
    --output_dir ../eval/trial \
    --trust_remote_code True \
    --do_predict True

