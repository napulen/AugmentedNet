import re

from AugmentedNet.common import ANNOTATIONSCOREDUPLES

rep_forward = '<repeat direction="forward"/>'
rep_backward = '<repeat direction="backward"/>'
rep_backward3 = '<repeat direction="backward" times="3"/>'
rep_backward4 = '<repeat direction="backward" times="4"/>'

for nick, (a, s) in ANNOTATIONSCOREDUPLES.items():
    print(nick, s)
    if s.endswith(".mxl"):
        smusicxml = s.replace(".mxl", ".musicxml")
        with open(smusicxml) as fd:
            data = fd.read()
        data = (
            data.replace(rep_forward, "")
            .replace(rep_backward, "")
            .replace(rep_backward3, "")
            .replace(rep_backward4, "")
        )
        with open(smusicxml, "w") as fd:
            fd.write(data)
