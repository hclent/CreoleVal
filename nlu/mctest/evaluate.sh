#MBERT

#To evaluate on English dev, use the MCTest160 dir that you trained on
python3 run_mbert.py --data_dir=./MCTest160         --output_dir=./outputs/MBERT160/         --tb_dir=./MBERT160         --learning_rate=1e-5         --weight_decay=0.01 --num_epochs=10 --action=evaluate --from_checkpoint=./outputs/MBERT160/mbert_lr1e-05_wd0.01/checkpoint-450

#To evaluate on a Creole dev set, simply point towards the directory with the name matching the Creole. For example:
python3 run_mbert.py --data_dir=./MCTestHat1         --output_dir=./outputs/MBERT160/         --tb_dir=./MBERT160         --learning_rate=1e-5         --weight_decay=0.01 --num_epochs=10 --action=evaluate --from_checkpoint=./outputs/MBERT160/mbert_lr1e-05_wd0.01/checkpoint-450
python3 run_mbert.py --data_dir=./MCTestHat2         --output_dir=./outputs/MBERT160/         --tb_dir=./MBERT160         --learning_rate=1e-5         --weight_decay=0.01 --num_epochs=10 --action=evaluate --from_checkpoint=./outputs/MBERT160/mbert_lr1e-05_wd0.01/checkpoint-450
python3 run_mbert.py --data_dir=./MCTestMar         --output_dir=./outputs/MBERT160/         --tb_dir=./MBERT160         --learning_rate=1e-5         --weight_decay=0.01 --num_epochs=10 --action=evaluate --from_checkpoint=./outputs/MBERT160/mbert_lr1e-05_wd0.01/checkpoint-450

#If you want to see your model's performance on test, you should point to the MCTest160 or MCTest500 , which has English test
python3 run_mbert.py --data_dir=./MCTest160         --output_dir=./outputs/MBERT160/         --tb_dir=./MBERT160         --learning_rate=1e-5         --weight_decay=0.01 --num_epochs=10 --action=test --from_checkpoint=./outputs/MBERT160/mbert_lr1e-05_wd0.01/checkpoint-450

#XLMR
python3 run_xlmr.py --data_dir=./MCTest160         --output_dir=./outputs/XLMR160/         --tb_dir=./XLMR160         --learning_rate=1e-5         --weight_decay=0.01 --num_epochs=10 --action=evaluate --from_checkpoint=./outputs/XLMR160/xlmr_lr1e-05_wd0.01/checkpoint-450


