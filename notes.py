import asyncio


async def hi():
    task = asyncio.Task.current_task()
    return "hi " + task.msg


async def main():
    task = loop.create_task(hi())
    task.msg = "am cow"
    print(await task)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
