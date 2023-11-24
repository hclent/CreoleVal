for DATASET in MCTestHat1 MCTestHat2 MCTestMar
do
    echo "Training on $DATASET"
    #MBERT
    python run_mbert.py --data_dir=$DATASET --output_dir=./outputs/$DATASET/mBERT --tb_dir=./tensorboard/$DATASET/mBERT --learning_rate=1e-5 --weight_decay=0.01 --num_epochs=10 --action=train

    #XLMR
    python run_xlmr.py --data_dir=$DATASET --output_dir=./outputs/$DATASET/XLM-R --tb_dir=./tensorboard/$DATASET/XLM-R --learning_rate=1e-5  --weight_decay=0.01 --num_epochs=10 --action=train
    python run_xlmr.py --data_dir=$DATASET --output_dir=./outputs/$DATASET/XLM-R-FRA/ --tb_dir=./tensorboard/$DATASET/XLM-R-FRA --learning_rate=1e-5 --weight_decay=0.01 --num_epochs=10 --action=train --from_pretrained "lgrobol/xlm-r-CreoleEval_fra"
done
