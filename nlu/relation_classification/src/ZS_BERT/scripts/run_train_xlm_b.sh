#!/bin/bash
#SBATCH -J xlm_b #Slurm job name

# Choose partition (queue) "gpu" or "gpu-share"
#SBATCH -p gpu
#SBATCH --output=xlm_b.out
#SBATCH -N 1
#SBATCH --gres=gpu:1
#SBATCH --time=48:00:00 --mem=246000M

# Go to the job submission directory and run your application

cd /ceph/hpc/home/euliz/LiZhou/CreoleRE
source activate torch_tacred



mkdirs() {
    local dir="$1"
    if [ ! -d "$dir" ]; then
        mkdirs "$(dirname "$dir")"
        mkdir "$dir"
    fi
}


# model=('bert-base-multilingual-cased' 'xlm-roberta-base' 'xlm-roberta-large' 'bert-base-cased')
model=('xlm-roberta-base')

sentence=('bert-base-nli-mean-tokens' 'bert-large-nli-mean-tokens' 'xlm-r-bert-base-nli-mean-tokens' 'xlm-r-100langs-bert-base-nli-mean-tokens')
log_dir="/ceph/hpc/home/euliz/LiZhou/CreoleRE/log"

for mm in "${model[@]}"; do
    for ss in "${sentence[@]}"; do
        mkdirs "$log_dir"
        log_file="${log_dir}/${mm}_${ss}.log"
        > "$log_file"
        echo "$mm" | tee -a "$log_file"
        echo "$ss" | tee -a "$log_file"
        CUDA_VISIBLE_DEVICES=0 python /ceph/hpc/home/euliz/LiZhou/CreoleRE/ZS_BERT/model/train_wiki.py -se "$ss" -t "$mm" -cr bi cbk-zam jam pih tpi --model_saves /ceph/hpc/data/d2023d06-049-users/CreoleRE/save_models --Wiki_ZSL_data /ceph/hpc/home/euliz/LiZhou/CreoleRE/ZS_BERT/Wiki-ZSL --Creole_data /ceph/hpc/home/euliz/LiZhou/CreoleRE/CreoleData --prop_list_path /ceph/hpc/home/euliz/LiZhou/CreoleRE/ZS_BERT/resources/property_list.html  | tee -a "$log_file"
    done
done