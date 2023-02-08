from KafkaManager import KafkaManager
import speech_recognition as sr
import asyncio
from utils import (convert_cp_to_utf, get_input_device, get_record_duration)
from exceptions import RecordDurationTooLong
import argparse


async def recognizer():
    r = sr.Recognizer()
    try:
        kafka_manager = KafkaManager()
    except Exception as e:
        print("ERROR: Kafka could not be initialized. Message:", str(e))
        return None

    mics = sr.Microphone.list_microphone_names()
    # cover convert cp to utf with try except
    mics = convert_cp_to_utf(mics)

    while True:
        is_mic_valid, selected_mic = get_input_device(mics)
        is_duration_valid, duration = get_record_duration()
        
        if is_mic_valid and is_duration_valid:
            print(f"LOG: Preparing for {duration} second recording on device {mics[int(selected_mic)-1]}.")
            break
        elif not is_mic_valid:
            print("WARNING: Your input choice is not valid. \n"
            "Please choice one of the choice.")
        elif not is_duration_valid:
            print("WARNING: Record duration time is not valid.\n"
            "Please try again.")
        else:
            print("WARNING: Please enter valid inputs.")
        

    while True and kafka_manager:
        try:
            with sr.Microphone(device_index=int(selected_mic) - 1) as source:
                # mics = sr.Microphone.list_microphone_names()
                # mics = convert_cp_to_utf(mics)
                print("LOG: Starting recording.")
                audio_data = r.record(source, duration=duration)
                text = r.recognize_google(audio_data, language="en-US")
                if kafka_manager.produce:
                    await kafka_manager.produce(message=text)
                else:
                    print("LOG: Kafka producer could not connect to bootstrap server.")
                    return None
        except Exception as e:
            continue


async def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--foo', help='foo help')
    # args = parser.parse_args()
    # parser = argparse.ArgumentParser()

    # parser.add_argument(dest="--duration", default=600, help="This is the time period for registration. In seconds. Default: 600 seconds. \n"
    #                     "If duration is not specified, then it will record until there is no more audio input")
    # # print(parser.print_help())
    # parser.add_argument("--accent", default='US', help="Define english accent. \n"
    #                     "GB: British\n"
    #                     "US: USA")
    # # parser.add_argument("--add-one", action="count")
    # parser.add_argument(
    #     "--version", default="1.0", help="App version"
    # )
    # args = parser.parse_args
    # print(args)
    # return None
    # print(args.version)
    asyncio.create_task(recognizer())  # last to finish
    # asyncio.create_task(KafkaManager.consume())
    await asyncio.sleep(10)

asyncio.get_event_loop().run_until_complete(main())
