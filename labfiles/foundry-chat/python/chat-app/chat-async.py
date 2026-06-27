import glob
import os
from dotenv import load_dotenv

# import namespaces for async
from openai import AsyncOpenAI
import asyncio

async def main():

    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        # Get configuration settings
        load_dotenv()
        azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        model_deployment = os.getenv("MODEL_DEPLOYMENT")

        # Initialize an async OpenAI client
        async_client = AsyncOpenAI(
            base_url = azure_openai_endpoint,
            api_key = os.getenv("AZURE_OPEN_AI_KEY"),
        )
        vector_store = await async_client.vector_stores.create(
            name="ASHUTOSH_9102307389"
        )

        file_streams = [open(f, "rb") for f in glob.glob(r"C:\Users\asus\Downloads\docs\*.pdf")]
        if not file_streams:
            print("No PDF files found in the specified directory.")
            return
        
        file_batch = await async_client.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id,
            files = file_streams,
        )

        for f in file_streams:
            f.close()
        print(f"Vector store created with {file_batch.file_counts.completed} files")
        # Track responses
        last_response_id = None

        # Loop until the user wants to quit
        while True:
            input_text = input('\nEnter a prompt (or type "quit" to exit): ')
            if input_text.lower() == "quit":
                break
            if len(input_text) == 0:
                print("Please enter a prompt.")
                continue

            # Await an asynchronous response
            stream = await async_client.responses.create(
                model = model_deployment,
                instructions="You are a helpful AI assistant that answers questions and provides information.",
                input = input_text,
                previous_response_id = last_response_id,
                stream = True,
                tools = [
                    {"type": "code_interpreter",
                    "container": {"type": "auto"}},
                    {"type":"web_search"},
                    {"type": "file_search",
                    "vector_store_ids": [vector_store.id]}
                ],
                include = ["file_search_call.results"]
            )

            async for event in stream:
                if event.type == "response.output_text.delta":
                    print(event.delta, end ="", flush = True)
                elif event.type == "response.completed":
                    last_response_id = event.response.id
            print()
    except Exception as ex:
        print(ex)

    finally:
        # Close the async client session
        await async_client.close()


if __name__ == '__main__':
    asyncio.run(main())
