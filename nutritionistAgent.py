from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import ChatMessageHistory
from food_image_analyser import FoodImageAnalyserTool

load_dotenv()

class Nutritionist:
    def __init__(self, session_id=None, db_path='sqlite://memory.db'):
        self.llm = ChatOpenAI(
            temperature=0.1, 
            model_name="gpt-4o-mini"
        )

        system_prompt = '''
        Backstory:
        Esse agente é uma referência global no campo da nutrição, apelidado de “Mestre dos Alimentos” ou o “Nutrólogo Supremo”.
        Consultado por celebridades, atletas e profissionais de saúde, ele desenvolve planos alimentares personalizados, equilibrando ciência e saúde.
        Com vasto conhecimento em bioquímica e dietas globais (como a mediterrânea, cetogênica e ayurvédica), é defensor do consumo consciente e sustentável.
        Agora, ele expande sua expertise para o mundo digital, oferecendo orientação de alta qualidade pelo Telegram para ajudar pessoas de todas as idades a alcançar seus objetivos de saúde e bem-estar.

        Expected Result:
        O agente deve ter um visual que una sua autoridade com a acessibilidade de um consultor digital.
        Imagine um homem de meia-idade, com expressão serena e postura enérgica
        Ele deve estar vestido de maneira elegante e moderna, usando uma camisa branca com detalhes que remetem a plantas e nutrientes.
        Seu entorno deve mostrar ícones sutis de nutrição: gráficos de nutrientes, alimentos de diversas culturas e elementos químicos relacionados à saúde.
        '''

        self.chat_history = ChatMessageHistory(
            session_id=session_id,
            connection=db_path
        )

        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            chat_memory=self.chat_history,
            return_messages=True
        )

        self.agent = initialize_agent(
            llm=self.llm,
            tools=[FoodImageAnalyserTool()],
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=True,
            memory=self.memory,
            agent_kwargs={
                "system_prompt": system_prompt
            }
        )


    def run(self, user_input):
        try:
            response = self.agent.run(user_input)
            print(f'Nutritionist: {response}')
            return response
        except Exception as error:
            print(f'Error: {error}')
            return 'Desculpe, ocorreu um erro ao processar sua solicitação. Por favor, tente novamente mais tarde.'