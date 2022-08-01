FROM nvcr.io/nvidia/pytorch:21.10-py3

# Project setup
ENV VIRTUAL_ENV=/opt/venv

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc g++ make  python3 python3-dev python3-pip python3-venv python3-wheel libsndfile1-dev gcc g++ mecab libmecab-dev mecab-ipadic-utf8 libsndfile1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv "$VIRTUAL_ENV"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install --quiet --upgrade pip && \
    pip install --quiet pip-tools

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt \
    && rm -rf /root/.cache/pip

# RUN pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113

COPY . /app
WORKDIR /app

ENTRYPOINT [ "/bin/sh" ]