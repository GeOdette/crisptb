FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:02ab-main

#Install conda
RUN curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh --output miniconda.sh
ENV CONDA_DIR /opt/conda
RUN bash miniconda.sh -b -p /opt/conda
ENV PATH=$CONDA_DIR/bin:$PATH

# Install dependencies 
RUN conda install -c bioconda parallel-fastq-dump &&\
    conda install -c bioconda blast &&\
    conda install -c kantorlab blastn

#Install requirements
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Clone repo
RUN git clone https://github.com/cguyeux/CRISPRbuilder-TB.git

COPY data /root/reference
ENV BOWTIE2_INDEXES="reference"

# STOP HERE:
# The following lines are needed to ensure your build environement works
# correctly with latch.
COPY wf /root/wf
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
RUN python3 -m pip install --upgrade latch
WORKDIR /root
ENV LATCH_AUTHENTICATION_ENDPOINT https://nucleus.latch.bio

