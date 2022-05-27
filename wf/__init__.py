"""
Reconstruct Mycobacterium tuberculosis CRISPR locus from WGS data
"""

import subprocess
from pathlib import Path
import os
from latch import small_task, workflow
from latch.types import LatchFile, LatchDir


@small_task
def CRISPRbuilderTB_task(SRA_ref: str, output_dir: LatchDir, output_name: str) -> LatchDir:

  # change directory to 'CRISPRbuilder-TB'

    os.chdir(Path("CRISPRbuilder-TB"))

    # Defining the output
    local_dir = Path("crispr_out")  # local directory to put output files in

    # prefix including local path
    local_prefix = os.path.join(local_dir, output_name)

    # Command to run
    _CRISPRbuilderTB_cmd = [
        "python",
        "crisprbuilder.py",
        "-sra",
        str(SRA_ref),
        "-out",
        str(local_prefix),
    ]

    # Files produce
    # Path(f"{local_prefix}.contig").resolve()
    # Path(f"{local_prefix}.reads_with_2_spacers").resolve()
    # Path(f"{local_prefix}.not_consecutive").resolve()
    # Path(f"{local_prefix}.cas_locus").resolve()
    # Path(f"{local_prefix}.cas_reads").resolve()
    # Path(f"{local_prefix}.is_around").resolve()

    subprocess.run(_CRISPRbuilderTB_cmd, check=True)
    return LatchDir(str(local_dir), output_dir.remote_path)


@workflow
def CRISPRbuilderTB(SRA_ref: str, output_dir: LatchDir, output_name: str) -> LatchDir:
    """

    # CRISPRbuilderTB

    This is the latch implementation of the CRISPRbuilder-TB tool
    for the reconstruction of Mycobacterium tuberculosis CRISPR-Cas loci
     from short reads under a semi-automatized process

    # Basic usage

     To use the tool, you will need a SRA reference. 

    - Input the reference, select an output directory, and input the output name

    - Click on Launch workflow at the [Latch console](https://console.latch.bio/explore/60752/info)

    ## Output files

    You will access the following files at each execution: 

    > contig: contigs of the CRISPR locus

    > not_consecutive

    > reads_with_2_spacers: the number of reads that contain the end of spacer k, 
      followed by a DR, followed by the beginning of spacer l (in .not_consecutive, l is not k+1)

    > cas_locus: a tentative reconstruction of the Cas locus
      based on the blast of beginning and end of Cas genes, 
      plus part of such genes followed by a beginning (or end) of IS6110, based on a short list of known events

    > cas_reads: number of reads for each event of the list used in .cas_locus

    > is_around: investigation of possibly unknown IS6110 in the flanking regions of the CRISPR locus.




    __metadata__:
        display_name: Reconstruct Mycobacterium tuberculosis CRISPR locus from WGS data.

        author: cguyeux

            name:  CRISPRbuilder-TB

            email:
            github: https://github.com/cguyeux/CRISPRbuilder-TB.git

        repository: https://github.com/cguyeux/CRISPRbuilder-TB.git

        license:

            id: MIT

    Args:

        SRA_ref:
          SRA reference

          __metadata__:
            display_name: SRA reference

        output_dir:
          Output directory

          __metadata__:
            display_name: Output directory

        output_name:
          Output name

          __metadata__:
            display_name: Output name
    """
    return CRISPRbuilderTB_task(SRA_ref=SRA_ref, output_dir=output_dir, output_name=output_name)
