import asyncio

async def run_java_process(scan_id: str):
    cmd = ["java", "-jar", "/analyser/target/analyse.jar", scan_id]
    
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        
        print(f"Erreur Java : {stderr.decode()}")
    else:
        print(f"Résultat Java : {stdout.decode()}")