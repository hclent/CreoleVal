### Command for training models from scratch
### I am assuming that you have installed YANMTT
### Language codes are in creoles_list.txt. For example mfe stands for mauritian creole.

cd <PATH TO YANMTT FOLDER>

## Decoding a scratch model
## Note 1: The best model will be present in the model folder as: <model prefix>.best_dev_bleu.<source language code>-<target language code>

gpu=0
port=23344
slang=<source language code>
tlang=<target language code>
export CUDA_VISIBLE_DEVICES=$gpu
slangtag=$lang
dec_model=<PATH TO MODEL TO BE DECODED>
export CUDA_VISIBLE_DEVICES=$gpu
python <PATH TO YANMTT>/decode_nmt.py --model_path $dec_model --slang $slangtag --tlang $tlangtag --test_src <TEST INPUT FILE> --test_tgt <TRANSLATION FILE> --port $port --encoder_layers=6 --decoder_layers=6 --encoder_attention_heads=8 --decoder_attention_heads=8 --encoder_ffn_dim=2048 --decoder_ffn_dim=2048 --d_model=512 --tokenizer_name_or_path=<PATH TO TOKENIZER> --beam_size 4 --length_penalty 0.8

## Decoding a fine-tuned model
## Note 1: The best model will be present in the model folder as: <model prefix>.best_dev_bleu.<source language code>-<target language code>. Except in this case, the language codes will be en_XX and fr_XX.
## Note 2: For the example below, we assume English as source and creole as target and hence: --train_slang en_XX --train_tlang fr_XX --dev_slang en_XX --dev_tlang fr_XX. Reverse for when creole is source.

gpu=0
port=23344
export CUDA_VISIBLE_DEVICES=$gpu

dec_model=<PATH TO MODEL TO BE DECODED>
export CUDA_VISIBLE_DEVICES=$gpu
python <PATH TO YANMTT>/decode_nmt.py --model_path facebook/mbart-large-50-many-to-many-mmt --slang en_XX --tlang fr_XX --test_src <TEST INPUT FILE> --test_tgt <TRANSLATION FILE> --port $port --use_official_pretrained --locally_fine_tuned_model_path $dec_model --tokenizer_name_or_path facebook/mbart-large-50-many-to-many-mmt --beam_size 4 --length_penalty 0.8


## Evaluation

## BLEU
cat <TRANSLATION FILE> | sacrebleu -b <TEST REFERENCE FILE> 

## CHRF
cat <TRANSLATION FILE> | sacrebleu -b <TEST REFERENCE FILE> --metrics chrf