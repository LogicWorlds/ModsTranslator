import sys, time
#from yandexfreetranslate import YandexFreeTranslate
from easygoogletranslate import EasyGoogleTranslate
debug = True
#yt = YandexFreeTranslate()
gt = EasyGoogleTranslate()

if __name__ == "__main__":
    if len (sys.argv) == 1:
        print ("Привет, мир!")
    else:
        if len (sys.argv) < 3:
            print ("Ошибка. Слишком мало параметров.")
            sys.exit (1)

        if len (sys.argv) > 3:
            print ("Ошибка. Слишком много параметров.")
            sys.exit (1)

        param_name = sys.argv[1]
        param_value = sys.argv[2]

        if (param_name == "--input" or
                param_name == "-i"):
            print ("Start translating: {}!".format (param_value) )
        else:
            print ("Ошибка. Неизвестный параметр '{}'".format (param_name) )
            sys.exit (1)

        try:
            print(f"Reading {param_value}")
            f = open(param_value, encoding="utf-8")
            data = f.read();
            translated = ""
            to_translated_text = ""
            line_number = 0
            to_translate_arr = []
            # Разбиваем и читаем по строкам
            print(f"Preparing to translate...")
            data_splited = data.split("\n")
            for data_line in data_splited:
                line_number += 1
                line_part = data_line.split("=")
                if (len(line_part) > 1):
                    label = line_part[0]
                    text = line_part[1]
                 
                    if text:
                        #translated_text = yt.translate("en", "ru", text)
                        if ((len(to_translated_text)+len(text)) > 4500):
                            to_translate_arr.append(to_translated_text)
                            to_translated_text = ""
                        to_translated_text += f"{text}\n"
                        
                        
                    if (debug):
                        print(f"[{line_number}/{len(data_splited)}]: {text}")
                    #time.sleep(0.3)
            if (len(to_translated_text) > 0):
                to_translate_arr.append(to_translated_text)
                to_translated_text = ""
                
            print(f"Translating...")
            for packet_id, to_translate_packet in enumerate(to_translate_arr):
                print(f"Translating packet: {str(packet_id+1)}")
                to_translated_text += "\n"+gt.translate(to_translate_packet, target_language='ru')
                #time.sleep(0.3)
            print(f"Compiling translated file...")
            to_translated_text = to_translated_text.split("\n")
            line_number = 0
            translated_line = 1
            for data_line in data_splited:
                line_number += 1
                line_part = data_line.split("=")
                if (len(line_part) > 1):
                    label = line_part[0]
                    text = line_part[1]
                    translated += f"{label}={to_translated_text[translated_line]}\n"
                    if (debug):
                        print(f"[{line_number}/{len(data_splited)}]: {to_translated_text[translated_line]}")
                    translated_line += 1
                    #time.sleep(0.3)
                else:
                    label = line_part[0]
                    translated += f"{label}\n"
                



            ru_file_name = param_value.replace('en_US', 'ru_RU')
            ru_file_name = ru_file_name.replace('en_us', 'ru_ru')
            print(f"Writing {ru_file_name}")
            t = open(ru_file_name, "w", encoding="utf-8")
            t.write(translated)
            t.close()
            # Do something with the file
        except IOError:
            print("File not accessible")
        finally:
            f.close()
        print("Translating finished!")
