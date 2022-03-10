import pip

def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])


install('requests')

import logging, os, json, requests
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    # # On charge les variables de l'application
    #dotenv.load_dotenv()
    #model_url = os.getenv("MODEL_URL")
    model_url = "http://7cc2e629-221d-4f12-8682-6b926ecb310b.westeurope.azurecontainer.io/score"

    logging.info(f"Python HTTP trigger function processed a request at : {model_url}")

    ######### 1. get user_id from htpp param or from api call
    user_id = req.params.get('userId')   
    if not user_id:
        try:         
            req_body = req.get_json()
            user_id = req_body.get("userId")
        except ValueError:
            logging.info('USER not found')
            return func.HttpResponse(
                "'userId' n'existe pas",
                status_code=200
            )
    else:
        user_id = user_id
    ######### get user_id from htpp param or from api call
    
    logging.info(f'USER {user_id}')

    ######### 2. On appelle le modèle qui renvoit les recommendations    
    # On crée la donnée d'entrée du modèle déployé
    model_data = {"user_id": int(user_id)}   
    headers = {"Content-Type": "application/json", 'Accept':'application/json'}
    response = requests.post(model_url, json=model_data, headers=headers)
    ######### On appelle le modèle qui renvoit les recommendations

    ######### 3. On vérifie la réponse
    if not response.ok:
        return func.HttpResponse(
            f"Erreur on model side, err: {response.status_code}",
            status_code=200
        )
    else:
        recommended = json.loads(response.text)

        articles_id = []
        for k,v in recommended.items():
            articles_id.append(int(v))

        # On spécifie que la réponse sera en JSON
        func.HttpResponse.mimetype = "application/json"
        func.HttpResponse.charset = "utf-8"

        return func.HttpResponse(json.dumps(articles_id))
        # return func.HttpResponse(json.dumps(recommended))
    ######## On vérifie la réponse