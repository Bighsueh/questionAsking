import requests
class Model:
    def __init__(self, model_name:str = "gpt-35-turbo", model_endpoint: str = ''):
        self.model_name = model_name
        self.model_endpoint = model_endpoint

    def send_post_request(self, request_body) -> dict:
        try:
            response = requests.post(self.model_endpoint, json=request_body)
            if response.status_code == 200:
                return response.json()
            else:
                print('連線錯誤:', response.status_code)
        except Exception as e:
            print("請求失敗:", str(e))

    def chat(self, system_message: str = '', chat_message: str = '', context: str = '') -> dict:
        if not self.model_name or not chat_message:
            return {}

        chat_log = []
        if system_message:
            chat_log.append({"role": 'system', "content": f"{system_message}, You must respond according to the following information:{context}"})
        
        chat_log.append({"role": 'user', "content": chat_message})

        request_body = {
            "engine": self.model_name,
            "temperature": 0.3,
            "max_tokens": 500,
            "top_p": 0.95,
            "top_k": 5,
            "roles": chat_log,
            "frequency_penalty": 0,
            "repetition_penalty": 1.03,
            "presence_penalty": 0,
            "stop": "",
            "past_messages": 10,
            "purpose": "dev"
        }
        
        return self.send_post_request(request_body=request_body)