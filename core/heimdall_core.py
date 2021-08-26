from core.nlpfunctions import bow
from core.nlpfunctions import clean_up_sentence
from core.telegram_alert import sendText
from core.telegram_alert import sendPhoto
from core.telegram_alert import sendDoc

import numpy as np
import random
from keras.models import load_model
import pickle
import json

data = pickle.load(open( "files/meta.pkl", "rb" ) )
words = data['words']
classes = data['classes']
with open('files/intents.json') as json_data:
    intents = json.load(json_data)
model = load_model('files/model.h5')

context = {}
debugmode = {}
ERROR_THRESHOLD = 0.3

context = {}
ERROR_THRESHOLD = 0.3

def classify(sentence):
    p = np.array([bow(sentence, words)])
    results = list(model.predict(p))[0]
    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    return return_list

def action(action,userID,context_filter=None):
    print("Action:"+action)                        
    if action=="debug_mode":
        debugmode[userID]=True
        print("Debug mode initialised for "+str(userID))
        return True
    
    elif action=="debug_mode_off":
        debugmode[userID]=False
        print("Debug mode disabled for "+str(userID))
        return True
    
    elif userID in context and context_filter==context[userID]:
        if action=="gen_cert_type_vm":
            sendText("Generate VM Certs")
            context.pop(userID, None)
            return True
        
        elif action=="gen_cert_type_rg":
            sendText("Generate RG Certs")
            context.pop(userID, None)
            return True
    return False


def response(sentence, userID='anonymous',show_details=False):
    results = classify(sentence)
    output = {"response":"Sorry, please try again","input":sentence,"userid":userID,"debug":False}
    if results:
        while results:
            for i in intents['intents']:
                if i['tag'] == results[0][0]:
                    if 'context_set' in i:
                        context[userID] = i['context_set']
                        output["context_set"] = i["context_set"]      
                    output["tag"] = i['tag']
                    if not 'context_filter' in i:
                        output["response"] = random.choice(i['responses'])
                    elif (userID in context and 'context_filter' in i and i['context_filter'] == context[userID]):
                        #context.pop(userID, None)
                        output["response"] = random.choice(i['responses'])
                        output["context_filter"] = i["context_filter"]
                    
                    ################ Action Set #########################
                    if 'action' in i:
                        output['action'] = i['action']
                        if "context_filter" in i:
                            output['output_status'] = action(i['action'],userID,i["context_filter"])
                        else:
                            output['output_status'] = action(i['action'],userID)
                    ######################################################
            results.pop(0)
    
    if userID in debugmode:
        if debugmode[userID]:
            show_details = debugmode[userID]
            output["debug"] = debugmode[userID]

    if show_details: 
        return output
    else:
        return output["response"]

print(response("hello"))