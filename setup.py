import asyncio
import subprocess

async def run_process(loop, command):
    try:
        process = await asyncio.create_subprocess_shell(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = await process.communicate()
    except NotImplementedError:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = await loop.run_in_executor(None, process.communicate)

    return [output.decode() for output in result]

async def setup(loop):
    try:
        out, exc = await run_process(loop, "python3 -m pip install -r requirements.txt")
        print(f"stdout: \n{out}")
    
        if exc:
            print(f"stderr: \n{exc}")
    except Exception as exc:
        print(f"Error while setup... \n{exc}")
    else:
        print("setup complete")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(setup(loop))
