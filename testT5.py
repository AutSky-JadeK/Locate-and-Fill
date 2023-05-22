from transformers import T5Config, T5Tokenizer, T5ForConditionalGeneration
import torch
import os
#os.environ['CUDA_VISIBLE_DEVICES'] = '3'

config = T5Config.from_json_file("tst-T5-becky-nosplit/config.json")
tokenizer = T5Tokenizer.from_pretrained("tst-T5-becky-nosplit/")
model = T5ForConditionalGeneration.from_pretrained("tst-T5-becky-nosplit/")

'''
# training
inputs = tokenizer("The <extra_id_0> walks in <extra_id_1> park", return_tensors="tf").input_ids
labels = tokenizer("<extra_id_0> cute dog <extra_id_1> the <extra_id_2>", return_tensors="tf").input_ids
outputs = model(inputs, labels=labels)
loss = outputs.loss
logits = outputs.logits

'''


'''

# inference
inputs = tokenizer(
    "superstar billy graham [SEP] disputes with the mcmahons [SEP] what disputes did he have ? [SEP] graham personally sued zahorian and the wwf , [SEP] why ? [SEP] claiming that they had forced him to take steroids to maintain his position in the company . [SEP] did he win the lawsuit ? [SEP] his lawsuit was unsuccessful , [SEP] what happened after the suit failed ? [SEP] graham went on a public awareness campaign regarding the dangers of steroids [SEP] how did the campaign do ? [SEP] during the donahue taping graham claimed to have witnessed wwf officials sexually abuse children . [SEP] did these allegations get anywhere ? [SEP] graham later admitted that he made up the allegations , hoping to extort \" hush money \" out of the wwf . was he able to get money from <extra_id_0> after all ?", "superstar billy graham [SEP] disputes with the mcmahons [SEP] what disputes did he have ? [SEP] graham personally sued zahorian and the wwf , [SEP] why ? [SEP] claiming that they had forced him to take steroids to maintain his position in the company .", return_tensors="pt"
).input_ids  # Batch size 1
outputs = model.generate(inputs)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
# studies have shown that owning a dog is good for you


'''

f1 = open('test-becky-ner-5571-T5-inputs-nosplit.txt', 'r')
f2 = open('test-becky-ner-5571-T5-outputs-nosplit.txt', 'w')

cnt = 0
while True:
    line = f1.readline()
    line = line.strip()
    if line == '':
        break
    print(cnt)
    inputs = tokenizer(line, return_tensors="pt", truncation=True).input_ids  # Batch size 1
    print('inputs finish')
    outputs = model.generate(inputs)
    print('outputs finish')
    print(tokenizer.decode(outputs[0], skip_special_tokens=True), file=f2)
    print('decode finish')
    cnt += 1
    '''
    if cnt == 142:
        break
    '''
