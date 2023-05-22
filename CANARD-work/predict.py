import os 
#os.environ['CUDA_VISIBLE_DEVICES']='2'

from allennlp.models.archival import load_archive
from allennlp.predictors.predictor import Predictor
# WARNING: Do not exclude these imports
from predictor import RewritePredictor
from data_reader import RewriteDatasetReader
from model import UnifiedFollowUp

f1 = open('../dataset/CANARD/test.txt', 'r')
#f1 = open('../dataset/CANARD/test.txt','r')
f2 = open('predict_results-author.txt','w')

class PredictManager:

    def __init__(self, archive_file):
        archive = load_archive(archive_file)
        self.predictor = Predictor.from_archive(
            archive, predictor_name="rewrite")

    def predict_result(self, dialog_flatten: str):
        # dialog_flatten is split by \t\t
        dialog_snippets = dialog_flatten.split("\t\t")
        #print(dialog_snippets)
        param = {
            "context": dialog_snippets[:-2],
            "current": dialog_snippets[-2]
        }
        #print(param['context'])
        #print('\n')
        #print(param['current'])
        #print('\n')
        restate = self.predictor.predict_json(param)['predicted_tokens']
        #print(restate)
        #print('\n\n\n')
        return restate


if __name__ == '__main__':
    manager = PredictManager("../pretrained_weights/canard.tar.gz")
    #result = manager.predict_result("anna politkovskaya      the murder remains unsolved , 2016      did they have any clues ?       did investigators have any clues in the unresolved murder of anna politkovskaya ?")
    #print(result)
    cnt = 0
    while True:
        line = f1.readline()
        line = line.strip()
        if line == '':
            break
        result = manager.predict_result(line)
        '''
        pts = line.split('\t\t')
        prt = ''
        for i in range(len(pts)-1):
            if i != 0:
                prt += '\t\t'
            prt += pts[i]
        prt = prt + '\t\t' + result
        '''
        print(line + '\t\t' + result, file=f2)
        cnt += 1
        print(cnt)
