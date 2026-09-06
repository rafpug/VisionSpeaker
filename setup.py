import subprocess
import configparser

def main():
    config = configparser.ConfigParser()
    config.read("config.ini")

    vision_user = config.get("vision_pi", "user")
    vision_ip = config.get("vision_pi", "ip")
    # voice_user = config.get("voice_pi", "user")
    # voice_ip = config.get("voice_pi", "ip")
    process = subprocess.run(["scp", "./vision-identifier.py", f"{vision_user}@{vision_ip}:~/"])

if __name__ == "__main__":
    main()