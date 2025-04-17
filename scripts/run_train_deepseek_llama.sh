#!/bin/bash
#SBATCH --gpus=1
#SBATCH --ntasks=1
#SBATCH --output=../logs/train_output_%j.log   
#SBATCH --error=../S10/logs/train_error_%j.log     

mkdir -p ../logs

python ../LLaMA-Factory/src/train.py \
    --stage sft \
    --do_train True \
    --model_name_or_path ../DeepSeek-R1-Distill-llama-8B \
    --preprocessing_num_workers 16 \
    --finetuning_type lora \
    --template deepseek3 \
    --flash_attn auto \
    --dataset_dir ../LLaMA-Factory/data \
    --dataset SHC-oAK_train_with_names \
    --cutoff_len 2048 \
    --learning_rate 5e-05 \
    --num_train_epochs 30.0 \
    --max_samples 100000 \
    --per_device_train_batch_size 2 \
    --gradient_accumulation_steps 8 \
    --lr_scheduler_type cosine \
    --max_grad_norm 1.0 \
    --logging_steps 10 \
    --save_steps 100 \
    --warmup_steps 0 \
    --packing False \
    --report_to tensorboard \
    --output_dir ../SHC-oAK_train_with_names \
    --bf16 True \
    --plot_loss True \
    --trust_remote_code True \
    --ddp_timeout 180000000 \
    --include_num_input_tokens_seen True \
    --optim adamw_torch \
    --lora_rank 16 \
    --lora_alpha 32 \
    --lora_dropout 0 \
    --lora_target all \
    2>&1 | tee -a ../logs/training_log_%j.txt