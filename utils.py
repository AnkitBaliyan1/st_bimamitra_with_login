# from dotenv import load_dotenv
# load_dotenv()


# importing for generating resposne.
import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Pinecone
from pinecone import Pinecone as PineconeClient
from langchain.chains.question_answering import load_qa_chain

def generate_response_rag(user_input):
    k=os.environ.get("k")
    embeddings = OpenAIEmbeddings()
    
    pinecone_index_name=os.environ.get("PINECONE_INDEX_NAME")
    PineconeClient(
    api_key=os.environ.get("PINECONE_API_KEY")
    )
    index = Pinecone.from_existing_index(pinecone_index_name, embeddings, namespace=os.environ.get("NAMESPACE"))

    similar_doc = index.similarity_search_with_score(user_input, int(k))

    relevant_docs = [doc for doc, similarity_score in similar_doc]


    llm = ChatOpenAI(temperature=0.0)
    chain = load_qa_chain(llm=llm, chain_type="stuff")

    question = f"""  
        You are a chatbot named 'BimaMitra'.
        Your job is to assist user for their insurance related queryies but your knowledge source is limited to the document provided.
        Carefully review the provided document to address the query. 
        If the document contains relevant information that directly answers the question, 
        please provide a detailed response based on that information. 
        However, if the document does not contain pertinent details or if the answer cannot be derived from the document, 
        politely decline to answer, stating the lack of relevant information in the document as the reason. 
        
        Question: Hi?
        Response: Hey, I'm BimaMitra. wonderful to see that you wish to interact with me. Tell me how can i help you.
        
        Question: what is insurance?
        Response: Insurance is a financial arrangement where individuals pay premiums to an insurance company in exchange for protection against specific risks. In the event of a covered loss or event, the insurer provides compensation or coverage as outlined in the policy. It operates on the principle of risk pooling, spreading the financial burden of unexpected events among a larger group.

        Question: what is Large language model ?
        Response: I'm sorry but I can't find information about Large Language Model in provided document.

        Question: {user_input}
        Response:

        """
    
    response = chain.run(input_documents = relevant_docs, question = question)

    return response
