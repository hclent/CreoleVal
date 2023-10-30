
#MBERT
#to train on the MCTest160 dataset
python run_mbert.py --data_dir=./MCTest160       --output_dir=./outputs/MBERT160/         --tb_dir=./tensorboard/MBERT160         --learning_rate=1e-5         --weight_decay=0.01 --num_epochs=10 --action=train
#to train on the MCTest500 dataset
python run_mbert.py --data_dir=./MCTest500       --output_dir=./outputs/MBERT500/         --tb_dir=./tensorboard/MBERT160         --learning_rate=1e-5         --weight_decay=0.01 --num_epochs=10 --action=train


#XLMR
python run_xlmr.py --data_dir=./MCTest160         --output_dir=./outputs/XLMR160/         --tb_dir=./tensorboard/XLMR160         --learning_rate=1e-5          --weight_decay=0.01 --num_epochs=10 --action=train
