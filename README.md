
# Llama-Law 
LlamaLaw is an AI-powered chatbot designed to help visitors and newcomers navigate government websites and understand legal processes with ease. Built with a fine-tuned language model trained on legal conversations, LlamaLaw provides multilingual support, breaking down complex information on topics like visas, permits, and residency applications into clear, step-by-step guidance. By offering accurate, up-to-date information and a user-friendly experience, LlamaLaw simplifies government procedures, making essential services more accessible and reducing confusion for users.


## Demo

[![Watch the video]](https://youtu.be/loLcfCr6Ul0)
## Architecture

![App Screenshot](https://github.com/Immortal-Pi/doc_chat_bot/blob/main/resources/1.png)

## Features

#### Multilingual model
Provides legal assistance in any given language
#### Provide any URL
Provide any web URL and the bot provides the right instruction to navigate 
#### Legal Assistance
This is a legal chatbot provies legal information and assistance as per the webpage
#### Guide
Gives step by step instruction to navigate through the webpage and provides rules and regulations




## Key Highlights

This project was built for the hackathon Llama-Impact-Hackathon so we used the llama-3 models, We used Together.AI platform for API's for our project. We also leveraged togetherai for fine tuning our models to this perticular use case. we trained the model using the below lawyer-instruct dataset from hugging face. We compared other models hosted on togetherai and finally choose llama-3-8B-instruct for our use case.




## Screenshot

![App Screenshot](https://github.com/Immortal-Pi/doc_chat_bot/blob/main/resources/1.png)

![App Screenshot](https://github.com/Immortal-Pi/doc_chat_bot/blob/main/resources/2.png)

![App Screenshot](https://github.com/Immortal-Pi/doc_chat_bot/blob/main/resources/3.png)

![App Screenshot](https://github.com/Immortal-Pi/doc_chat_bot/blob/main/resources/4.png)


## Tech Stack

**web-scraping**
[crawl4ai]('https://github.com/unclecode/crawl4ai')

**base model** 
[huggingface](https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct)

**dataset for fine-tuning our model**
[huggingface](https://huggingface.co/datasets/Alignment-Lab-AI/Lawyer-Instruct)

**User Interface** - Streamlit

**Vectordatabase** - ChromaDB





## Conclusion
LlamaLaw addresses several critical challenges that tourists, visitors, international students and citizens face when trying to navigate government websites and access legal services:

1. Language Barriers: LlamaLaw provides multilingual support, allowing users to access guidance in their preferred language.

2. Complex Legal Jargon: It simplifies legal terms, making government information clear and easy to understand.

3. Time-Consuming Navigation: LlamaLaw offers quick, direct answers, helping users find what they need without endless searching.

4. Misinformation and Errors: By providing accurate, updated information, LlamaLaw reduces misunderstandings and mistakes.

5. Lack of Personalized Support: It delivers personalized, step-by-step guidance, offering a more supportive experience.
## Authors

- [@Amruth Pai](https://www.linkedin.com/in/amruthpai/)
- [@Mcenroe](https://www.linkedin.com/in/mcenroe-ryan-dsilva-591798185/)
- [@Daarun](https://www.linkedin.com/in/daarun-jk/)


## Acknowledgements
 - [Llama Impact Hackathon](https://lablab.ai/event/llama-impact-hackathon)
 - [Together AI](https://www.together.ai/)

