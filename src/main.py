from src.communication import WebServer
from src.common.ConfigProperties import ConfigProperties
from src.services.RecognitionService import RecognitionService

config = ConfigProperties()


# TODO: Add debug main with debug visualization & adjustment for parameters, cleanup main
if __name__ == "__main__":

    print(f"[{'PROD' if config.DEPLOY_ENV_PROD else 'DEV'}] Start Programm...")

    if (config.DEPLOY_ENV_PROD):
        WebServer.app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        RecognitionService.analyze_turntable_video_stream()

    print("End Programm...")
