import os
from textwrap import dedent
import traceback

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from tools import add_note, list_notes, calculate


load_dotenv()


def main():
    model = ChatOpenAI(
        model=os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo').lower(),
        temperature=0,
        max_retries=2,
        timeout=15
    )

    agent = create_agent(
        model,
        tools=[add_note, list_notes, calculate],
        system_prompt='You are a helpful assistant with a calculator and a note-taking tool.'
    )

    welcome_msg = dedent('''\
    ---
    Agent CLI started. Type 'exit' to quit.
    Example commands:
    - calculate 2 + 3 * 4
    - note Buy milk
    - list notes
    ---''')
    print(welcome_msg)

    while True:
        try:
            user_input = input('\nUser: ').strip()
            if user_input.lower() == 'exit':
                break

            if not user_input:
                continue

            response = agent.invoke({
                'messages': [HumanMessage(user_input)],
            })
            print(f'Agent: {response["messages"][-1].content}')

            # track execution steps
            #
            # for chunk in agent.stream(
            #     {'messages': [HumanMessage(user_input)]},
            #     stream_mode='updates',
            # ):
            #     for step, data in chunk.items():
            #         print(f'step: {step}')
            #         print(f'content: {data["messages"][-1].content_blocks}')

        except KeyboardInterrupt:
            break
        except Exception:
            print(f'Some error occurred:\n{traceback.format_exc()}')


if __name__ == '__main__':
    main()
