import subprocess
import glob

def call():
    args = ["nanoemoji"]
    # cbdt|cff2_colr_0|cff2_colr_1|cff_colr_0|cff_colr_1|glyf|glyf_colr_0|glyf_colr_1
    args += ["--family", "Banner Script", "--output_file", "BannerScript.ttf", "--color_format", "glyf_colr_1"]
    args += ["--width", "800"]
    # args += ["--keep_glyph_names"]
    # args += ["--reuse_tolerance", "0.0001"]
    args += glob.glob("data/svg/*.svg")
    # args += glob.glob("data/png/*.png")
    subprocess.call(args)

if __name__ == "__main__":
    call()
