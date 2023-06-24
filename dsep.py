#prereqs install demucs using github page
import demucs.separate
import os
def vocals(file, out=None):
    if out==None:
        if "/" in file:
            dash="/"
        else:
            dash="\\"
        out = file.rsplit(dash,1)[0]

    demucs.separate.main(["--two-stems", "vocals", "-n", "mdx_extra", "-o", out, file])
    folder = out + "\\mdx_extra\\" + file.rsplit(dash,1)[1].rsplit(".",1)[0] + "\\"
    return folder + "no_vocals.wav", folder + "vocals.wav"