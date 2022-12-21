FROM anibali/pytorch:1.13.0-cuda11.8

WORKDIR ./

COPY . ./

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN ls -la ./

CMD ["python", "-m", "src.train_wiki_val_test"]