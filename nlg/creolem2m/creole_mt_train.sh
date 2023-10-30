### Command for training models from scratch
### I am assuming that you have installed YANMTT
### Language codes are in creoles_list.txt. For example mfe stands for mauritian creole.



## Training from scratch

## Note 1: We used V100 GPUs.
## Note 2: A single GPU can be used with multistep optimizer. In our case we used 4, to simulate a 4 GPU training.
## Note 3: The hyperparameters in the command below are exactly what we used.

cd <PATH TO YANMTT FOLDER>

gpu=0
port=23344
slang=<source language code>
tlang=<target language code>
mkdir -p <PATH TO OUTPUT FOLDER>
export CUDA_VISIBLE_DEVICES=$gpu
python <PATH TO YANMTT>/train_nmt.py --train_slang $slang --train_tlang $tlang --dev_slang $slang --dev_tlang $tlang --train_src <PATH TO TRAIN SOURCE FILE> --train_tgt <PATH TO TRAIN TARGET FILE> --dev_src <PATH TO DEV SOURCE FILE> --dev_tgt <PATH TO DEV TARGET FILE> --model_path <PATH TO OUTPUT FOLDER> --label_smoothing=0.1 --encoder_layers=6 --decoder_layers=6 --encoder_attention_heads=8 --decoder_attention_heads=8 --encoder_ffn_dim=2048 --decoder_ffn_dim=2048 --d_model=512 --tokenizer_name_or_path=<PATH TO TOKENIZER> --lr 0.001 --max_gradient_clip_value 1.0 --dev_batch_size 128 --port $port --warmup_steps 16000 --weight_decay 0.00001 --hard_truncate_length 256 --dropout=0.1 --attention_dropout=0.1 --activation_dropout=0.1 --shard_files --multistep_optimizer_steps 4 &> <PATH TO OUTPUT FOLDER>/log


## Training by fine tuning mBART-50

## Note 1: We used the MT models trained on top of mbart-50. 
## Note 2: Rather than adding language codes to the mbart tokenizer which is a bit annoying, we reused existing language tokens of mBART-50: en_XX for ENGLISH and fr_XX for CREOLE. You can try any other language code. Results may vary.
## Note 3: For the example below, we assume English as source and creole as target and hence: --train_slang en_XX --train_tlang fr_XX --dev_slang en_XX --dev_tlang fr_XX. Reverse for when creole is source.

gpu=0
port=23344
mkdir -p <PATH TO OUTPUT FOLDER>
export CUDA_VISIBLE_DEVICES=$gpu
python <PATH TO YANMTT>/train_nmt.py --train_slang en_XX --train_tlang fr_XX --dev_slang en_XX --dev_tlang fr_XX --train_src <PATH TO TRAIN SOURCE FILE> --train_tgt <PATH TO TRAIN TARGET FILE> --dev_src <PATH TO DEV SOURCE FILE> --dev_tgt <PATH TO DEV TARGET FILE> --model_path <PATH TO OUTPUT FOLDER> --label_smoothing=0.1 --tokenizer_name_or_path=facebook/mbart-large-50-many-to-many-mmt --warmup_steps 2500 --weight_decay 0.00001 --lr 0.00003 --max_gradient_clip_value 1.0 --dev_batch_size 32 --batch_size 512 --port $port --hard_truncate_length 256 --pretrained_model facebook/mbart-large-50-many-to-many-mmt --use_official_pretrained --dropout=0.3 --attention_dropout=0.3 --activation_dropout=0.3 --shard_files --multistep_optimizer_steps 4 &> <PATH TO OUTPUT FOLDER>/log