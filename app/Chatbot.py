from Model import Model

import json

class Chatbot():
    def __init__(self,model: Model, prompt_file:str):
        self.model:Model = model
        self.user_message:str = ''
        self.prompt_file:str = prompt_file
        self.feedback:str = ''
        self.response_log:str = ''
        self.prompt_dict:dict = {}
        
        self.load_prompt_file()

    def input_message(self, user_query:str) -> None:
        self.user_message = user_query
        
    def load_prompt_file(self) -> None:
        if not self.prompt_file :print('empty')
        with open(self.prompt_file, 'r') as file:
            self.prompt_dict = json.load(file)
            
    def check_condition(self, system_message:str) -> bool:
        user_query = self.user_message
        result = self.model.chat(system_message=system_message, 
                                 chat_message=f"使用者輸入內容：{user_query}")
        response = result['choices'][0]['message']['content']
        print(f"使用者輸入內容：{user_query}, 系統回覆：{response}")
        self.response_log += response
        # self.response_log += response.replace('yes', '').replace('no', '')

        return "yes" in response or 'Yes' in response
    
    def feedback_summarize(self) -> None:
        system_message = self.prompt_dict['feedback_summarize']
        result = self.model.chat(system_message=system_message,
                                        chat_message=f"使用者輸入內容：{self.user_message},回饋內容：{self.response_log}")
        
        self.feedback = result['choices'][0]['message']['content']

    def check_complete_question(self) -> bool:
        all_conditions_pass:bool = True
        # condition_list = ['interrogative','subject','verb','context']
        condition_list = ['interrogative','verb','context']
        
        for condition in condition_list:
            system_message = self.prompt_dict[condition]
            if not self.check_condition(system_message=system_message): all_conditions_pass = False
            
        if not all_conditions_pass: self.feedback_summarize()
        
        return all_conditions_pass
    
    def check_relavent(self) -> bool:
        condition_pass:bool = True
        topic:str = '植物'
        
        system_message = self.prompt_dict["topic_relavent"]
        if not self.check_condition(system_message=f"{system_message}, 當前主題：{topic}"): condition_pass = False
        
        if not condition_pass: self.feedback_summarize()
        
        return condition_pass
    
    def refine_question(self):
        pass

    def workflow(self) -> bool:
        if not len(self.user_message) > 0 : return ''
        
        if self.check_complete_question() : return False 
        if self.check_relavent() : return False 

        return True
        
        pass