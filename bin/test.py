import re

p = re.compile(r"Haib\w*\.")
m=p.findall("0.spp.idrOptimal.bf.wgEncodeHaibTfbsA549Atf3V0422111Etoh02AlnRep0.bam_VS_wgEncodeHaibTfbsA549RxlchPcr1xEtoh02AlnRep0.bam.bed")
print m