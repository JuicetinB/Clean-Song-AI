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
    dmodel="htdemucs_ft"
    demucs.separate.main(["--two-stems", "vocals", "-n", dmodel, "-o", out, file])
    folder = out + "\\" + dmodel + "\\" + file.rsplit(dash,1)[1].rsplit(".",1)[0] + "\\"
    return folder + "no_vocals.wav", folder + "vocals.wav"

#I also want to try -n htdemucs_ft instead of the mdx_extra model; htdemucs might be faster