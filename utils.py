from exceptions import NoAudioDevice

def convert_cp_to_utf(mics: list):
    if not len(mics):
        raise NoAudioDevice

    for idx in range(len(mics)):
        mics[idx] = mics[idx].encode('cp1252').decode('utf8')
    return mics

def get_input_device(mics: list):
    print("--------------------------------------")
    for i in range(len(mics)):
        print(str(i+1),".",mics[i])
    selected_mic = input('PLEASE SELECT INPUT DEVICE:')
    is_valid = True
    try:
        if int(selected_mic) -1 < len(mics):
            raise NoAudioDevice
    except Exception as e:
        print("ERROR: Invalid input device entered.")
        is_valid = False
    finally:
        return is_valid, selected_mic

def get_record_duration():
    print("--------------------------------------")
    duration = input("PLEASE ENTER RECORD DURATION (SECONDS): ")
    try:
        if int(duration) > 2700:
            print("WARNING: The recording duration cannot exceed 2700 seconds.")
            return False, duration
    except Exception as e:
        return False, duration
    return True, int(duration)
