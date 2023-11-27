import sys
sys.path.append('../ExtractPY')

from createBD import CreateBD

myExtract = CreateBD()

myExtract.scrapper_medias(1, 1, 2)
