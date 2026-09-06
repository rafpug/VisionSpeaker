import subprocess
import configparser

def main():
    config = configparser.ConfigParser()
    config.read("config.ini")

    vision_user = config.get("vision_pi", "user")
    vision_ip = config.get("vision_pi", "ip")
    voice_user = config.get("voice_pi", "user")
    voice_ip = config.get("voice_pi", "ip")
    process = subprocess.Popen(["ssh", f"{vision_user}@{vision_ip}", "python3 -u", 
                                "~/vision-identifier.py"], 
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                               text=True, bufsize=1)

    try:
        for line in process.stdout:
            print("stuck")
            line = line.strip().split("/")
            print(line[0], flush=True)
    except KeyboardInterrupt:
        print("\nStopping SSH connection...")
        process.terminate()

        try:
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()

    finally:
        if process.poll() is None:
            process.terminate()
            process.wait()
    
if __name__ == "__main__":
    main()