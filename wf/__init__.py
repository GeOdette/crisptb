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

    # Defining the output
    local_dir = Path("crispr_out")  # local directory to put output files in

    # prefix including local path
    local_prefix = os.path.join(local_dir, output_name)

    # Command to run
    _CRISPRbuilderTB_cmd = [
        "python",
        "crisprbuilder.py",
        "--sra",
        str(SRA_ref),
    ]

    # Files produced
    Path(f"{local_prefix}.contig").resolve()
    Path(f"{local_prefix}.reads_with_2_spacers").resolve()
    Path(f"{local_prefix}.not_consecutive").resolve()
    Path(f"{local_prefix}.cas_locus").resolve()
    Path(f"{local_prefix}.cas_reads").resolve()
    Path(f"{local_prefix}.is_around").resolve()

    subprocess.run(_CRISPRbuilderTB_cmd, check=True)
    return LatchDir(local_dir, output_dir.remote_path)


@workflow
def CRISPRbuilderTB(SRA_ref: str, output_dir: LatchDir, output_name: str) -> LatchDir:
    """


    __metadata__:
        display_name: Reconstruct Mycobacterium tuberculosis CRISPR locus from WGS data.
        author:
            name:
            email:
            github:
        repository:
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
